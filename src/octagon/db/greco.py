"""Load the Greco1899 ufcstats scrape CSVs — the canonical fight data.

Source: https://github.com/Greco1899/scrape_ufc_stats (regularly re-scraped
and published; our own scraper is blocked by ufcstats' anti-bot wall).

Files and how they connect:
* ufc_event_details.csv   — events with URL uid, date, location
* ufc_fight_results.csv   — one row per fight; references its event BY NAME
  (names verified unique), fighters by 'A vs. B' bout string, fight URL uid
* ufc_fight_stats.csv     — one row per fighter PER ROUND; we aggregate to
  whole-fight totals keyed by (event, bout, fighter)
* ufc_fighter_details.csv — fighter uid -> nickname
* ufc_fighter_tott.csv    — fighter uid -> tale of the tape
"""

import csv
import sqlite3
from collections import defaultdict
from pathlib import Path

from octagon.db.parsing import (
    fight_duration_seconds,
    parse_bout,
    parse_dob,
    parse_height_to_cm,
    parse_long_date,
    parse_method,
    parse_mmss_to_seconds,
    parse_of_pair,
    parse_outcome,
    parse_reach_to_cm,
    parse_time_format,
    parse_weightclass,
    parse_weight_to_kg,
)


def _clean(s: str) -> str:
    """Collapse stray whitespace — the CSVs have trailing spaces everywhere."""
    return " ".join((s or "").split())


def _read_csv(path: Path) -> list[dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _uid(url: str) -> str:
    return url.rstrip("/").rsplit("/", 1)[-1]


def load_greco(conn: sqlite3.Connection, greco_dir: Path) -> dict[str, int]:
    counts = {"events": 0, "fights": 0, "fight_stats": 0, "fighters": 0,
              "skipped_fights": 0, "skipped_stat_rows": 0}

    # --- events ---
    event_ids: dict[str, tuple[int, str]] = {}  # clean name -> (event_id, date)
    for row in _read_csv(greco_dir / "ufc_event_details.csv"):
        name, date = _clean(row["EVENT"]), parse_long_date(row["DATE"])
        if not date:
            continue
        cur = conn.execute(
            "INSERT INTO events (uid, name, date, location, source) VALUES (?, ?, ?, ?, 'greco')",
            (_uid(row["URL"]), name, date, _clean(row["LOCATION"]) or None),
        )
        event_ids[name] = (cur.lastrowid, date)
        counts["events"] += 1

    # --- per-round stats, aggregated to whole-fight totals per fighter ---
    # Keyed by (event, bout, fighter) since the stats file has no fight URL.
    totals: dict[tuple[str, str, str], dict[str, int | None]] = {}
    for row in _read_csv(greco_dir / "ufc_fight_stats.csv"):
        if not row["ROUND"].strip():  # a few blank filler rows
            counts["skipped_stat_rows"] += 1
            continue
        key = (_clean(row["EVENT"]), _clean(row["BOUT"]), _clean(row["FIGHTER"]))
        agg = totals.setdefault(key, defaultdict(int))

        sig_l, sig_a = parse_of_pair(row["SIG.STR."])
        tot_l, tot_a = parse_of_pair(row["TOTAL STR."])
        td_l, td_a = parse_of_pair(row["TD"])
        for field, value in [
            ("knockdowns", int(row["KD"]) if row["KD"].strip().isdigit() else None),
            ("sig_landed", sig_l), ("sig_attempted", sig_a),
            ("total_landed", tot_l), ("total_attempted", tot_a),
            ("td_landed", td_l), ("td_attempted", td_a),
            ("sub_attempts", int(row["SUB.ATT"]) if row["SUB.ATT"].strip().isdigit() else None),
            ("reversals", int(row["REV."]) if row["REV."].strip().isdigit() else None),
            ("ctrl_seconds", parse_mmss_to_seconds(row["CTRL"])),
        ]:
            if value is not None:
                agg[field] += value

    # --- fights ---
    stat_fields = ["knockdowns", "sig_landed", "sig_attempted", "total_landed",
                   "total_attempted", "td_landed", "td_attempted",
                   "sub_attempts", "reversals", "ctrl_seconds"]
    for row in _read_csv(greco_dir / "ufc_fight_results.csv"):
        event_name = _clean(row["EVENT"])
        bout = parse_bout(_clean(row["BOUT"]))
        winner = parse_outcome(row["OUTCOME"])
        if event_name not in event_ids or bout is None or winner is None:
            counts["skipped_fights"] += 1
            continue
        event_id, date = event_ids[event_name]
        fighter1, fighter2 = bout

        weight_class, title = parse_weightclass(row["WEIGHTCLASS"])
        method, detail = parse_method(row["METHOD"])
        round_minutes = parse_time_format(row["TIME FORMAT"])
        end_round = int(row["ROUND"]) if row["ROUND"].strip().isdigit() else None
        end_time_s = parse_mmss_to_seconds(row["TIME"])

        cur = conn.execute(
            """INSERT INTO fights (uid, event_id, date, weight_class, title_fight,
                                   scheduled_rounds, fighter1, fighter2, winner,
                                   method, method_detail, end_round, end_time_s,
                                   duration_s, source)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'greco')""",
            (_uid(row["URL"]), event_id, date, weight_class, int(title),
             len(round_minutes) if round_minutes else None,
             fighter1, fighter2, winner, method, detail, end_round, end_time_s,
             fight_duration_seconds(end_round, end_time_s, round_minutes)),
        )
        fight_id = cur.lastrowid
        counts["fights"] += 1

        bout_key = _clean(row["BOUT"])
        for corner, fighter in [("fighter1", fighter1), ("fighter2", fighter2)]:
            agg = totals.get((event_name, bout_key, fighter))
            if agg is None:
                continue  # old fights have no stats table on ufcstats
            conn.execute(
                f"""INSERT INTO fight_stats (fight_id, fighter, corner,
                                             {', '.join(stat_fields)})
                    VALUES (?, ?, ?, {', '.join('?' * len(stat_fields))})""",
                (fight_id, fighter, corner,
                 *(agg.get(f) for f in stat_fields)),
            )
            counts["fight_stats"] += 1

    # --- fighters: tott (tale of the tape) + details (nickname), joined on uid ---
    nicknames = {
        _uid(r["URL"]): _clean(r["NICKNAME"]) or None
        for r in _read_csv(greco_dir / "ufc_fighter_details.csv")
    }
    for row in _read_csv(greco_dir / "ufc_fighter_tott.csv"):
        uid = _uid(row["URL"])
        try:
            conn.execute(
                """INSERT INTO fighters (uid, name, nickname, height_cm, reach_cm,
                                         weight_kg, stance, dob, source)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'greco')""",
                (uid, _clean(row["FIGHTER"]), nicknames.get(uid),
                 parse_height_to_cm(row["HEIGHT"]), parse_reach_to_cm(row["REACH"]),
                 parse_weight_to_kg(row["WEIGHT"]), _clean(row["STANCE"]) or None,
                 parse_dob(row["DOB"])),
            )
            counts["fighters"] += 1
        except sqlite3.IntegrityError:  # duplicate uid row in the CSV
            pass

    conn.commit()
    return counts

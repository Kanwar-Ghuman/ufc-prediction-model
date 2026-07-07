"""Attach the bootstrap dataset's closing odds to canonical (Greco) fights.

The jansen88/ufc-data bootstrap was our day-1 fight data; the Greco scrape
(richer, current) has replaced it for fights/fighters/stats. What the
bootstrap still uniquely contributes is ~3.4k closing odds (betmma.tips,
2014 -> 2023), which live in complete_ufc_data.csv already matched to fights.

Matching problem: the two sources spell names differently ('José Aldo' vs
'Jose Aldo', 'Weili Zhang' vs 'Zhang Weili'), so we join on
(event_date, unordered pair of normalized names) and report the match rate —
silent partial joins are how datasets rot.
"""

import csv
import sqlite3
from pathlib import Path

from octagon.db.parsing import normalize_name, parse_valid_odds


def load_bootstrap_odds(conn: sqlite3.Connection, bootstrap_dir: Path) -> dict[str, int]:
    counts = {"odds_matched": 0, "odds_matched_one_name": 0,
              "odds_unmatched": 0, "odds_invalid": 0}

    # Index every fight in the DB two ways:
    # 1. (date, unordered normalized name pair) — the precise join.
    # 2. (date, one normalized name) — fallback for fighters who changed
    #    their listed name between sources ('Bobby Green' -> 'King Green',
    #    'Katlyn Chookagian' -> 'Katlyn Cerminara'). A fighter fights at
    #    most once per night, so date + one name is still identifying.
    pair_index: dict[tuple[str, frozenset[str]], tuple[int, str, str]] = {}
    name_index: dict[tuple[str, str], list[tuple[int, str, str]]] = {}
    for row in conn.execute("SELECT fight_id, date, fighter1, fighter2 FROM fights"):
        f1n, f2n = normalize_name(row["fighter1"]), normalize_name(row["fighter2"])
        entry = (row["fight_id"], f1n, f2n)
        pair_index[(row["date"], frozenset((f1n, f2n)))] = entry
        name_index.setdefault((row["date"], f1n), []).append(entry)
        name_index.setdefault((row["date"], f2n), []).append(entry)

    with open(bootstrap_dir / "complete_ufc_data.csv", newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            fav_odds = parse_valid_odds(row["favourite_odds"])
            dog_odds = parse_valid_odds(row["underdog_odds"])
            if fav_odds is None or dog_odds is None:
                counts["odds_invalid"] += 1
                continue

            date = row["event_date"]
            fav_n = normalize_name(row["favourite"])
            dog_n = normalize_name(row["underdog"])

            entry = pair_index.get((date, frozenset((fav_n, dog_n))))
            if entry is not None:
                counts["odds_matched"] += 1
            else:
                candidates = {e for n in (fav_n, dog_n) for e in name_index.get((date, n), [])}
                if len(candidates) != 1:
                    counts["odds_unmatched"] += 1
                    continue
                entry = candidates.pop()
                counts["odds_matched_one_name"] += 1
            fight_id, db_f1n, db_f2n = entry

            # Orient favourite/underdog odds to the DB fight's corners; with a
            # renamed fighter only one of the two names may match — that's enough.
            if fav_n == db_f1n or dog_n == db_f2n:
                f1_odds, f2_odds = fav_odds, dog_odds
            elif fav_n == db_f2n or dog_n == db_f1n:
                f1_odds, f2_odds = dog_odds, fav_odds
            else:  # neither corner identifiable — don't guess
                counts["odds_unmatched"] += 1
                continue
            conn.execute(
                """INSERT OR IGNORE INTO odds (fight_id, fighter1_odds, fighter2_odds, source)
                   VALUES (?, ?, ?, 'betmma')""",
                (fight_id, f1_odds, f2_odds),
            )

    conn.commit()
    return counts

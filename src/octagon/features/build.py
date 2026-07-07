"""Point-in-time feature builder — the heart of the project (PRD section 5).

The one rule: for a fight on date D, every feature must be computable from
information available BEFORE D. We enforce it by construction: fights are
replayed in chronological order, and each fighter's snapshot is taken from
their accumulated history *before* appending the current fight to it.
tests/test_features.py proves the property by truncation: a fight's features
must not change when future fights are deleted from the input.

Symmetry (PRD 5.5): sources list fighters in orders that correlate with the
winner, so the assembled rows get a seeded coin-flip corner swap — f1/f2
columns exchanged, differentials negated, label flipped. A model then can't
learn "fighter1 tends to win"; it has to learn fight dynamics.

The builder is a pure function over plain data (no SQL inside) so tests can
feed it tiny synthetic histories and check the arithmetic by hand.
"""

import random
import sqlite3
from dataclasses import dataclass, field
from datetime import date as date_type
from datetime import datetime

from octagon.features.elo import Elo

# ---------------------------------------------------------------------------
# Input records (plain data in, plain dicts out)
# ---------------------------------------------------------------------------


@dataclass
class Bout:
    """One fight as the builder consumes it, already in chronological order."""

    fight_id: int
    date: str                    # ISO
    fighter1: str
    fighter2: str
    winner: str                  # 'fighter1' | 'fighter2' | 'draw' | 'nc'
    method: str | None
    end_round: int | None
    duration_s: int | None
    weight_class: str | None
    title_fight: int
    scheduled_rounds: int | None
    stats1: dict | None          # fight_stats row for each corner (or None)
    stats2: dict | None
    odds1: float | None          # decimal closing odds (or None)
    odds2: float | None


@dataclass
class PastFight:
    """One completed fight from a single fighter's perspective."""

    date: date_type
    result: str                  # 'win' | 'loss' | 'draw' | 'nc'
    method: str | None
    end_round: int | None
    duration_s: int | None
    stats: dict | None           # own fight_stats
    opp_stats: dict | None       # opponent's fight_stats (what we absorbed)
    opp_elo_pre: float = 1500.0  # opponent's Elo entering that fight (strength of schedule)


@dataclass
class FighterHistory:
    fights: list[PastFight] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Per-fighter snapshot (everything known about a fighter BEFORE date D)
# ---------------------------------------------------------------------------


def _ratio(num: float | None, den: float | None) -> float | None:
    """Safe division: None when the denominator is missing or zero."""
    if num is None or not den:
        return None
    return num / den


def _window_stats(window: list[PastFight], suffix: str) -> dict[str, float | None]:
    """Rolling per-minute/accuracy stats over the last N statted fights.

    Rates are computed as (sum of numerators / sum of denominators) across
    the window rather than averaging per-fight rates — a 30-second KO
    shouldn't count as much striking evidence as a 25-minute war.
    """
    minutes = sum(f.duration_s for f in window) / 60 if window else 0

    def total(key: str, opponent: bool = False) -> int | None:
        rows = [(f.opp_stats if opponent else f.stats) for f in window]
        values = [r[key] for r in rows if r and r[key] is not None]
        return sum(values) if values else None

    return {
        f"slpm_{suffix}": _ratio(total("sig_landed"), minutes),
        f"sapm_{suffix}": _ratio(total("sig_landed", opponent=True), minutes),
        f"sig_acc_{suffix}": _ratio(total("sig_landed"), total("sig_attempted")),
        f"sig_def_{suffix}": (
            None if total("sig_attempted", opponent=True) in (None, 0)
            else 1 - total("sig_landed", opponent=True) / total("sig_attempted", opponent=True)
        ),
        f"td15_{suffix}": _ratio(total("td_landed"), minutes / 15 if minutes else None),
        f"td_acc_{suffix}": _ratio(total("td_landed"), total("td_attempted")),
        f"td_def_{suffix}": (
            None if total("td_attempted", opponent=True) in (None, 0)
            else 1 - total("td_landed", opponent=True) / total("td_attempted", opponent=True)
        ),
        f"sub15_{suffix}": _ratio(total("sub_attempts"), minutes / 15 if minutes else None),
        f"kd15_{suffix}": _ratio(total("knockdowns"), minutes / 15 if minutes else None),
        f"ctrl_pct_{suffix}": _ratio(total("ctrl_seconds"), minutes * 60 if minutes else None),
    }


def fighter_snapshot(
    history: FighterHistory,
    on_date: date_type,
    tott: dict | None,
    elo_rating: float,
) -> dict[str, float | None]:
    """All point-in-time features for one fighter entering a fight."""
    fights = history.fights
    decisive = [f for f in fights if f.result in ("win", "loss")]
    wins = [f for f in decisive if f.result == "win"]
    losses = [f for f in decisive if f.result == "loss"]

    # Current streak: consecutive wins (+) or losses (-); draw/nc breaks it.
    streak = 0
    for f in reversed(fights):
        if f.result == "win" and streak >= 0:
            streak += 1
        elif f.result == "loss" and streak <= 0:
            streak -= 1
        else:
            break

    age = None
    if tott and tott.get("dob"):
        dob = datetime.strptime(tott["dob"], "%Y-%m-%d").date()
        age = (on_date - dob).days / 365.25

    last = fights[-1].date if fights else None
    timed = [f for f in fights if f.duration_s is not None]
    total_min = sum(f.duration_s for f in timed) / 60 if timed else None
    statted = [f for f in fights if f.stats and f.duration_s]

    def rate(subset: list[PastFight], base: list[PastFight]) -> float | None:
        return _ratio(len(subset), len(base))

    snapshot = {
        "age": age,
        "height_cm": tott.get("height_cm") if tott else None,
        "reach_cm": tott.get("reach_cm") if tott else None,
        "southpaw": (1.0 if tott.get("stance") == "Southpaw" else 0.0) if tott and tott.get("stance") else None,
        "n_fights": float(len(fights)),
        "wins": float(len(wins)),
        "losses": float(len(losses)),
        "win_pct": rate(wins, decisive),
        "streak": float(streak),
        "layoff_days": float((on_date - last).days) if last else None,
        "fights_12m": float(sum(1 for f in fights if (on_date - f.date).days <= 365)),
        "fights_24m": float(sum(1 for f in fights if (on_date - f.date).days <= 730)),
        "total_octagon_min": total_min,
        "avg_fight_min": _ratio(total_min, len(timed)),
        # Finish profile: how do this fighter's wins/losses happen?
        "ko_win_rate": rate([f for f in wins if f.method == "KO/TKO"], decisive),
        "sub_win_rate": rate([f for f in wins if f.method == "SUB"], decisive),
        "dec_win_rate": rate([f for f in wins if f.method and f.method.endswith("DEC")], decisive),
        "times_koed": float(len([f for f in losses if f.method == "KO/TKO"])),
        "times_subbed": float(len([f for f in losses if f.method == "SUB"])),
        # Cardio proxy: share of wins that were finishes in round 3+.
        "late_finish_rate": rate(
            [f for f in wins if f.method in ("KO/TKO", "SUB") and (f.end_round or 0) >= 3],
            decisive),
        "elo": elo_rating,
        # Strength of schedule: a 5-0 record against 1400-rated opposition is
        # not a 5-0 record against 1650-rated opposition.
        "opp_elo_l5": (sum(f.opp_elo_pre for f in fights[-5:]) / len(fights[-5:])
                       if fights else None),
    }
    snapshot |= _window_stats(statted[-3:], "l3")
    snapshot |= _window_stats(statted[-5:], "l5")
    return snapshot


# ---------------------------------------------------------------------------
# The chronological sweep
# ---------------------------------------------------------------------------

_ELO_SCORES = {"fighter1": 1.0, "fighter2": 0.0, "draw": 0.5}


def build_feature_rows(
    bouts: list[Bout],
    tott_by_name: dict[str, dict],
    elo_k: float = 32.0,
    seed: int = 42,
) -> list[dict]:
    """Replay bouts chronologically; emit one modeling row per decisive fight.

    Draws and no-contests produce no row (no label) but still update fighter
    histories — a draw is real cage time and real absorbed damage.

    Bouts with winner == 'upcoming' (a future card) emit a row with
    label=None built from history as of the card date, are never corner-
    swapped, and leave histories and Elo untouched — nothing has happened.
    """
    rng = random.Random(seed)
    elo = Elo(k=elo_k)
    histories: dict[str, FighterHistory] = {}
    rows: list[dict] = []

    for bout in bouts:
        on_date = date_type.fromisoformat(bout.date)
        snaps = {}
        for corner, name in [("f1", bout.fighter1), ("f2", bout.fighter2)]:
            history = histories.setdefault(name, FighterHistory())
            snaps[corner] = fighter_snapshot(
                history, on_date, tott_by_name.get(name), elo.get(name))

        if bout.winner in ("fighter1", "fighter2", "upcoming"):
            row = {
                "fight_id": bout.fight_id,
                "date": bout.date,
                "weight_class": bout.weight_class,
                "gender": "F" if (bout.weight_class or "").startswith("Women") else "M",
                "title_fight": bout.title_fight,
                "scheduled_rounds": bout.scheduled_rounds,
                "f1_name": bout.fighter1,
                "f2_name": bout.fighter2,
                "f1_odds": bout.odds1,
                "f2_odds": bout.odds2,
                "label": {"fighter1": 1, "fighter2": 0}.get(bout.winner),
                # How the fight ended — LABEL material for the method-of-victory
                # model, never a feature (it's an output of the fight).
                "method": bout.method,
                "swapped": 0,
            }
            for key, value in snaps["f1"].items():
                row[f"f1_{key}"] = value
            for key, value in snaps["f2"].items():
                row[f"f2_{key}"] = value
            for key in snaps["f1"]:
                a, b = snaps["f1"][key], snaps["f2"][key]
                row[f"diff_{key}"] = (a - b) if a is not None and b is not None else None
            if row["label"] is not None and rng.random() < 0.5:
                row = swap_corners(row)
            rows.append(row)

        if bout.winner == "upcoming":  # nothing happened yet — no updates
            continue

        # Only after the snapshots: append this fight to both histories.
        for name, own, opp, opp_elo, result in [
            (bout.fighter1, bout.stats1, bout.stats2, snaps["f2"]["elo"],
             {"fighter1": "win", "fighter2": "loss"}.get(bout.winner, bout.winner)),
            (bout.fighter2, bout.stats2, bout.stats1, snaps["f1"]["elo"],
             {"fighter1": "loss", "fighter2": "win"}.get(bout.winner, bout.winner)),
        ]:
            histories[name].fights.append(PastFight(
                date=on_date, result=result, method=bout.method,
                end_round=bout.end_round, duration_s=bout.duration_s,
                stats=own, opp_stats=opp, opp_elo_pre=opp_elo))
        if bout.winner != "nc":  # nothing was decided in a no-contest
            elo.update(bout.fighter1, bout.fighter2, _ELO_SCORES[bout.winner])

    return rows


def swap_corners(row: dict) -> dict:
    """Exchange the two fighters in an assembled row.

    f1_*/f2_* swap, diff_* negates, the label flips. Applying this twice
    must return the original row — tests rely on that involution.
    """
    swapped = dict(row)
    for key in row:
        if key.startswith("f1_"):
            other = "f2_" + key[3:]
            swapped[key], swapped[other] = row[other], row[key]
        elif key.startswith("diff_"):
            swapped[key] = -row[key] if row[key] is not None else None
    swapped["label"] = 1 - row["label"]
    swapped["swapped"] = 1 - row["swapped"]
    return swapped


# ---------------------------------------------------------------------------
# DB adapter: SQLite -> plain inputs -> parquet-ready rows
# ---------------------------------------------------------------------------


def load_bouts(conn: sqlite3.Connection) -> list[Bout]:
    """Read fights in true chronological order.

    Within one event the CSV lists the main event first, but prelims happen
    first in real time — and in the old tournament era one man fought several
    times in a night, so intra-event order genuinely matters for his record.
    Descending fight_id within a date approximates card order.
    """
    stats: dict[tuple[int, str], dict] = {}
    for row in conn.execute("SELECT * FROM fight_stats"):
        stats[(row["fight_id"], row["corner"])] = dict(row)

    odds: dict[int, tuple[float, float]] = {
        row["fight_id"]: (row["fighter1_odds"], row["fighter2_odds"])
        for row in conn.execute("SELECT * FROM odds")
    }

    bouts = []
    for row in conn.execute("SELECT * FROM fights ORDER BY date ASC, fight_id DESC"):
        fid = row["fight_id"]
        bouts.append(Bout(
            fight_id=fid, date=row["date"],
            fighter1=row["fighter1"], fighter2=row["fighter2"],
            winner=row["winner"], method=row["method"],
            end_round=row["end_round"], duration_s=row["duration_s"],
            weight_class=row["weight_class"], title_fight=row["title_fight"],
            scheduled_rounds=row["scheduled_rounds"],
            stats1=stats.get((fid, "fighter1")), stats2=stats.get((fid, "fighter2")),
            odds1=odds.get(fid, (None, None))[0], odds2=odds.get(fid, (None, None))[1],
        ))
    return bouts


def load_tott(conn: sqlite3.Connection) -> dict[str, dict]:
    """Tale-of-the-tape by name; names shared by 2+ fighters map to nothing.

    Fights reference fighters by name only, so for the handful of duplicate
    names we honestly don't know which person fought — no tott is better
    than the wrong man's reach.
    """
    by_name: dict[str, list[dict]] = {}
    for row in conn.execute("SELECT name, height_cm, reach_cm, stance, dob FROM fighters"):
        by_name.setdefault(row["name"], []).append(dict(row))
    return {name: rows[0] for name, rows in by_name.items() if len(rows) == 1}


def build_features(conn: sqlite3.Connection, elo_k: float, seed: int):
    """SQLite -> feature DataFrame (import pandas here to keep tests light)."""
    import pandas as pd

    rows = build_feature_rows(load_bouts(conn), load_tott(conn), elo_k=elo_k, seed=seed)
    return pd.DataFrame(rows)

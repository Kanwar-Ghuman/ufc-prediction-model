"""Data leakage audit (PRD section 6) — run with `python -m octagon audit`.

Unit tests guard the *code* (point-in-time by truncation, Elo pre-ratings,
swap involution on synthetic data). This module audits the *built artifacts*:
the real feature table against the real database, using independent
recomputation — deliberately NOT reusing the feature builder's code paths,
so a shared bug can't vouch for itself.

Every check returns (name, passed, detail); the CLI fails loudly if any fail.
"""

import math
import random
import sqlite3

import pandas as pd

from octagon.features.build import swap_corners

Check = tuple[str, bool, str]


def _record_before(conn: sqlite3.Connection, name: str, date: str, fight_id: int) -> tuple[int, int]:
    """Recompute a fighter's UFC record entering a fight, straight from SQL.

    'Before' means: earlier date, or same date with a LARGER fight_id — the
    builder replays same-day fights (old tournament era) in descending
    fight_id order because the source lists the main event first.
    """
    row = conn.execute(
        """SELECT
             SUM(CASE WHEN (fighter1 = :name AND winner = 'fighter1')
                        OR (fighter2 = :name AND winner = 'fighter2') THEN 1 ELSE 0 END) AS wins,
             SUM(CASE WHEN (fighter1 = :name AND winner = 'fighter2')
                        OR (fighter2 = :name AND winner = 'fighter1') THEN 1 ELSE 0 END) AS losses
           FROM fights
           WHERE (fighter1 = :name OR fighter2 = :name)
             AND (date < :date OR (date = :date AND fight_id > :fight_id))""",
        {"name": name, "date": date, "fight_id": fight_id},
    ).fetchone()
    return row["wins"] or 0, row["losses"] or 0


def _corner_features(row: pd.Series, name: str) -> dict | None:
    """Read one fighter's features out of a (possibly swapped) parquet row."""
    for prefix in ("f1", "f2"):
        if row[f"{prefix}_name"] == name:
            return {"wins": row[f"{prefix}_wins"], "losses": row[f"{prefix}_losses"]}
    return None


def check_records_vs_sql(conn: sqlite3.Connection, df: pd.DataFrame, n: int = 10) -> Check:
    """PRD: 'recompute N random fighters' features by hand from raw data'."""
    rng = random.Random(0)
    veterans = df[(df["f1_n_fights"] >= 3) | (df["f2_n_fights"] >= 3)]
    mismatches = []
    for _, row in veterans.sample(n * 3, random_state=rng.randint(0, 10**6)).iterrows():
        for name in (row["f1_name"], row["f2_name"]):
            wins, losses = _record_before(conn, name, row["date"], row["fight_id"])
            feat = _corner_features(row, name)
            if feat["wins"] != wins or feat["losses"] != losses:
                mismatches.append(f"{name} @ {row['date']}: table says "
                                  f"{feat['wins']}-{feat['losses']}, SQL says {wins}-{losses}")
    detail = f"checked {n * 6} fighter-records independently"
    if mismatches:
        detail = "; ".join(mismatches[:3])
    return ("records match independent SQL recomputation", not mismatches, detail)


# Public-knowledge canaries: if these records are wrong, the pipeline is
# broken no matter what the internal consistency checks say.
_CANARIES = [
    # (fighter, fight date, expected UFC record entering that night)
    ("Conor McGregor", "2021-07-10", (10, 3)),   # entering Poirier 3 at UFC 264
    ("Khabib Nurmagomedov", "2020-10-24", (12, 0)),  # entering Gaethje at UFC 254
    ("Israel Adesanya", "2022-11-12", (12, 1)),  # entering Pereira at UFC 281
]


def check_known_records(df: pd.DataFrame) -> Check:
    problems = []
    for name, date, (wins, losses) in _CANARIES:
        rows = df[(df["date"] == date) & ((df["f1_name"] == name) | (df["f2_name"] == name))]
        if len(rows) != 1:
            problems.append(f"{name} @ {date}: fight not found")
            continue
        feat = _corner_features(rows.iloc[0], name)
        if (feat["wins"], feat["losses"]) != (wins, losses):
            problems.append(f"{name} @ {date}: expected {wins}-{losses}, "
                            f"got {feat['wins']:.0f}-{feat['losses']:.0f}")
    return ("publicly-known records reproduce",
            not problems, "; ".join(problems) or f"{len(_CANARIES)} canaries verified")


def _values_equal(a, b) -> bool:
    """Equality that treats NaN == NaN (parquet rows are full of NaN)."""
    if isinstance(a, float) and isinstance(b, float) and math.isnan(a) and math.isnan(b):
        return True
    return a == b


def check_symmetry(df: pd.DataFrame, n: int = 200) -> Check:
    """diff columns must equal f1 - f2, and the corner swap must invert cleanly."""
    diff_cols = [c for c in df.columns if c.startswith("diff_")]
    problems = []
    for _, row in df.sample(min(n, len(df)), random_state=0).iterrows():
        d = row.to_dict()
        for col in diff_cols:
            base = col[len("diff_"):]
            a, b = d[f"f1_{base}"], d[f"f2_{base}"]
            expected = (a - b) if pd.notna(a) and pd.notna(b) else None
            actual = d[col] if pd.notna(d[col]) else None
            if (expected is None) != (actual is None) or (
                    expected is not None and not math.isclose(expected, actual, abs_tol=1e-9)):
                problems.append(f"fight {d['fight_id']}: {col}")
        undone = swap_corners(swap_corners(d))
        if not all(_values_equal(undone[k], d[k]) for k in d):
            problems.append(f"fight {d['fight_id']}: swap not an involution")
    return ("differentials antisymmetric on real rows",
            not problems, "; ".join(problems[:3]) or f"{n} rows verified")


def check_chronological_splits(df: pd.DataFrame, train_end: str, valid_end: str) -> Check:
    train = df[df["date"] <= train_end]
    valid = df[(df["date"] > train_end) & (df["date"] <= valid_end)]
    test = df[df["date"] > valid_end]
    ok = (not len(set(train["fight_id"]) & set(valid["fight_id"]) & set(test["fight_id"]))
          and (len(train) == 0 or len(valid) == 0 or train["date"].max() < valid["date"].min())
          and (len(valid) == 0 or len(test) == 0 or valid["date"].max() < test["date"].min()))

    # Rematches across splits are legal but worth counting: the model has
    # "seen" these matchups. (Pair key ignores corner order.)
    def pairs(frame):
        return {frozenset((a, b)) for a, b in zip(frame["f1_name"], frame["f2_name"])}
    crossers = len(pairs(train) & (pairs(valid) | pairs(test)))
    return ("chronological split boundaries hold", ok,
            f"train {len(train)} / valid {len(valid)} / test {len(test)}; "
            f"{crossers} rematch pairs span train and later splits (informational)")


def check_odds_sane(df: pd.DataFrame) -> Check:
    """Odds must be usable — knowing what they ARE, not what we wish.

    betmma.tips records the best available line across books, so the
    overround sits near 1.0 (median ~1.01) and 24% of fights sum below 1
    (cross-book arbitrage baked in). Vig-free normalization handles that for
    market probabilities, but the M6 backtest MUST disclose that betting at
    best-available prices inflates simulated ROI vs. a single book.
    Bounds here are the observed envelope of the source, not standard vig.
    """
    priced = df[df["f1_odds"].notna() & df["f2_odds"].notna()]
    overround = 1 / priced["f1_odds"] + 1 / priced["f2_odds"]
    bad = priced[(priced["f1_odds"] <= 1) | (priced["f2_odds"] <= 1)
                 | ~overround.between(0.75, 1.20)]
    return ("odds are finite, >1, within the source's overround envelope",
            len(bad) == 0,
            f"{len(priced)} priced fights; overround range "
            f"[{overround.min():.3f}, {overround.max():.3f}]; "
            f"{(overround < 1).mean():.0%} below 1.0 (best-line odds source)"
            + (f"; {len(bad)} bad rows" if len(bad) else ""))


def check_no_leaky_columns(df: pd.DataFrame) -> Check:
    """Current-fight outputs must never appear as inputs.

    Rolling aggregates carry a window suffix (_l3/_l5); a bare stat column
    (e.g. f1_sig_landed) would mean someone joined the fight's own stats in.
    Same for the scrape-time snapshot_* career averages.
    """
    allowed_bare = {"f1_name", "f2_name", "f1_odds", "f2_odds"}
    leaky = [c for c in df.columns
             if ("snapshot" in c)
             or (c.startswith(("f1_", "f2_")) and c not in allowed_bare
                 and any(tok in c for tok in ("sig_landed", "sig_attempted", "td_landed",
                                              "knockdowns", "ctrl_seconds", "sub_attempts"))
                 and not c.endswith(("_l3", "_l5")))]
    return ("no current-fight or snapshot columns leaked in",
            not leaky, "; ".join(leaky) or "column scan clean")


def run_audit(conn: sqlite3.Connection, df: pd.DataFrame,
              train_end: str, valid_end: str) -> list[Check]:
    return [
        check_records_vs_sql(conn, df),
        check_known_records(df),
        check_symmetry(df),
        check_chronological_splits(df, train_end, valid_end),
        check_odds_sane(df),
        check_no_leaky_columns(df),
    ]

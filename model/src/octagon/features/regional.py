"""Pre-UFC regional record features, point-in-time on Sherdog rows."""

import re
import sqlite3
from datetime import date as date_type

# Feeder and major promotions — strength-of-schedule proxy outside the UFC.
_MAJOR_ORG = re.compile(
    r"\b(Cage Warriors|CW \d|LFA|Legacy Fighting|RFA|Resurrection Fighting|"
    r"Bellator|PFL|Professional Fighters League|ONE Championship|ONE FC|ONE Friday|"
    r"Rizin|KSW|Brave CF|Brave Combat|Oktagon|ACA|ACB|Absolute Championship|"
    r"UAE Warriors|Titan FC|Fury FC|Fury Fighting|iKon|CFFC|Cage Fury|Invicta|"
    r"Contender Series|DWCS|Road to UFC|M-1|Jungle Fight|Shooto|Pancrase|"
    r"Deep|World Series of Fighting|WSOF|Strikeforce|Pride|Dream|EliteXC|"
    r"Affliction|Cage Rage|BAMMA|Combate|Ares FC|Hexagone|Fight Nights|"
    r"Eagle FC|Gladiator Challenge|King of the Cage|KOTC|Tachi Palace|TPF|"
    r"Xtreme Fighting|XFC|Shogun Fights|Unified MMA|TKO|Sengoku|Konfrontacja|"
    r"Future FC|Standout Fighting|SFT|Serbian Battle|SBC|FEN|Babilon|"
    r"Levels Fight League|LFL|Cage Fighting Championship|FightWorld|Naiza|"
    r"Octagon League|Real Fight Arena|Superior Challenge|BRAVE|Fusion Fight League)\b",
    re.IGNORECASE)

_FINISHES = ("KO/TKO", "SUB")

# Regional Elo vs an org-quality proxy (the regional graph is too sparse
# to rate opponents individually). Only fights dated before the snapshot.
_REGIONAL_K = 40.0
_REGIONAL_INITIAL = 1500.0
_MAJOR_OPP_ELO = 1550.0
_DEFAULT_OPP_ELO = 1450.0
_AMATEUR_OPP_ELO = 1350.0


def load_regional(conn: sqlite3.Connection) -> dict[str, dict]:
    """Load regional fight records indexed by normalized fighter name.

    Returns: {normalize_name(fighter_name): {fight records list}}
    """
    from octagon.db.parsing import normalize_name

    regional = {}
    try:
        conn.row_factory = sqlite3.Row
        for row in conn.execute(
                "SELECT fighter_name, date, opponent, result, method, org, is_amateur "
                "FROM regional_fights"):
            norm_key = normalize_name(row["fighter_name"])
            if norm_key not in regional:
                regional[norm_key] = []
            regional[norm_key].append({
                "date": row["date"],
                "opponent": row["opponent"],
                "result": row["result"],
                "method": row["method"],
                "org": row["org"],
                "is_amateur": row["is_amateur"],
            })
    except sqlite3.OperationalError:
        # Table doesn't exist yet (fresh DB before load-regional)
        pass

    return regional


def _days_between(earlier_iso: str, later_iso: str) -> float:
    return float((date_type.fromisoformat(later_iso)
                  - date_type.fromisoformat(earlier_iso)).days)


def _opp_elo(fight: dict) -> float:
    """Opponent-quality proxy from promotion pedigree, not the other name."""
    if fight.get("is_amateur"):
        return _AMATEUR_OPP_ELO
    if _MAJOR_ORG.search(fight.get("org") or ""):
        return _MAJOR_OPP_ELO
    return _DEFAULT_OPP_ELO


def regional_elo(regional_fights: list[dict], on_date: str) -> float | None:
    """Pre-fight regional Elo, or None when there is no history before on_date."""
    from octagon.features.elo import expected_score

    pre = sorted((f for f in regional_fights if f["date"] < on_date),
                 key=lambda f: f["date"])
    rating = _REGIONAL_INITIAL
    scored = 0
    for fight in pre:
        result = fight.get("result")
        if result not in ("win", "loss", "draw"):
            continue
        actual = {"win": 1.0, "loss": 0.0, "draw": 0.5}[result]
        expected = expected_score(rating, _opp_elo(fight))
        rating = rating + _REGIONAL_K * (actual - expected)
        scored += 1
    return rating if scored else None


def _streak(results: list[str]) -> int:
    """Consecutive wins (+) or losses (-) at the end of a chronological list."""
    streak = 0
    for result in reversed(results):
        if result == "win" and streak >= 0:
            streak += 1
        elif result == "loss" and streak <= 0:
            streak -= 1
        else:
            break
    return streak


def regional_snapshot(
    regional_fights: list[dict],
    on_date: str,
) -> dict[str, float | int | None]:
    """Compute pre-UFC stats from regional fights BEFORE on_date.

    Every key is present on every call (None when there is no history) so
    the f1/f2 snapshots always carry identical columns.
    """
    pre_debut = sorted((f for f in regional_fights if f["date"] < on_date),
                       key=lambda f: f["date"])

    wins = sum(1 for f in pre_debut if f["result"] == "win")
    losses = sum(1 for f in pre_debut if f["result"] == "loss")
    draws = sum(1 for f in pre_debut if f["result"] == "draw")
    total = wins + losses + draws

    finishes = sum(1 for f in pre_debut if f["method"] in _FINISHES)
    finish_rate = finishes / total if total > 0 else None

    # Bayesian-smoothed win percentage (same method as context.py)
    win_pct = (wins + 0.5) / (total + 1.0) if total > 0 else 0.5

    amateur_bouts = sum(1 for f in pre_debut if f["is_amateur"])

    empty = {
        "pre_ufc_wins": wins if wins > 0 else None,
        "pre_ufc_losses": losses if losses > 0 else None,
        "pre_ufc_draws": draws if draws > 0 else None,
        "pre_ufc_fights": total if total > 0 else None,
        "pre_ufc_finish_rate": finish_rate,
        "pre_ufc_win_pct": win_pct if total > 0 else None,
        "pre_ufc_amateur_bouts": amateur_bouts if amateur_bouts > 0 else None,
        "pre_ufc_ko_rate": None,
        "pre_ufc_sub_rate": None,
        "pre_ufc_finish_loss_rate": None,
        "pre_ufc_streak": None,
        "pre_ufc_layoff_days": None,
        "pre_ufc_fights_24m": None,
        "pre_ufc_career_years": None,
        "pre_ufc_major_org_share": None,
        "pre_ufc_elo": None,
    }
    if total == 0:
        return empty

    ko_wins = sum(1 for f in pre_debut if f["result"] == "win" and f["method"] == "KO/TKO")
    sub_wins = sum(1 for f in pre_debut if f["result"] == "win" and f["method"] == "SUB")
    finish_losses = sum(1 for f in pre_debut
                        if f["result"] == "loss" and f["method"] in _FINISHES)
    major = sum(1 for f in pre_debut if _MAJOR_ORG.search(f.get("org") or ""))
    return empty | {
        "pre_ufc_ko_rate": ko_wins / total,
        "pre_ufc_sub_rate": sub_wins / total,
        "pre_ufc_finish_loss_rate": finish_losses / total,
        "pre_ufc_streak": float(_streak([f["result"] for f in pre_debut])),
        "pre_ufc_layoff_days": _days_between(pre_debut[-1]["date"], on_date),
        "pre_ufc_fights_24m": float(sum(
            1 for f in pre_debut if _days_between(f["date"], on_date) <= 730)),
        "pre_ufc_career_years": _days_between(pre_debut[0]["date"], on_date) / 365.25,
        "pre_ufc_major_org_share": major / total,
        "pre_ufc_elo": regional_elo(regional_fights, on_date),
    }


def career_snapshot(
    ufc_fights: list[tuple[str, str, str | None]],
    regional_fights: list[dict],
    on_date: str,
) -> dict[str, float | None]:
    """Whole-career view: UFC and regional fights merged chronologically.

    `ufc_fights` are (iso_date, result, method) triples from the fighter's
    UFC history; regional rows come straight from the DB. A debutant's
    career IS their regional record; a ten-fight UFC veteran's career adds
    the run that got them signed. The point is continuity — `n_fights` and
    `layoff_days` fall off a cliff to 0 / None at the debut line, and these
    columns do not, so a model can treat "0 UFC fights, 14 pro fights" as
    the different thing it is from "0 UFC fights, 3 pro fights".
    """
    merged = [(d, r, m) for d, r, m in ufc_fights if d < on_date]
    merged += [(f["date"], f["result"], f["method"])
               for f in regional_fights if f["date"] < on_date]
    merged.sort(key=lambda t: t[0])
    keys = ("career_n_fights", "career_wins", "career_losses", "career_win_pct",
            "career_streak", "career_finish_rate", "career_finished_rate",
            "career_layoff_days", "career_fights_24m", "career_years")
    if not merged:
        return dict.fromkeys(keys)

    results = [r for _, r, _ in merged]
    wins = results.count("win")
    losses = results.count("loss")
    decisive = wins + losses
    n = float(len(merged))
    return {
        "career_n_fights": n,
        "career_wins": float(wins),
        "career_losses": float(losses),
        # Laplace-smoothed so a 2-0 is not the same 1.000 as a 20-0.
        "career_win_pct": (wins + 1.0) / (decisive + 2.0),
        "career_streak": float(_streak(results)),
        "career_finish_rate": sum(1 for _, r, m in merged
                                  if r == "win" and m in _FINISHES) / n,
        "career_finished_rate": sum(1 for _, r, m in merged
                                    if r == "loss" and m in _FINISHES) / n,
        "career_layoff_days": _days_between(merged[-1][0], on_date),
        "career_fights_24m": float(sum(
            1 for d, _, _ in merged if _days_between(d, on_date) <= 730)),
        "career_years": _days_between(merged[0][0], on_date) / 365.25,
    }

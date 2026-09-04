"""Grade a frozen card against results in the database.

Reads `reports/card_predictions_<card>.parquet` rather than refitting.
A twelve-fight hit count is noise without the base-rate comparison.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from octagon.config import resolve_path
from octagon.eval import metrics
from octagon.models import finish_round
from octagon.scraping.fighters import _same_person, _tokens

GROUP = {"KO/TKO": "ko", "SUB": "sub", "U-DEC": "dec", "S-DEC": "dec", "M-DEC": "dec"}


def frozen_path(card_stem: str) -> Path:
    return resolve_path("reports") / f"card_predictions_{card_stem}.parquet"


def actual_results(conn, date: str) -> list[dict]:
    """Every fight on that date from the database."""
    out = []
    for row in conn.execute("SELECT * FROM fights WHERE date = ?", (date,)):
        out.append({"fighter1": row["fighter1"], "fighter2": row["fighter2"],
                    "winner": row["winner"], "method": row["method"],
                    "end_round": row["end_round"]})
    return out


def _surname(name: str) -> str:
    tokens = _tokens(name)
    return tokens[-1] if tokens else ""


def match_result(results: list[dict], f1: str,
                 f2: str) -> tuple[dict | None, str | None]:
    """Find the DB result for a card bout, and say which corner is the card's f1.

    Cards often carry the legal name ('Nina Nikolija Milošević') while
    ufcstats drops the middle ('Nina Milosevic'). Exact normalize_name
    keys miss those and the scorecard quietly reports 'did not take place'.

    A second kind of drift needs a looser net: ufcstats sometimes carries the
    name a fighter competes under rather than the one on the card ('Gigi
    Canuto' for 'Giovanna Canuto'), where the surnames agree but neither set
    of given names contains the other. Falling back to surnames alone would
    be reckless on its own, so it applies only when it identifies exactly one
    bout on the night — two fights on one card sharing both surnames is not a
    thing that happens, and requiring uniqueness means a wrong guess can't
    quietly outrank a real match.

    Returns (result, corner) where corner is the DB field ('fighter1' or
    'fighter2') holding the card's f1, so callers never have to re-derive the
    orientation by comparing names that already needed fuzzy matching once.
    """
    for result in results:
        if _same_person(result["fighter1"], f1) and _same_person(result["fighter2"], f2):
            return result, "fighter1"
        if _same_person(result["fighter1"], f2) and _same_person(result["fighter2"], f1):
            return result, "fighter2"

    surnames = {_surname(f1), _surname(f2)}
    if "" in surnames or len(surnames) < 2:
        return None, None
    candidates = [r for r in results
                  if {_surname(r["fighter1"]), _surname(r["fighter2"])} == surnames]
    if len(candidates) != 1:
        return None, None
    result = candidates[0]
    corner = "fighter1" if _surname(result["fighter1"]) == _surname(f1) else "fighter2"
    return result, corner


def outcome_column(result: dict, f1_corner: str) -> str | None:
    """Which cell of the 22-outcome joint distribution actually happened.

    Oriented to the *card's* corner order, which need not match ufcstats' —
    `f1_corner` is the DB field holding the card's f1, as resolved by
    `match_result`.
    """
    group = GROUP.get(result["method"] or "")
    if group is None or result["winner"] not in ("fighter1", "fighter2"):
        return None
    corner = "f1" if result["winner"] == f1_corner else "f2"
    return f"{corner}_dec" if group == "dec" else \
        f"{corner}_{group}_r{int(result['end_round'])}"


def base_rate_joint(conn, date: str) -> dict[int, dict[str, float]]:
    """What a no-opinion forecaster would say, per scheduled-round length.

    A coin flip on the winner times the era's observed method mix and round
    splits, read from the fights table rather than the feature frame so
    grading never has to rebuild features.
    """
    rows = conn.execute(
        "SELECT scheduled_rounds, method, end_round FROM fights "
        "WHERE date < ? AND winner IN ('fighter1','fighter2') AND method IS NOT NULL",
        (date,)).fetchall()

    tallies: dict[int, dict[str, float]] = {}
    for row in rows:
        group = GROUP.get(row["method"])
        scheduled = row["scheduled_rounds"]
        if group is None or not scheduled:
            continue
        bucket = tallies.setdefault(int(scheduled), {})
        key = "dec" if group == "dec" else f"{group}_r{int(row['end_round'] or 1)}"
        bucket[key] = bucket.get(key, 0.0) + 1.0

    out = {}
    for scheduled, bucket in tallies.items():
        total = sum(bucket.values())
        joint = dict.fromkeys(finish_round.outcome_columns(), 0.0)
        for key, count in bucket.items():
            share = count / total / 2.0        # split evenly across corners
            if key == "dec":
                joint["f1_dec"] = joint["f2_dec"] = share
            else:
                group, rnd = key.split("_r")
                if int(rnd) <= scheduled:
                    joint[f"f1_{group}_r{rnd}"] = joint[f"f2_{group}_r{rnd}"] = share
        scale = sum(joint.values())
        out[scheduled] = {k: v / scale for k, v in joint.items()} if scale else joint
    return out


def grade(conn, frame: pd.DataFrame, abstain: tuple[float, float]) -> dict:
    """Score frozen predictions against results. Pure data, no rendering."""
    date = str(frame["date"].iat[0])
    results = actual_results(conn, date)
    base_by_length = base_rate_joint(conn, date)
    columns = finish_round.outcome_columns()

    fights, skipped = [], []
    for _, saved in frame.iterrows():
        f1, f2 = saved["f1_name"], saved["f2_name"]
        result, f1_corner = match_result(results, f1, f2)
        if result is None or result["winner"] not in ("fighter1", "fighter2"):
            skipped.append({"f1": f1, "f2": f2,
                            "status": "no decisive result on record" if result
                                      else "did not take place"})
            continue

        p = float(saved["p_f1_wins"])
        winner = result[result["winner"]]
        label = float(result["winner"] == f1_corner)
        column = outcome_column(result, f1_corner)
        joint = {c: float(saved[c]) for c in columns}
        base = base_by_length.get(int(saved["scheduled_rounds"] or 3), {})

        called_group = called_method(joint)
        true_group = GROUP.get(result["method"] or "")

        modal_round = None
        if column and not column.endswith("_dec"):
            channel = column.rsplit("_r", 1)[0]
            block = [joint[f"{channel}_r{r}"] for r in finish_round.ROUNDS]
            modal_round = finish_round.ROUNDS[int(np.argmax(block))]

        fights.append({
            "f1": f1, "f2": f2,
            "weight_class": saved.get("weight_class"),
            "scheduled_rounds": int(saved["scheduled_rounds"] or 3),
            "p_f1_wins": p,
            "pick": f1 if p >= 0.5 else f2,
            "confidence": max(p, 1.0 - p),
            "called": not (abstain[0] <= p <= abstain[1]),
            "winner": winner,
            "method": result["method"],
            "end_round": (int(result["end_round"])
                          if result["end_round"] is not None else None),
            "correct": bool((p > 0.5) == (label == 1.0)),
            "log_loss": float(-(label * np.log(max(p, 1e-12))
                                + (1 - label) * np.log(max(1 - p, 1e-12)))),
            "method_called": called_group,
            "method_correct": called_group == true_group,
            "modal_round": modal_round,
            "round_correct": (None if modal_round is None
                              else modal_round == int(result["end_round"])),
            "p_actual": joint.get(column) if column else None,
            "p_actual_base": base.get(column) if column else None,
            "label": label,
        })

    return {"date": date,
            "event": str(frame["event"].iat[0]) if "event" in frame else "",
            "fights": fights, "skipped": skipped,
            "aggregates": _aggregates(fights)}


def called_method(joint: dict[str, float]) -> str:
    """The method family the card called: finish vs decision first.

    KO and submission split a finish's probability. Taking argmax over
    {ko, sub, dec} therefore calls a decision whenever the finish mass is
    split 35/20 against a 45% decision — which is how a night of knockouts
    gets scored as 'said dec'. Ask 'does it finish?' first, then how.
    """
    ko, sub, dec = (_marginal(joint, "ko"), _marginal(joint, "sub"),
                    _marginal(joint, "dec"))
    if ko + sub >= dec:
        return "ko" if ko >= sub else "sub"
    return "dec"


def _marginal(joint: dict[str, float], group: str) -> float:
    if group == "dec":
        return joint["f1_dec"] + joint["f2_dec"]
    return sum(joint[f"{c}_{group}_r{r}"]
               for c in ("f1", "f2") for r in finish_round.ROUNDS)


def _aggregates(fights: list[dict]) -> dict:
    if not fights:
        return {}
    y = np.array([f["label"] for f in fights])
    p = np.array([f["p_f1_wins"] for f in fights])
    correct = np.array([f["correct"] for f in fights])
    called = np.array([f["called"] for f in fights])
    rounds = [f["round_correct"] for f in fights if f["round_correct"] is not None]
    actual = np.array([f["p_actual"] for f in fights if f["p_actual"] is not None])
    base = np.array([f["p_actual_base"] for f in fights
                     if f["p_actual_base"] is not None])
    return {
        "n": len(fights),
        "winners_correct": int(correct.sum()),
        "accuracy": float(correct.mean()),
        "n_called": int(called.sum()),
        "called_correct": int(correct[called].sum()) if called.any() else 0,
        "called_accuracy": float(correct[called].mean()) if called.any() else None,
        "log_loss": metrics.log_loss(y, p),
        "brier": metrics.brier(y, p),
        "method_correct": int(sum(f["method_correct"] for f in fights)),
        "round_correct": int(sum(rounds)),
        "n_finishes": len(rounds),
        "mean_p_actual": float(actual.mean()) if len(actual) else None,
        "mean_p_actual_base": float(base.mean()) if len(base) else None,
    }


def load_or_refit(conn, card_path: Path, artifact: dict, cfg: dict):
    """The frozen predictions if we have them, otherwise a fresh refit."""
    path = frozen_path(card_path.stem)
    if path.exists():
        return pd.read_parquet(path), True
    from octagon.predict import card_predictions, predictions_frame
    return predictions_frame(card_predictions(conn, card_path, artifact, cfg)), False


def score_card(conn, card_path: Path, artifact: dict, cfg: dict) -> str:
    frame, frozen = load_or_refit(conn, card_path, artifact, cfg)
    graded = grade(conn, frame, (cfg["abstain"]["low"], cfg["abstain"]["high"]))
    if not graded["fights"]:
        return (f"# {graded['event']} — {graded['date']}\n\n"
                "No results in the database yet.")
    return render(graded, frozen)


def render(graded: dict, frozen: bool) -> str:
    a = graded["aggregates"]
    n = a["n"]
    lines = [
        f"# Scorecard — {graded['event']} ({graded['date']})",
        "",
        f"{a['winners_correct']} of {n} winners called correctly "
        f"({a['accuracy']:.0%}). Graded against ufcstats results.",
        "",
        "Probabilities are the frozen ones saved when the card was predicted."
        if frozen else
        "WARNING: no frozen prediction file for this card, so the models were "
        "refit on today's data. Source CSVs get revised and refits move "
        "individual fights by a point or two — treat these probabilities as "
        "an approximation of what was published.",
        "",
        "| fight | pick | P(pick) | actual | winner | method | round |",
        "|---|---|---|---|---|---|---|",
    ]
    for f in graded["fights"]:
        ending = (f"{f['method']} R{f['end_round']}"
                  if f["method"] and not str(f["method"]).endswith("DEC")
                  else str(f["method"]))
        method_mark = "hit" if f["method_correct"] else f"said {f['method_called']}"
        round_mark = "—" if f["modal_round"] is None else (
            "hit" if f["round_correct"] else f"said R{f['modal_round']}")
        lines.append(
            f"| {f['f1']} vs. {f['f2']} | {f['pick']} | {f['confidence']:.0%}"
            + ("" if f["called"] else " *(no call)*")
            + f" | {f['winner']}, {ending} | {'✓' if f['correct'] else '✗'} "
            f"| {method_mark} | {round_mark} |")
    for s in graded["skipped"]:
        lines.append(f"| {s['f1']} vs. {s['f2']} | — | — | {s['status']} | — | — | — |")

    lines += [
        "",
        "## Aggregates",
        "",
        "| metric | model | no-skill reference |",
        "|---|---|---|",
        f"| winners correct | {a['winners_correct']}/{n} ({a['accuracy']:.0%}) "
        f"| {n / 2:.1f}/{n} (50%) |",
        f"| winners correct, excluding no-calls | {a['called_correct']}/{a['n_called']} "
        f"({a['called_accuracy']:.0%}) | {a['n_called'] / 2:.1f}/{a['n_called']} (50%) |",
        f"| log loss (winner) | {a['log_loss']:.4f} | 0.6931 |",
        f"| Brier (winner) | {a['brier']:.4f} | 0.2500 |",
        f"| method called (KO/sub/dec) | {a['method_correct']}/{n} "
        f"({a['method_correct'] / n:.0%}) | — |",
        f"| round called, given fighter + method | {a['round_correct']}/{a['n_finishes']} "
        f"| — |",
        f"| mean P(exact outcome) | {a['mean_p_actual']:.3f} "
        f"| {a['mean_p_actual_base']:.3f} (base rate) |",
        "",
        "P(exact outcome) is the probability assigned to the fighter × method × "
        "round that actually happened, vs a coin flip times the historical mix.",
    ]
    return "\n".join(lines)

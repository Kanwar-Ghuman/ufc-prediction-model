"""Upcoming-card predictions (M7, PRD Phase E).

ufcstats.com's upcoming pages sit behind the same bot wall as the rest of
the site, so the card comes from a small YAML file you write by hand (see
cards/example_card.yaml). Everything else is automatic: point-in-time
features as of the card date, fresh models fit on all history before it,
calibrated + blended probabilities, SHAP explanations, market gap when you
provide odds, and the abstain band from config.

The models are refit at predict time (seconds) rather than loaded from the
artifact: the artifact's final model stops at train_end (2021) by design,
and a 2026 card deserves everything the pipeline knows through last month.
The artifact still supplies what tuning legitimately chose: the GBM
hyperparameters, the calibration map, and the blend weight.
"""

from dataclasses import dataclass
from pathlib import Path

import yaml

from octagon.betting.odds import implied_probability, remove_vig
from octagon.features.build import Bout, build_feature_rows, load_bouts, load_tott


@dataclass
class CardFight:
    fighter1: str
    fighter2: str
    weight_class: str | None = None
    title_fight: bool = False
    rounds: int = 3
    odds: tuple[float, float] | None = None


def load_card(path: Path) -> tuple[str, str, list[CardFight]]:
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    fights = [CardFight(
        fighter1=f["fighter1"], fighter2=f["fighter2"],
        weight_class=f.get("weight_class"), title_fight=bool(f.get("title_fight")),
        rounds=int(f.get("rounds", 3)),
        odds=tuple(f["odds"]) if f.get("odds") else None,
    ) for f in raw["fights"]]
    return str(raw["date"]), raw.get("event", "Upcoming card"), fights


def predict_card(conn, card_path: Path, artifact: dict, cfg: dict) -> str:
    import pandas as pd

    from octagon.eval import explain
    from octagon.models import calibration, ensemble, gbm, logistic, method

    date, event, card = load_card(card_path)
    bouts = [b for b in load_bouts(conn) if b.date < date]
    for i, f in enumerate(card):
        bouts.append(Bout(
            fight_id=-(i + 1), date=date, fighter1=f.fighter1, fighter2=f.fighter2,
            winner="upcoming", method=None, end_round=None, duration_s=None,
            weight_class=f.weight_class, title_fight=int(f.title_fight),
            scheduled_rounds=f.rounds, stats1=None, stats2=None,
            odds1=f.odds[0] if f.odds else None, odds2=f.odds[1] if f.odds else None,
        ))

    df = pd.DataFrame(build_feature_rows(bouts, load_tott(conn), elo_k=cfg["elo"]["k_factor"],
                                         seed=cfg["seed"]))
    history = df[df["label"].notna()]
    upcoming = df[df["label"].isna()]

    gbm_model = gbm.fit(history, artifact["params"], seed=artifact["seed"])
    lr_model = logistic.fit(history)
    p_gbm = calibration.apply(artifact["iso"], gbm.predict_sym(gbm_model, upcoming))
    p_lr = logistic.predict(lr_model, upcoming)
    p = ensemble.blend(p_lr, p_gbm, artifact["weight_lr"])

    # Method of victory: this model decides only the HOW; the blend's win
    # probability stays canonical (see method.condition_on_win_prob).
    method_model = method.fit(history, artifact["params"], seed=artifact["seed"])
    methods = method.condition_on_win_prob(
        method.predict_sym(method_model, upcoming), p)

    low, high = cfg["abstain"]["low"], cfg["abstain"]["high"]
    lines = [
        f"# {event} — {date}",
        "",
        f"Point-in-time predictions from {len(history)} historical fights. "
        "Educational output — NOT betting advice; the backtest shows this "
        "model does not beat the market.",
        "",
    ]
    for i, (idx, row) in enumerate(upcoming.iterrows()):
        prob = float(p[i])
        f1, f2 = row["f1_name"], row["f2_name"]
        pick = f1 if prob >= 0.5 else f2
        call = ("NO CALL (abstain band)" if low <= prob <= high
                else f"pick: {pick} ({max(prob, 1 - prob):.0%})")
        lines += [f"## {f1} vs. {f2}"
                  + (f" — {row['weight_class']}" if row["weight_class"] else ""),
                  f"P({f1} wins) = {prob:.3f}  ->  {call}"]

        for name, n_fights in [(f1, row["f1_n_fights"]), (f2, row["f2_n_fights"])]:
            if n_fights == 0:
                lines.append(f"- CAUTION: no UFC history for {name} "
                             "(debut or misspelled name?) — prediction is weak.")
        if row["f1_odds"] is not None and not pd.isna(row["f1_odds"]):
            fair1, _ = remove_vig(implied_probability(row["f1_odds"]),
                                  implied_probability(row["f2_odds"]))
            lines.append(f"- market (vig-free): P({f1}) = {fair1:.3f}; "
                         f"model - market = {prob - fair1:+.3f}")

        m = methods.loc[idx]
        lines.append(
            f"- method: {f1} by KO {m['f1_ko']:.0%} / sub {m['f1_sub']:.0%} / "
            f"dec {m['f1_dec']:.0%}; {f2} by KO {m['f2_ko']:.0%} / "
            f"sub {m['f2_sub']:.0%} / dec {m['f2_dec']:.0%}")

        contributions, _ = explain.shap_symmetrized(gbm_model, upcoming.loc[[idx]])
        top = contributions.iloc[0].sort_values(key=abs, ascending=False).head(5)
        drivers = ", ".join(f"{name} {value:+.2f}" for name, value in top.items()
                            if abs(value) > 1e-3)
        lines += [f"- drivers (log-odds): {drivers}", ""]

    lines += ["---", "*Simulation/educational project. No betting advice. "
              "The market knows more than this model.*"]
    return "\n".join(lines)

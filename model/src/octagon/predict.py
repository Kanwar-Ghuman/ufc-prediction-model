"""Upcoming-card predictions.

Cards come from `octagon fetch-card` (Wikipedia) plus optional
`octagon fetch-odds`. Models are refit at predict time on all history before
the card date. The artifact supplies tuned hyperparameters, the calibration
map, and the blend weight — not a 2021-stopped final model.
"""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from octagon.betting.odds import implied_probability, remove_vig
from octagon.features.build import (Bout, build_feature_rows, elo_kwargs, load_bouts,
                                    load_tott)
from octagon.features.research import research_brief
from octagon.models.market import (
    apply_market_layer, apply_ranking_nudge, resolve_research_weight,
)


@dataclass
class CardFight:
    fighter1: str
    fighter2: str
    weight_class: str | None = None
    title_fight: bool = False
    rounds: int = 3
    odds: tuple[float, float] | None = None
    section: str | None = None  # 'Main card' / 'Preliminary card'; display only
    ranking: tuple[int, int] | None = None  # dual-debut skill nudge
    region: tuple[str, str] | None = None


def _optional_pair(value) -> tuple | None:
    if not value:
        return None
    first, second = value[0], value[1]
    return (first, second)


def load_card(path: Path) -> tuple[str, str, list[CardFight]]:
    with open(path, encoding="utf-8") as fh:
        raw = yaml.safe_load(fh)
    fights = [CardFight(
        fighter1=f["fighter1"], fighter2=f["fighter2"],
        weight_class=f.get("weight_class"), title_fight=bool(f.get("title_fight")),
        rounds=int(f.get("rounds", 3)),
        odds=tuple(f["odds"]) if f.get("odds") else None,
        section=f.get("section"),
        ranking=_optional_pair(f.get("ranking")),
        region=_optional_pair(f.get("region")),
    ) for f in raw["fights"]]
    return str(raw["date"]), raw.get("event", "Upcoming card"), fights


def pick_call(prob: float, f1: str, f2: str, low: float, high: float) -> str:
    """Decisive pick, or no-call when the shipped number sits in the dead zone."""
    pick = f1 if prob >= 0.5 else f2
    conf = max(prob, 1.0 - prob)
    if low <= prob <= high:
        return f"no call ({conf:.0%} lean {pick})"
    return f"pick: {pick} ({conf:.0%})"


def _ending_lines(joint_row, ending_row, f1: str, f2: str,
                  scheduled: int) -> tuple[list[str], list[str]]:
    """One fight's outcome distribution, as (headline bullets, grid).

    The headlines answer what a reader asks first — does this go the
    distance, and what is the single likeliest ending? The grid is the
    whole joint distribution behind those two sentences.
    """
    from octagon.models import finish_round

    rounds = [r for r in finish_round.ROUNDS if r <= scheduled]
    decision = float(joint_row["f1_dec"] + joint_row["f2_dec"])
    by_round = " / ".join(f"R{r} {ending_row[f'r{r}']:.0%}" for r in rounds)
    likeliest = ", ".join(
        f"{finish_round.describe(name, f1, f2)} ({value:.0%})"
        for name, value in joint_row.sort_values(ascending=False).head(3).items())
    headlines = [
        f"- how it ends: finish {1 - decision:.0%} ({by_round}) "
        f"vs. decision {decision:.0%}",
        f"- likeliest endings: {likeliest}",
    ]

    grid = ["| ending | " + " | ".join(f"R{r}" for r in rounds) + " | any round |",
            "|---" * (len(rounds) + 2) + "|"]
    for corner, name in (("f1", f1), ("f2", f2)):
        for group, label in (("ko", "KO/TKO"), ("sub", "submission")):
            cells = [float(joint_row[f"{corner}_{group}_r{r}"]) for r in rounds]
            grid.append(f"| {name} by {label} | "
                        + " | ".join(f"{v:.1%}" for v in cells)
                        + f" | **{sum(cells):.1%}** |")
    grid.append("| decision (either fighter) | " + " | ".join("—" for _ in rounds)
                + f" | **{decision:.1%}** |")
    return headlines, grid


@dataclass
class CardPrediction:
    """Everything the models say about one card, before any rendering.

    Kept separate from the markdown so the same numbers can be graded
    against results later (`octagon score-card`) without re-deriving them
    from a report — and so grading can never quietly use a different model
    than the prediction did.
    """

    date: str
    event: str
    upcoming: "object"        # DataFrame: one feature row per announced bout
    history: "object"         # DataFrame: every fight before the card
    win_prob: "object"        # ndarray: P(fighter1 wins), row-aligned — the
                              # market-aware stack where odds were provided,
                              # the skill blend elsewhere
    skill_prob: "object"      # ndarray: the skill-only blend, always
    market_prob: "object"     # ndarray: vig-free market P(f1), NaN if no odds
    methods: "object"         # DataFrame: 6 method classes
    joint: "object"           # DataFrame: fighter x method x round, sums to 1
    endings: "object"         # DataFrame: P(ends in round r) + P(decision)
    drivers: "object"         # DataFrame: SHAP log-odds contributions per bout
    card_order: dict          # fight_id -> position on the announced card
    sections: dict            # fight_id -> broadcast segment, when known
    renames: list[str]
    shap_model: "object"
    include_raw: bool
    context_notes: dict = field(default_factory=dict)  # bout idx -> notes
    context: object | None = None  # day-before scrape payload, if present


def card_predictions(conn, card_path: Path, artifact: dict, cfg: dict) -> CardPrediction:
    """Fit every model on history strictly before the card and predict it.

    Fights on or after the card date are excluded by construction, so this
    stays point-in-time even once the results are in the database.
    """
    import numpy as np
    import pandas as pd

    from octagon.db.parsing import normalize_name
    from octagon.models import calibration, ensemble, finish_round, gbm, logistic, method

    date, event, card = load_card(card_path)
    bouts = [b for b in load_bouts(conn) if b.date < date]

    known: dict[str, str] = {}
    for b in bouts:
        known.setdefault(normalize_name(b.fighter1), b.fighter1)
        known.setdefault(normalize_name(b.fighter2), b.fighter2)
    renames = []
    for f in card:
        for attr in ("fighter1", "fighter2"):
            name = getattr(f, attr)
            match = known.get(normalize_name(name))
            if match and match != name:
                renames.append(f"{name} -> {match}")
                setattr(f, attr, match)

    for i, f in enumerate(card):
        bouts.append(Bout(
            fight_id=-(i + 1), date=date, fighter1=f.fighter1, fighter2=f.fighter2,
            winner="upcoming", method=None, end_round=None, duration_s=None,
            weight_class=f.weight_class, title_fight=int(f.title_fight),
            scheduled_rounds=f.rounds, stats1=None, stats2=None,
            odds1=f.odds[0] if f.odds else None, odds2=f.odds[1] if f.odds else None,
        ))

    from octagon.features.regional import load_regional

    df = pd.DataFrame(build_feature_rows(
        bouts, load_tott(conn), regional_by_name=load_regional(conn),
        seed=cfg["seed"], **elo_kwargs(cfg)))
    history = df[df["label"].notna()]
    upcoming = df[df["label"].isna()]

    raw_flag = artifact.get("include_raw", False)
    n_seeds = artifact.get("n_seeds", 1)
    gbm_model = gbm.fit(history, artifact["params"], seed=artifact["seed"],
                        include_raw=raw_flag, n_seeds=n_seeds)
    shap_model = gbm_model.members[0] if hasattr(gbm_model, "members") else gbm_model
    lr_model = logistic.fit(history, C=artifact.get("lr_C", 1.0),
                            half_life_years=artifact.get("lr_half_life"), as_of=date)
    p_gbm = calibration.apply(artifact["iso"],
                              gbm.predict_sym(gbm_model, upcoming, include_raw=raw_flag))
    p_lr = logistic.predict(lr_model, upcoming)
    p_skill = ensemble.blend(p_lr, p_gbm, artifact["weight_lr"])

    if artifact.get("debut_model") is not None and artifact.get("debut_stack") is not None:
        from octagon.models import debut
        from octagon.models import debut_stack as debut_stack_model

        low_hist = debut.low_history_mask(upcoming).to_numpy()
        if low_hist.any():
            p_debut = debut.predict_sym(artifact["debut_model"], upcoming,
                                        include_raw=raw_flag)
            d_a, d_b = artifact["debut_stack"]
            p_stacked = debut_stack_model.predict_stack(d_a, d_b, p_skill, p_debut)
            p_skill = np.where(low_hist, p_stacked, p_skill)

    context_notes: dict[int, list[str]] = {}
    for i, fight in enumerate(card):
        if not fight.ranking:
            continue
        row = upcoming.iloc[i]
        adjusted, note = apply_ranking_nudge(
            float(p_skill[i]), fight.ranking[0], fight.ranking[1],
            float(row["f1_n_fights"] or 0), float(row["f2_n_fights"] or 0))
        p_skill[i] = adjusted
        if note:
            context_notes.setdefault(i, []).append(note)

    fair = np.full(len(upcoming), np.nan)
    for i, (_, row) in enumerate(upcoming.iterrows()):
        if row["f1_odds"] is not None and not pd.isna(row["f1_odds"]):
            fair[i], _ = remove_vig(implied_probability(row["f1_odds"]),
                                    implied_probability(row["f2_odds"]))
    p, trapped = apply_market_layer(
        p_skill, fair,
        upcoming["f1_n_fights"].to_numpy(), upcoming["f2_n_fights"].to_numpy(),
        stack=artifact.get("market_stack"),
        research_weight=resolve_research_weight(artifact, cfg),
        career1=upcoming["f1_career_n_fights"].to_numpy(),
        career2=upcoming["f2_career_n_fights"].to_numpy())
    for i in np.flatnonzero(trapped):
        context_notes.setdefault(int(i), []).append(
            f"market-trap guard: skill={float(p_skill[i]):.2f} but market="
            f"{float(fair[i]):.2f} on a debut bout — abstaining")

    context_payload = None
    try:
        from octagon.scraping import context as card_context

        context_payload = card_context.load_context(card_path)
        if context_payload:
            from octagon.db.parsing import normalize_name as _nn

            fighters_ctx = context_payload.get("fighters", {})
            bouts_ctx = {
                (b.get("f1_key"), b.get("f2_key")): b
                for b in context_payload.get("bouts", [])
            }
            for i, (_, row) in enumerate(upcoming.iterrows()):
                k1, k2 = _nn(row["f1_name"]), _nn(row["f2_name"])
                c1, c2 = fighters_ctx.get(k1, {}), fighters_ctx.get(k2, {})
                bout = bouts_ctx.get((k1, k2)) or bouts_ctx.get((k2, k1)) or {}
                yt = bout.get("youtube") or {}
                # Flip the lean if the context bout is stored f2-first.
                lean = yt.get("lean_f1")
                if lean is not None and bout.get("f1_key") == k2:
                    lean = -float(lean)
                adjusted, notes = card_context.soft_adjust_p_f1(
                    float(p[i]),
                    float(row["f1_n_fights"] or 0),
                    float(row["f2_n_fights"] or 0),
                    c1.get("pro_record"),
                    c2.get("pro_record"),
                    c1.get("circumstances"),
                    c2.get("circumstances"),
                    float(c1.get("sentiment") or 0.0),
                    float(c2.get("sentiment") or 0.0),
                    has_market_odds=bool(np.isfinite(fair[i])),
                    youtube_lean=None if lean is None else float(lean),
                    youtube_n_signals=int(yt.get("n_signals") or 0),
                    skill_p=float(p_skill[i]),
                )
                if notes:
                    p[i] = adjusted
                    context_notes.setdefault(i, []).extend(notes)
    except Exception:  # noqa: BLE001 — context is optional at predict time
        context_payload = None

    method_model = method.fit(history, seed=artifact["seed"],
                              include_raw=raw_flag)
    methods = method.condition_on_win_prob(
        method.blend(
            method.base_rate_methods(history, upcoming),
            method.predict_sym(method_model, upcoming, include_raw=raw_flag),
            artifact.get("weight_method_base", 0.0)),
        p)
    round_model = finish_round.fit(history, seed=artifact["seed"])
    rounds = finish_round.blend(
        finish_round.base_rate_rounds(history, upcoming),
        finish_round.predict_rounds(round_model, upcoming),
        artifact.get("weight_round_base", 0.5))
    joint = finish_round.joint_outcomes(methods, rounds)
    endings = finish_round.ending_summary(joint)

    from octagon.eval import explain

    drivers, _ = explain.shap_symmetrized(shap_model, upcoming, include_raw=raw_flag)

    return CardPrediction(
        date=date, event=event, upcoming=upcoming, history=history, win_prob=p,
        skill_prob=p_skill, market_prob=fair,
        methods=methods, joint=joint, endings=endings, drivers=drivers,
        card_order={-(i + 1): i for i in range(len(card))},
        sections={-(i + 1): f.section for i, f in enumerate(card)},
        renames=renames, shap_model=shap_model, include_raw=raw_flag,
        context_notes=context_notes, context=context_payload)


def top_drivers(contributions, top: int = 6) -> list[dict]:
    """The features that moved one bout most, largest absolute pull first."""
    ranked = contributions.sort_values(key=abs, ascending=False).head(top)
    return [{"feature": name, "value": round(float(value), 4)}
            for name, value in ranked.items() if abs(value) > 1e-3]


def predictions_frame(pred: CardPrediction):
    """One row per bout: identities, win probability, full outcome grid.

    Saved next to the report so `octagon score-card` grades the numbers that
    were actually published. Re-deriving them later is not the same thing —
    the source CSVs get revised and a refit moves individual fights by a
    couple of points, which is exactly the kind of drift that lets a
    post-hoc grade flatter itself.

    The card position, broadcast segment and SHAP drivers ride along so the
    website can show a card the way it was announced, and explain a pick,
    without re-running anything.
    """
    import json

    import pandas as pd

    frame = pred.upcoming[["f1_name", "f2_name", "weight_class",
                           "scheduled_rounds"]].copy()
    frame.insert(0, "date", pred.date)
    frame.insert(1, "event", pred.event)
    fight_ids = pred.upcoming["fight_id"]
    frame["bout_order"] = [pred.card_order.get(i, n)
                           for n, i in enumerate(fight_ids)]
    frame["section"] = [pred.sections.get(i) for i in fight_ids]
    for corner in ("f1", "f2"):
        frame[f"{corner}_ufc_fights"] = (
            pred.upcoming[f"{corner}_n_fights"].fillna(0).astype(int).to_numpy())
    frame["p_f1_wins"] = pred.win_prob
    frame["p_skill"] = pred.skill_prob
    frame["p_market"] = pred.market_prob
    frame["drivers"] = [json.dumps(top_drivers(pred.drivers.loc[idx]))
                        for idx in pred.upcoming.index]
    notes = pred.context_notes or {}
    ctx = pred.context or {}
    fighters_ctx = ctx.get("fighters", {}) if isinstance(ctx, dict) else {}
    bout_rows = []
    for i, (_, row) in enumerate(pred.upcoming.iterrows()):
        from octagon.db.parsing import normalize_name

        k1, k2 = normalize_name(row["f1_name"]), normalize_name(row["f2_name"])
        c1, c2 = fighters_ctx.get(k1, {}), fighters_ctx.get(k2, {})
        bout_rows.append({
            "adjustments": notes.get(i, []),
            "research": research_brief(row.to_dict(), row["f1_name"], row["f2_name"]),
            "f1": {
                "styles": c1.get("styles") or [],
                "pro_record": c1.get("pro_record"),
                "circumstances": c1.get("circumstances") or {},
                "sentiment": c1.get("sentiment"),
                "summary": (c1.get("summary") or "")[:400] or None,
                "headlines": (c1.get("headlines") or [])[:4],
            },
            "f2": {
                "styles": c2.get("styles") or [],
                "pro_record": c2.get("pro_record"),
                "circumstances": c2.get("circumstances") or {},
                "sentiment": c2.get("sentiment"),
                "summary": (c2.get("summary") or "")[:400] or None,
                "headlines": (c2.get("headlines") or [])[:4],
            },
        })
    frame["context"] = [json.dumps(b, ensure_ascii=False) for b in bout_rows]
    return pd.concat([frame.reset_index(drop=True),
                      pred.joint.reset_index(drop=True)], axis=1)


def _pro_record(name: str, cfg: dict) -> str | None:
    """A debutant's career record outside the UFC, if we know it.

    Sherdog first, ufc.com second. For a true debutant ufc.com's roster page
    is exactly the wrong source — it carries the fighter's UFC record, which
    is 0-0-0 until they have fought, so the caution line ended up telling
    the reader that a 19-3 regional champion had never won a fight. The
    Sherdog cache is the pre-UFC history the model itself is scoring on.
    Read-only: no network at predict time.
    """
    from octagon.config import resolve_path
    from octagon.scraping import fighters, sherdog

    data = cfg.get("data", {})
    regional = sherdog.lookup([name], resolve_path(
        data.get("sherdog_cache", "data/sherdog_records.json")))
    fights = (regional.get(name) or {}).get("regional_fights") or []
    if fights:
        wins = sum(1 for f in fights if f.get("result") == "win")
        losses = sum(1 for f in fights if f.get("result") == "loss")
        draws = sum(1 for f in fights if f.get("result") == "draw")
        return f"{wins}-{losses}-{draws}"

    record = fighters.lookup([name], resolve_path(
        data.get("media_path", "data/fighter_media.json"))
    ).get(name, {}).get("record")
    # '0-0-0' from ufc.com means "not yet fought in the UFC", not "no career".
    return None if record in (None, "0-0-0", "0-0") else record


def render_card(pred: CardPrediction, artifact: dict, cfg: dict) -> str:
    import pandas as pd

    date, event, upcoming = pred.date, pred.event, pred.upcoming
    p, methods, joint, endings = (pred.win_prob, pred.methods, pred.joint,
                                  pred.endings)
    renames = pred.renames
    history_size = len(pred.history)

    lines = [
        f"# {event} — {date}",
        "",
        f"Point-in-time predictions from {history_size} historical fights. "
        "Educational output — NOT betting advice; the backtest shows this "
        "model does not beat the market.",
        "",
    ]
    if renames:
        lines += ["Name spellings resolved against ufcstats: " + "; ".join(renames), ""]
    for i, (idx, row) in enumerate(upcoming.iterrows()):
        prob = float(p[i])
        f1, f2 = row["f1_name"], row["f2_name"]
        band = cfg.get("abstain") or {}
        call = pick_call(prob, f1, f2,
                         float(band.get("low", 0.42)),
                         float(band.get("high", 0.58)))
        lines += [f"## {f1} vs. {f2}"
                  + (f" — {row['weight_class']}" if row["weight_class"] else ""),
                  f"P({f1} wins) = {prob:.3f}  ->  {call}"]

        for name, n_fights in [(f1, row["f1_n_fights"]), (f2, row["f2_n_fights"])]:
            if n_fights == 0:
                pro = _pro_record(name, cfg)
                context = (f" Pro record outside the UFC: {pro}."
                           if pro else "")
                lines.append(f"- CAUTION: no UFC history for {name} "
                             f"(debut or misspelled name?) — prediction is "
                             f"weak.{context}")
        for note in (pred.context_notes or {}).get(i, []):
            lines.append(f"- context: {note}")
        for note in research_brief(row.to_dict(), f1, f2):
            lines.append(f"- research: {note}")
        fair1, skill1 = float(pred.market_prob[i]), float(pred.skill_prob[i])
        if not pd.isna(fair1):
            lines.append(f"- skill-only research model P({f1}) = {skill1:.3f}; "
                         f"vig-free market = {fair1:.3f} "
                         f"(gap {skill1 - fair1:+.3f}). "
                         f"Shipped number mixes both; deeper UFC history "
                         f"weights the research model more.")

        m = methods.loc[idx]
        lines.append(
            f"- method: {f1} by KO {m['f1_ko']:.0%} / sub {m['f1_sub']:.0%} / "
            f"dec {m['f1_dec']:.0%}; {f2} by KO {m['f2_ko']:.0%} / "
            f"sub {m['f2_sub']:.0%} / dec {m['f2_dec']:.0%}")
        headlines, table = _ending_lines(joint.loc[idx], endings.loc[idx], f1, f2,
                                         int(row["scheduled_rounds"] or 3))
        lines += headlines

        drivers = ", ".join(f"{d['feature']} {d['value']:+.2f}"
                            for d in top_drivers(pred.drivers.loc[idx], top=5))
        lines += [f"- drivers (log-odds): {drivers}", ""] + table + [""]

    lines += ["---", "*Simulation/educational project. No betting advice. "
              "The market knows more than this model.*"]
    return "\n".join(lines)


def predict_card(conn, card_path: Path, artifact: dict, cfg: dict) -> str:
    """Predict a card and render it — the one-call path for simple uses."""
    return render_card(card_predictions(conn, card_path, artifact, cfg),
                       artifact, cfg)

"""Walk-forward scoring for method and round models vs historical base rates."""

import numpy as np
import pandas as pd

from octagon.models import finish_round, method


def report(df: pd.DataFrame, eval_df: pd.DataFrame, windows: list[tuple[str, str]],
           params: dict, seed: int = 42, weight_round_base: float = 0.5,
           weight_method_base: float = 0.0, include_raw: bool = False,
           p_f1_wins: np.ndarray | None = None) -> str:
    """Markdown section: both models against their base-rate opponents."""
    m_pred, m_base = method.walk_forward_predict(df, windows, seed=seed,
                                                 include_raw=include_raw)
    r_pred, r_base = finish_round.walk_forward_predict(df, windows, seed=seed)

    scored = eval_df.loc[m_pred.loc[eval_df.index].notna().all(axis=1)]
    m_truth = method.trainable(scored)
    m_rows = []
    m_model, m_baseline = m_pred.loc[m_truth.index], m_base.loc[m_truth.index]
    true_how = m_truth["method_class"].str.split("_").str[1]
    p_win = None
    if p_f1_wins is not None:
        p_win = pd.Series(p_f1_wins, index=eval_df.index).reindex(m_truth.index)
    for name, p in [
        (f"method model, shrunk (production, {1 - weight_method_base:.0%} model)",
         method.blend(m_baseline, m_model, weight_method_base)),
        ("method model, unshrunk", m_model),
        ("base rate (division x scheduled rounds, recent era)", m_baseline),
    ]:
        how = method.winner_how(p, m_truth)
        fight_p = method.condition_on_win_prob(p, p_win.to_numpy()) if p_win is not None else p
        fight = pd.DataFrame({g: fight_p[f"f1_{g}"] + fight_p[f"f2_{g}"]
                              for g in method.GROUPS}, index=p.index)
        if p_win is None:
            fight = fight / 2.0
        called = np.where(
            fight["ko"] + fight["sub"] >= fight["dec"],
            np.where(fight["ko"] >= fight["sub"], "ko", "sub"),
            "dec")
        m_rows.append((
            name, len(m_truth),
            method.how_log_loss(true_how, how),
            float((how.idxmax(axis=1) == true_how).mean()),
            float((called == true_how).mean())))

    r_truth = finish_round.trainable(scored)
    model_p = finish_round.actual_channel_probs(r_pred.loc[r_truth.index], r_truth)
    base_p = finish_round.actual_channel_probs(r_base.loc[r_truth.index], r_truth)
    r_rows = []
    for name, p in [
        (f"round model, shrunk (production, {1 - weight_round_base:.0%} model)",
         finish_round.blend(base_p, model_p, weight_round_base)),
        ("round model, unshrunk", model_p),
        ("base rate (method x scheduled rounds)", base_p),
    ]:
        modal = p.to_numpy().argmax(axis=1) + 1
        truth = r_truth["end_round"].to_numpy()
        r_rows.append((name, len(r_truth),
                       finish_round.round_log_loss(r_truth["end_round"], p),
                       float((modal == truth).mean()),
                       float((np.abs(modal - truth) <= 1).mean())))

    lines = [
        "",
        "## How the fight ends (method + round)",
        "",
        "Both models are walk-forward and scored only where they apply: the "
        "method model on every decisive fight, the round model on finishes "
        "only (a decision has no round to predict). The method model answers "
        "how the winner wins (KO / submission / decision); fight-level "
        "KO/sub/dec is that split averaged across corners, which is what "
        "the scorecard grades. The round model answers a conditional "
        "question — given that this fighter finished by this method, which "
        "round? — so its opponent is the historical round split for the "
        "same method and the same fight length.",
        "",
        "| method of victory (how the winner wins) | n | log loss | winner's method | fight KO/sub/dec |",
        "|---|---|---|---|---|",
    ]
    lines += [f"| {name} | {n} | {ll:.4f} | {acc:.1%} | {grp:.1%} |"
              for name, n, ll, acc, grp in m_rows]
    lines += [
        "",
        "| round of finish (1-5) | n | log loss | exact round | within 1 round |",
        "|---|---|---|---|---|",
    ]
    lines += [f"| {name} | {n} | {ll:.4f} | {acc:.1%} | {near:.1%} |"
              for name, n, ll, acc, near in r_rows]
    lines += [
        "",
        f"Uninformed reference: guessing uniformly over 3 methods "
        f"costs {np.log(3):.4f}; over the 3 rounds of a standard fight, "
        f"{np.log(3):.4f}. Read both tables with the base-rate row as "
        "the bar. Finish timing is close to a coin flip weighted by "
        "'earlier is likelier', which is why the production model is "
        "shrunk toward that base rate rather than trusted outright.",
    ]
    return "\n".join(lines)

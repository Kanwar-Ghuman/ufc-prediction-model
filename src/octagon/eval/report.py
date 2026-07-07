"""Milestone 3 evaluation: all baselines vs. the reference logistic
regression, walk-forward, written to a markdown report + reliability plot.

Ground rules encoded here:
* Default split is VALIDATION (2022-2023). The test years stay untouched
  until the project's final report — evaluating on test during development
  quietly turns it into a second validation set.
* The market baseline exists only where odds exist; models are additionally
  scored on that priced subset so the comparison is apples-to-apples.
* Every run appends to reports/experiments.csv — results you can't trace
  back later didn't happen.
"""

from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from octagon.eval import metrics
from octagon.models import baselines, logistic


def semiannual_windows(start_exclusive: str, end_inclusive: str) -> list[tuple[str, str]]:
    """Chop (start, end] into ~6-month walk-forward windows."""
    windows = []
    year, half = int(start_exclusive[:4]), 1 if start_exclusive[5:7] < "07" else 2
    # first window starts just after the boundary
    year, half = (year, 2) if half == 1 else (year + 1, 1)
    while True:
        lo = f"{year}-01-01" if half == 1 else f"{year}-07-01"
        hi = f"{year}-06-30" if half == 1 else f"{year}-12-31"
        if lo > end_inclusive:
            return windows
        windows.append((lo, min(hi, end_inclusive)))
        year, half = (year, 2) if half == 1 else (year + 1, 1)


def evaluate_split(df: pd.DataFrame, train_end: str, valid_end: str,
                   split: str, reports_dir: Path) -> str:
    if split == "valid":
        lo, hi = train_end, valid_end
    else:  # 'test'
        lo, hi = valid_end, "9999-12-31"
    eval_df = df[(df["date"] > lo) & (df["date"] <= hi)].copy()
    y = eval_df["label"].to_numpy(dtype=float)

    rows: list[dict] = []
    named_preds: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    def add(name: str, p: np.ndarray, mask: np.ndarray | None = None, note: str = ""):
        m = np.isfinite(p) if mask is None else (mask & np.isfinite(p))
        if m.sum() == 0:
            rows.append({"model": name, "note": "no fights to score" + (f" ({note})" if note else "")})
            return
        rows.append({"model": name, **metrics.summarize(y[m], p[m]), "note": note})
        named_preds[name] = (y[m], p[m])

    # --- baselines ---
    for name, fn in baselines.BASELINES.items():
        p = fn(eval_df)
        add(name, p, note="priced fights only" if name.startswith("market") else "")

    # --- reference model: walk-forward logistic regression on differentials ---
    windows = semiannual_windows(lo, min(hi, str(eval_df["date"].max())))
    lr_pred = logistic.walk_forward_predict(df, windows).loc[eval_df.index].to_numpy()
    add("logistic regression (walk-forward)", lr_pred)

    # --- tuned GBM (+ blend), if `octagon train` has produced an artifact ---
    gbm_cal_pred = blend_pred = None
    artifact_path = reports_dir.parent / "artifacts" / "gbm.joblib"
    if artifact_path.exists():
        import joblib

        from octagon.models import calibration, ensemble, gbm

        artifact = joblib.load(artifact_path)
        raw = gbm.walk_forward_predict(df, windows, artifact["params"],
                                       seed=artifact["seed"]).loc[eval_df.index].to_numpy()
        add("GBM (walk-forward, tuned)", raw)
        gbm_cal_pred = np.full(len(raw), np.nan)
        finite = np.isfinite(raw)
        gbm_cal_pred[finite] = calibration.apply(artifact["iso"], raw[finite])
        add("GBM + isotonic (fit on train-era OOS)", gbm_cal_pred)
        blend_pred = ensemble.blend(lr_pred, gbm_cal_pred, artifact["weight_lr"])
        add(f"LR+GBM blend (w={artifact['weight_lr']:.2f}, tuned on train-era OOS)",
            blend_pred)

    # Apples-to-apples on the priced subset.
    priced = (eval_df["f1_odds"].notna() & eval_df["f2_odds"].notna()).to_numpy()
    if priced.any():
        add("logistic regression (priced subset)", lr_pred, mask=priced,
            note="same fights as market row")
        if gbm_cal_pred is not None:
            add("GBM + isotonic (priced subset)", gbm_cal_pred, mask=priced,
                note="same fights as market row")
        if blend_pred is not None:
            add("LR+GBM blend (priced subset)", blend_pred, mask=priced,
                note="same fights as market row")
        if blend_pred is not None and "market_stack" in artifact:
            from octagon.models import market as market_stack

            a, b = artifact["market_stack"]
            p_mkt = baselines.market(eval_df)
            stack = np.full(len(eval_df), np.nan)
            ok = priced & np.isfinite(blend_pred) & np.isfinite(p_mkt)
            stack[ok] = market_stack.predict_stack(a, b, p_mkt[ok], blend_pred[ok])
            add(f"market-aware stack (a={a:.2f}, b={b:.2f})", stack, mask=priced,
                note="IS the odds + residual skill — never 'beat the odds'")

    # --- artifacts ---
    reports_dir.mkdir(parents=True, exist_ok=True)
    plot_path = reports_dir / f"reliability_{split}.png"
    metrics.reliability_diagram(
        {k: v for k, v in named_preds.items() if k != "coin flip"}, plot_path)

    # Per-fight predictions for downstream analysis (error notebook, abstain
    # band, backtest). One row per evaluated fight, one column per model.
    pred_frame = eval_df[["fight_id", "date", "f1_name", "f2_name", "weight_class",
                          "title_fight", "label", "f1_odds", "f2_odds",
                          "f1_n_fights", "f2_n_fights", "f1_layoff_days",
                          "f2_layoff_days"]].copy()
    pred_frame["p_market"] = baselines.market(eval_df)
    pred_frame["p_lr"] = lr_pred
    if gbm_cal_pred is not None:
        pred_frame["p_gbm_cal"] = gbm_cal_pred
    if blend_pred is not None:
        pred_frame["p_blend"] = blend_pred
    pred_frame.to_parquet(reports_dir / f"predictions_{split}.parquet", index=False)

    # Coefficients from a final fit on everything before the split (the
    # walk-forward folds differ per window; this one is for reading).
    final_fit = logistic.fit(df[df["date"] <= lo])
    coefs = logistic.coefficients(final_fit, df).head(15)

    _append_experiment_log(reports_dir, split, rows)
    return _render_markdown(split, lo, hi, rows, coefs, plot_path, windows)


def _append_experiment_log(reports_dir: Path, split: str, rows: list[dict]) -> None:
    log_path = reports_dir / "experiments.csv"
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    frame = pd.DataFrame([{"ts": stamp, "split": split, **r} for r in rows if "n" in r])
    frame.to_csv(log_path, mode="a", header=not log_path.exists(), index=False)


def _render_markdown(split, lo, hi, rows, coefs, plot_path, windows) -> str:
    lines = [
        f"# Evaluation report — {split} split",
        "",
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}. "
        f"Fights dated ({lo}, {hi}]. Walk-forward windows: "
        + ", ".join(f"{a}->{b}" for a, b in windows),
        "",
        "| model | n | accuracy | log loss | Brier | ROC AUC | ECE | note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        if "n" not in r:
            lines.append(f"| {r['model']} | - | - | - | - | - | - | {r['note']} |")
            continue
        lines.append(
            f"| {r['model']} | {r['n']} | {r['accuracy']:.4f} | {r['log_loss']:.4f} "
            f"| {r['brier']:.4f} | {r['roc_auc']:.4f} | {r['ece']:.4f} | {r.get('note','')} |")
    lines += [
        "",
        "Reading guide: 'better record' is a picking rule (0/0.5/1 outputs) — "
        "its log loss is meaningless by design; compare models on log loss / "
        "Brier / ECE against the market row, on accuracy against all rows.",
        "",
        f"![reliability diagram]({plot_path.name})",
        "",
        "## Logistic regression — largest standardized coefficients",
        "",
        "Positive means: the bigger fighter1's edge in this differential, the "
        "likelier fighter1 wins (per the model).",
        "",
        "| feature | coefficient |",
        "|---|---|",
    ]
    lines += [f"| {name} | {value:+.3f} |" for name, value in coefs.items()]
    lines += [
        "",
        "---",
        "*Honest context: 'always pick the favorite' wins ~65% of priced fights "
        "and the vig-free market's log loss is ~0.62. Beating the record/Elo "
        "baselines is expected; approaching the market is the actual fight.*",
    ]
    return "\n".join(lines)

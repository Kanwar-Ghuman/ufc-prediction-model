"""SHAP explanations for the GBM (PRD Phase C step 6).

Explanations must describe the prediction we actually make, and our
prediction is the SYMMETRIZED one: p = (f(x) + 1 - f(x'))/2 with x' the
corner-swapped input. In log-odds space that's score(x) = (raw(x) -
raw(x'))/2, so each feature's contribution is (phi(x) - phi(x'))/2:

* diff features flip sign under the swap, so their two contributions
  reinforce — the model's real opinion about the matchup;
* context features (title fight, weight class) are identical in x and x',
  so their contributions nearly cancel — correct, because a title flag
  can't favor either corner, it can only interact with the diffs;
* the base value cancels to 0 = log-odds of 0.5 — with no information,
  a fight is a coin flip. Every explanation starts from fair.

Units are log-odds: +0.20 on diff_elo means the Elo edge moved the fight
about 5 percentage points toward fighter1 (near p=0.5, 4 log-odds points
~ 1 probability point). The sum of contributions is the symmetrized score,
whose sigmoid approximates (not exactly equals) the reported probability —
the tiny gap is the price of averaging in probability space.
"""

import warnings

import numpy as np
import pandas as pd

from octagon.models import gbm

# shap warns that its LightGBM binary output format changed; we already
# handle both shapes below, so the warning is pure noise for users.
warnings.filterwarnings(
    "ignore", message=".*LightGBM binary classifier with TreeExplainer.*")


def _flipped(X: pd.DataFrame) -> pd.DataFrame:
    out = X.copy()
    for col in out.columns:
        if col.startswith("diff_"):
            out[col] = -out[col]
    return out


def shap_symmetrized(model, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Per-fight, per-feature contributions to the symmetrized log-odds.

    Returns (contributions, features_used) aligned row-for-row with df.
    """
    import shap

    X = gbm.feature_frame(df)
    explainer = shap.TreeExplainer(model)
    phi = explainer.shap_values(X)
    phi_flipped = explainer.shap_values(_flipped(X))
    if isinstance(phi, list):  # some shap versions return [class0, class1]
        phi, phi_flipped = phi[1], phi_flipped[1]
    sym = (phi - phi_flipped) / 2.0
    return pd.DataFrame(sym, columns=X.columns, index=df.index), X


def global_importance(model, df: pd.DataFrame) -> pd.Series:
    """Mean |contribution| per feature — what the model leans on overall."""
    contributions, _ = shap_symmetrized(model, df)
    return contributions.abs().mean().sort_values(ascending=False)


def summary_plot(model, df: pd.DataFrame, path) -> None:
    """Beeswarm: each dot is one fight; color = feature value, x = push."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import shap

    contributions, X = shap_symmetrized(model, df)
    shap.summary_plot(contributions.to_numpy(),
                      X.drop(columns=["weight_class"]).assign(
                          weight_class=X["weight_class"].cat.codes),
                      feature_names=list(X.columns), max_display=20, show=False)
    plt.gcf().set_size_inches(9, 7)
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close("all")


def explain_fight(model, df: pd.DataFrame, fight_id: int) -> pd.Series:
    """Sorted feature contributions (log-odds) for one fight."""
    row = df[df["fight_id"] == fight_id]
    if row.empty:
        raise SystemExit(f"fight_id {fight_id} not found in the feature table")
    contributions, _ = shap_symmetrized(model, row)
    return contributions.iloc[0].sort_values(key=abs, ascending=False)


def render_fight_text(df: pd.DataFrame, fight_id: int, contributions: pd.Series,
                      probability: float, top: int = 10) -> str:
    """Human-readable per-fight explanation for the terminal / reports."""
    row = df[df["fight_id"] == fight_id].iloc[0]
    f1, f2 = row["f1_name"], row["f2_name"]
    lines = [
        f"{f1} vs. {f2} — {row['date']} ({row['weight_class']})",
        f"P({f1} wins) = {probability:.3f}   [symmetrized, calibrated]",
        "",
        f"What moved it (log-odds; + favors {f1}, - favors {f2}):",
    ]
    for name, value in contributions.head(top).items():
        if abs(value) < 1e-4:
            continue
        lines.append(f"  {value:+.3f}  {name}")
    residual = contributions.iloc[top:].sum()
    lines.append(f"  {residual:+.3f}  (everything else)")
    return "\n".join(lines)


def waterfall_plot(contributions: pd.Series, path, top: int = 12) -> None:
    """Per-fight waterfall via shap's own plot, fed our symmetrized values."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import shap

    head = contributions.head(top)
    rest = contributions.iloc[top:].sum()
    explanation = shap.Explanation(
        values=np.append(head.to_numpy(), rest),
        base_values=0.0,  # log-odds of 0.5: no information, fair fight
        feature_names=list(head.index) + ["everything else"],
    )
    shap.plots.waterfall(explanation, show=False)
    plt.gcf().set_size_inches(9, 6)
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close("all")

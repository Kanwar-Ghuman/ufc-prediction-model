"""How the winner wins: P(finish | win) and P(KO | finish).

A 6-class joint spent capacity on who wins (already answered by the blend)
and then lost the argmax to decision when KO+sub split the finish mass.
Hyperparameters are this model's, not the win GBM's. Base rates use the
last four years of the division × fight-length cell.
"""

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier

from octagon.models.gbm import _flip, feature_frame

CLASSES = ["f1_ko", "f1_sub", "f1_dec", "f2_ko", "f2_sub", "f2_dec"]
GROUPS = ["ko", "sub", "dec"]

_METHOD_GROUP = {"KO/TKO": "ko", "SUB": "sub",
                 "U-DEC": "dec", "S-DEC": "dec", "M-DEC": "dec"}

# Sized for ~8,000 winner-method labels, not the win model's 8,600 fights
# x a much stronger target. Smaller trees, more regularisation.
DEFAULT_PARAMS = {
    "n_estimators": 300,
    "learning_rate": 0.04,
    "num_leaves": 12,
    "min_child_samples": 60,
    "feature_fraction": 0.65,
    "bagging_fraction": 0.8,
    "bagging_freq": 1,
    "reg_lambda": 4.0,
}

# Don't let 2010's decision-heavy heavyweight mix price 2026.
RECENCY_YEARS = 4
RECENCY_MIN_FIGHTS = 60


def method_class(label: float, method: str | None) -> str | None:
    """Row label + method string -> one of CLASSES, or None if untrainable."""
    group = _METHOD_GROUP.get(method or "")
    if group is None or label not in (0, 1):
        return None
    return f"{'f1' if label == 1 else 'f2'}_{group}"


def winner_group(method: str | None) -> str | None:
    return _METHOD_GROUP.get(method or "")


def trainable(df: pd.DataFrame) -> pd.DataFrame:
    """Rows with a clean method class, plus a 'method_class' column."""
    out = df.copy()
    out["method_class"] = [method_class(label, m)
                           for label, m in zip(df["label"], df["method"])]
    return out[out["method_class"].notna()]


def _oriented(X: pd.DataFrame, winner_is_f1) -> pd.DataFrame:
    """Rewrite each row from the winner's point of view."""
    flipped = _flip(X)
    mask = np.asarray(winner_is_f1, dtype=bool)
    out = X.copy()
    for col in X.columns:
        if col.startswith(("diff_", "f1_", "f2_")):
            out[col] = np.where(mask, X[col].to_numpy(), flipped[col].to_numpy())
    return out


def _design(df: pd.DataFrame, winner_is_f1, include_raw: bool = True) -> pd.DataFrame:
    return _oriented(feature_frame(df, include_raw=include_raw), winner_is_f1)


class _ConstantProba:
    """Fallback when a binary head has only one class in the training window."""

    def __init__(self, p_positive: float):
        self.p_positive = float(p_positive)

    def predict_proba(self, X) -> np.ndarray:
        n = len(X)
        p = np.full(n, self.p_positive)
        return np.column_stack([1.0 - p, p])


class HowModel:
    """P(finish | win) and P(KO | finish), composed into ko/sub/dec."""

    def __init__(self, finish, ko_given):
        self.finish = finish
        self.ko_given = ko_given

    def predict_how(self, X: pd.DataFrame) -> np.ndarray:
        p_finish = self.finish.predict_proba(X)[:, 1]
        p_ko_given = self.ko_given.predict_proba(X)[:, 1]
        p_ko = p_finish * p_ko_given
        p_sub = p_finish * (1.0 - p_ko_given)
        p_dec = 1.0 - p_finish
        return np.column_stack([p_ko, p_sub, p_dec])


def _binary(X: pd.DataFrame, y: np.ndarray, params: dict, seed: int):
    if len(np.unique(y)) < 2:
        return _ConstantProba(float(np.mean(y)))
    model = LGBMClassifier(objective="binary", random_state=seed, verbose=-1,
                           **params)
    model.fit(X, y)
    return model


def fit(train_df: pd.DataFrame, params: dict | None = None, seed: int = 42,
        include_raw: bool = True, **_ignored) -> HowModel:
    """Finish-vs-decision, then KO-vs-sub given a finish."""
    train = trainable(train_df)
    X = _design(train, train["label"].to_numpy() == 1, include_raw)
    groups = train["method_class"].str.split("_").str[1].to_numpy()
    settings = DEFAULT_PARAMS if params is None else params
    finish = _binary(X, (groups != "dec").astype(int), settings, seed)
    finished = groups != "dec"
    if finished.any():
        ko_given = _binary(X.iloc[finished], (groups[finished] == "ko").astype(int),
                           settings, seed)
    else:
        ko_given = _ConstantProba(0.5)
    return HowModel(finish, ko_given)


def _how_matrix(model: HowModel, X: pd.DataFrame) -> np.ndarray:
    """P(ko, sub, dec | the designed corner wins), columns in GROUPS order."""
    return model.predict_how(X)


def predict_sym(model: HowModel, df: pd.DataFrame,
                include_raw: bool = True) -> pd.DataFrame:
    """P(how | this corner wins) for both corners. Each trio sums to 1.

    Exactly invariant to corner order: predict(A,B)['f1_ko'] ==
    predict(B,A)['f2_ko']. Who-wins mass is applied later by
    `condition_on_win_prob`.
    """
    X = feature_frame(df, include_raw=include_raw)
    p_f1 = _how_matrix(model, X)
    p_f2 = _how_matrix(model, _flip(X))
    out = np.concatenate([p_f1, p_f2], axis=1)
    return pd.DataFrame(out, columns=CLASSES, index=df.index)


def condition_on_win_prob(probs: pd.DataFrame, p_f1_wins: np.ndarray) -> pd.DataFrame:
    """Rescale so each fighter's three classes sum to the canonical
    (calibrated blend) win probability — this model only decides the HOW."""
    out = probs.copy()
    f1_cols, f2_cols = CLASSES[:3], CLASSES[3:]
    f1_sum = out[f1_cols].sum(axis=1).replace(0, np.nan)
    f2_sum = out[f2_cols].sum(axis=1).replace(0, np.nan)
    for c in f1_cols:
        out[c] = out[c] / f1_sum * p_f1_wins
    for c in f2_cols:
        out[c] = out[c] / f2_sum * (1.0 - p_f1_wins)
    return out.fillna(0.0)


def call_group(ko, sub, dec):
    """Name the one method to call from {ko, sub, dec} marginals: the mode.

    The card report, the scorecard and the evaluation table all have to ask
    this, and they have to agree — otherwise a fight is reported one way and
    graded another. Argmax is also the accuracy-maximising answer for a 0-1
    score on calibrated probabilities.

    Pooling KO and submission into 'a finish' and resolving that first is
    the tempting alternative, on the grounds that argmax under-calls
    finishes when the two split the finish mass. Measured on the validation
    and test eras it was worse on both: KO is ~65% of finishes, so a
    resolved finish nearly always resolved to KO, which called KO on 48% of
    test-era fights that ended in KO 33% of the time. It scored 50.5% where
    a constant 'decision' scores 49.9%; argmax scores 54.4%.

    Accepts scalars or arrays and returns the matching shape.
    """
    ko, sub, dec = np.asarray(ko), np.asarray(sub), np.asarray(dec)
    out = np.where((dec >= ko) & (dec >= sub), "dec",
                   np.where(ko >= sub, "ko", "sub"))
    return str(out) if out.ndim == 0 else out


def winner_how(probs: pd.DataFrame, truth: pd.DataFrame) -> pd.DataFrame:
    """The winner's three how-probabilities, for scoring the HOW model."""
    label = truth["label"].to_numpy()
    rows = np.column_stack([
        np.where(label == 1,
                 probs.loc[truth.index, f"f1_{g}"].to_numpy(),
                 probs.loc[truth.index, f"f2_{g}"].to_numpy())
        for g in GROUPS
    ])
    return pd.DataFrame(rows, index=truth.index, columns=GROUPS)


def how_log_loss(groups: pd.Series, how: pd.DataFrame) -> float:
    p = np.clip(how.to_numpy(), 1e-12, 1.0)
    idx = [GROUPS.index(str(g)) for g in groups]
    return float(-np.mean(np.log(p[np.arange(len(idx)), idx])))


def multiclass_log_loss(y_true: pd.Series, probs: pd.DataFrame) -> float:
    """6-class log loss, kept for callers that still have f1_ko labels.

    Prefer `how_log_loss` on `winner_how(...)` — that is what this model
    actually decides.
    """
    p = np.clip(probs.to_numpy(), 1e-12, 1.0)
    idx = [CLASSES.index(c) for c in y_true]
    return float(-np.mean(np.log(p[np.arange(len(idx)), idx])))


def _era(train: pd.DataFrame) -> pd.DataFrame:
    """Recent fights when there are enough of them to estimate a mix."""
    if "date" not in train.columns or train["date"].isna().all():
        return train
    dates = pd.to_datetime(train["date"], errors="coerce")
    latest = dates.max()
    if pd.isna(latest):
        return train
    cutoff = latest - pd.DateOffset(years=RECENCY_YEARS)
    recent = train[dates >= cutoff]
    return recent if len(recent) >= RECENCY_MIN_FIGHTS else train


def base_rate_methods(train_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """P(KO/sub/dec | a win) for this division and fight length.

    Same mix on both corners — the model is what makes a KO artist different
    from a grinder. Split is recent-era so 2026 is not priced off 2010.
    """
    train = _era(trainable(train_df))
    groups = train["method_class"].str.split("_").str[1]
    overall = groups.value_counts(normalize=True)
    fallback = np.array([overall.get(g, 1.0 / 3) for g in GROUPS], dtype=float)

    def mix(rows: pd.DataFrame) -> np.ndarray | None:
        if len(rows) < 40:
            return None
        share = rows["method_class"].str.split("_").str[1].value_counts(normalize=True)
        return np.array([share.get(g, 0.0) for g in GROUPS], dtype=float)

    by_class_len: dict[tuple, np.ndarray] = {}
    for key, rows in train.groupby(["weight_class", "scheduled_rounds"], dropna=False):
        cell = mix(rows)
        if cell is not None:
            by_class_len[key] = cell
    by_class: dict[object, np.ndarray] = {}
    for key, rows in train.groupby("weight_class", dropna=False):
        cell = mix(rows)
        if cell is not None:
            by_class[key] = cell

    out = np.zeros((len(df), len(CLASSES)))
    for i, (_, row) in enumerate(df.iterrows()):
        key = (row.get("weight_class"), row.get("scheduled_rounds"))
        share = by_class_len.get(key)
        if share is None:
            share = by_class.get(row.get("weight_class"), fallback)
        out[i] = np.concatenate([share, share])
    return pd.DataFrame(out, columns=CLASSES, index=df.index)


def blend(base_probs: pd.DataFrame, model_probs: pd.DataFrame,
          weight_base: float) -> pd.DataFrame:
    """Shrink the model's how-split toward the division base rate."""
    return base_probs * weight_base + model_probs * (1.0 - weight_base)


def walk_forward_predict(
    df: pd.DataFrame, windows: list[tuple[str, str]],
    params: dict | None = None, seed: int = 42, include_raw: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """How-given-win distributions from a model and a base rate that each
    saw only earlier fights. Returns (model, base), NaN outside the windows."""
    model_out = pd.DataFrame(np.nan, index=df.index, columns=CLASSES)
    base_out = pd.DataFrame(np.nan, index=df.index, columns=CLASSES)
    for start, end in windows:
        train = df[df["date"] < start]
        window = df[(df["date"] >= start) & (df["date"] <= end)]
        if len(trainable(train)) < 200 or len(window) == 0:
            continue
        fitted = fit(train, params=params, seed=seed, include_raw=include_raw)
        model_out.loc[window.index] = predict_sym(
            fitted, window, include_raw=include_raw).to_numpy()
        base_out.loc[window.index] = base_rate_methods(train, window).to_numpy()
    return model_out, base_out


def tune_base_weight(df: pd.DataFrame, windows: list[tuple[str, str]],
                     params: dict | None = None, seed: int = 42,
                     include_raw: bool = True) -> tuple[float, float]:
    """Pick the base-rate share by walk-forward log loss of the winner's method."""
    model_p, base_p = walk_forward_predict(df, windows, params=params, seed=seed,
                                           include_raw=include_raw)
    usable = model_p.notna().all(axis=1)
    scored = trainable(df.loc[usable])
    if len(scored) == 0:
        return 1.0, float("nan")
    groups = scored["method_class"].str.split("_").str[1]
    m = winner_how(model_p.loc[scored.index], scored)
    b = winner_how(base_p.loc[scored.index], scored)
    grid = np.linspace(0.0, 1.0, 21)
    losses = [how_log_loss(groups, blend(b, m, w)) for w in grid]
    best = int(np.argmin(losses))
    return float(grid[best]), float(losses[best])

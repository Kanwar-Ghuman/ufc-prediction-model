"""Method-of-victory prediction (v2 stretch goal): who wins AND how.

Six classes: {fighter1, fighter2} x {KO/TKO, submission, decision}.
Fights ending in DQs, doctor-stoppage oddities recorded as other methods,
or overturned results are excluded from method training (a few percent).

Symmetry works like the binary GBM, one step further: the training set is
augmented with corner-swapped copies whose CLASS is remapped (f1_ko <->
f2_ko, ...), and prediction averages the model's output on x with the
remapped output on swap(x). Swapping the fighters then permutes the class
probabilities exactly — predict(A,B)['f1_ko'] == predict(B,A)['f2_ko'].

The win probability implied by this model (sum of a fighter's three
classes) is NOT the project's canonical win probability — the calibrated
blend is. `condition_on_win_prob` rescales the six classes so they agree
with the blend, leaving only the method split to this model.
"""

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier

from octagon.models.gbm import feature_frame

CLASSES = ["f1_ko", "f1_sub", "f1_dec", "f2_ko", "f2_sub", "f2_dec"]
_SWAPPED_ORDER = [3, 4, 5, 0, 1, 2]  # f1_* <-> f2_*

_METHOD_GROUP = {"KO/TKO": "ko", "SUB": "sub",
                 "U-DEC": "dec", "S-DEC": "dec", "M-DEC": "dec"}


def method_class(label: float, method: str | None) -> str | None:
    """Row label + method string -> one of CLASSES, or None if untrainable."""
    group = _METHOD_GROUP.get(method or "")
    if group is None or label not in (0, 1):
        return None
    return f"{'f1' if label == 1 else 'f2'}_{group}"


def trainable(df: pd.DataFrame) -> pd.DataFrame:
    """Rows with a clean method class, plus a 'method_class' column."""
    out = df.copy()
    out["method_class"] = [method_class(label, m)
                           for label, m in zip(df["label"], df["method"])]
    return out[out["method_class"].notna()]


def fit(train_df: pd.DataFrame, params: dict, seed: int = 42) -> LGBMClassifier:
    train = trainable(train_df)
    X = feature_frame(train)
    y = train["method_class"]

    flipped = X.copy()
    for col in flipped.columns:
        if col.startswith("diff_"):
            flipped[col] = -flipped[col]
    swap_class = dict(zip(CLASSES, (CLASSES[i] for i in _SWAPPED_ORDER)))
    X_aug = pd.concat([X, flipped], ignore_index=True)
    y_aug = pd.concat([y, y.map(swap_class)], ignore_index=True)

    model = LGBMClassifier(objective="multiclass", num_class=len(CLASSES),
                           random_state=seed, verbose=-1,
                           **{k: v for k, v in params.items() if k != "bagging_freq"})
    model.fit(X_aug, y_aug)
    return model


def predict_sym(model: LGBMClassifier, df: pd.DataFrame) -> pd.DataFrame:
    """Class probabilities, exactly invariant to corner order."""
    X = feature_frame(df)
    flipped = X.copy()
    for col in flipped.columns:
        if col.startswith("diff_"):
            flipped[col] = -flipped[col]
    order = list(model.classes_)
    p = model.predict_proba(X)[:, [order.index(c) for c in CLASSES]]
    p_flip = model.predict_proba(flipped)[:, [order.index(c) for c in CLASSES]]
    p_sym = (p + p_flip[:, _SWAPPED_ORDER]) / 2.0
    return pd.DataFrame(p_sym, columns=CLASSES, index=df.index)


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


def multiclass_log_loss(y_true: pd.Series, probs: pd.DataFrame) -> float:
    p = np.clip(probs.to_numpy(), 1e-12, 1.0)
    idx = [CLASSES.index(c) for c in y_true]
    return float(-np.mean(np.log(p[np.arange(len(idx)), idx])))

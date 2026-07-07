"""The reference model: logistic regression on differentials (PRD Phase A).

Antisymmetry by architecture, not by hope (PRD 5.5): the model sees ONLY
diff_* features (fighter1 minus fighter2), missing diffs are imputed with
0 ("no known difference"), scaling divides without centering, and there is
no intercept. Then swapping the fighters negates the input exactly, and
sigmoid(-z) = 1 - sigmoid(z) gives predict(A,B) = 1 - predict(B,A) to
machine precision. tests/test_models.py holds it to that.

Why logistic regression as the reference: linear, so its coefficients are
readable; trained on log loss, so its probabilities are honest by nature;
and hard to beat by enough to justify anything fancier — which is exactly
the point of a reference.
"""

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def diff_columns(df: pd.DataFrame) -> list[str]:
    return sorted(c for c in df.columns if c.startswith("diff_"))


def _matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Feature matrix as floats. An all-missing column arrives from pandas
    as object dtype (None values), which the imputer would silently pass
    through; astype(float) turns every None into a real NaN first."""
    return df[diff_columns(df)].astype(float)


def make_pipeline(C: float = 1.0) -> Pipeline:
    """Impute -> scale -> logistic regression, one object.

    A Pipeline exists so that imputer and scaler statistics are fit ONLY on
    whatever .fit() sees (training data) — the leakage checklist's last box.
    """
    return Pipeline([
        # keep_empty_features: an era with (say) no control-time data must
        # still produce that column, or train/predict shapes drift apart.
        ("impute", SimpleImputer(strategy="constant", fill_value=0.0,
                                 keep_empty_features=True)),
        ("scale", StandardScaler(with_mean=False)),  # centering would break antisymmetry
        ("model", LogisticRegression(fit_intercept=False, C=C, max_iter=1000)),
    ])


def fit(train: pd.DataFrame, C: float = 1.0) -> Pipeline:
    pipeline = make_pipeline(C=C)
    pipeline.fit(_matrix(train), train["label"])
    return pipeline


def predict(pipeline: Pipeline, df: pd.DataFrame) -> np.ndarray:
    """P(fighter1 wins) for each row."""
    return pipeline.predict_proba(_matrix(df))[:, 1]


def coefficients(pipeline: Pipeline, df: pd.DataFrame) -> pd.Series:
    """Standardized coefficients, largest effect first — the 'why'."""
    coefs = pipeline.named_steps["model"].coef_[0]
    return (pd.Series(coefs, index=diff_columns(df))
            .sort_values(key=abs, ascending=False))


def walk_forward_predict(
    df: pd.DataFrame, windows: list[tuple[str, str]], C: float = 1.0
) -> pd.Series:
    """Expanding-window evaluation: for each window, train on strictly
    earlier fights, predict the window. No fight is ever predicted by a
    model that saw it — or saw anything after it.

    Returns predictions indexed like df, NaN outside the windows.
    """
    out = pd.Series(np.nan, index=df.index)
    for start, end in windows:
        train = df[df["date"] < start]
        window = df[(df["date"] >= start) & (df["date"] <= end)]
        if len(train) == 0 or len(window) == 0:
            continue
        out.loc[window.index] = predict(fit(train, C=C), window)
    return out

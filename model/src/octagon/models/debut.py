"""Second GBM trained only on fights where a fighter has thin UFC history.

Uses the same corner-swap / symmetrized predict path as `gbm.py`. Only
installed when it beats the main blend on held-out low-history fights
(`cli.cmd_train`); otherwise `debut_model` is None.
"""

import numpy as np
import pandas as pd

from octagon.models import gbm

DEBUT_THRESHOLD = 5


def low_history_mask(df: pd.DataFrame) -> pd.Series:
    """True where at least one fighter has fewer than DEBUT_THRESHOLD UFC fights.

    min() is symmetric under a corner swap (f1_n_fights and f2_n_fights just
    exchange), so this is a safe subset FILTER, never a model feature.
    """
    return df[["f1_n_fights", "f2_n_fights"]].min(axis=1) < DEBUT_THRESHOLD


def tune(df: pd.DataFrame, tuning_windows: list[tuple[str, str]],
         n_trials: int = 40, seed: int = 42,
         include_raw: bool = True) -> tuple[dict, float]:
    """Optuna search on the low-history subset only."""
    subset = df[low_history_mask(df)]
    return gbm.tune(subset, tuning_windows, n_trials=n_trials, seed=seed,
                    include_raw=include_raw)


def walk_forward_predict(
    df: pd.DataFrame, windows: list[tuple[str, str]], params: dict, seed: int = 42,
    include_raw: bool = True, n_seeds: int = 1,
) -> pd.Series:
    """Walk-forward OOS predictions, low-history subset only.

    Returns a full-length Series aligned to df's index — NaN for rows outside
    the low-history subset, so callers can mask consistently with the main
    blend's OOS predictions on the same subset.
    """
    subset = df[low_history_mask(df)]
    sub_pred = gbm.walk_forward_predict(subset, windows, params, seed=seed,
                                        include_raw=include_raw, n_seeds=n_seeds)
    out = pd.Series(np.nan, index=df.index)
    out.loc[sub_pred.index] = sub_pred
    return out


def fit(df: pd.DataFrame, params: dict, seed: int = 42,
        include_raw: bool = True, n_seeds: int = 1):
    """Fit the final debut model on the low-history subset of df."""
    subset = df[low_history_mask(df)]
    return gbm.fit(subset, params, seed=seed, include_raw=include_raw, n_seeds=n_seeds)


def predict_sym(model, df: pd.DataFrame, include_raw: bool = True) -> np.ndarray:
    """Symmetrized P(fighter1 wins) — identical contract to gbm.predict_sym."""
    return gbm.predict_sym(model, df, include_raw=include_raw)

"""Phase B: gradient boosting (LightGBM) with walk-forward Optuna tuning.

Why LightGBM: state of the art on tabular data, handles our NaNs natively
(no imputation guesswork), and fast enough to retrain inside every
walk-forward window.

Symmetry strategy (PRD 5.5) — trees can't be antisymmetric by architecture
the way the no-intercept logistic regression is, so we get there in two
moves:
1. TRAIN on both orderings: every training row is duplicated with
   differentials negated and the label flipped, so the model can't learn
   anything from corner assignment.
2. PREDICT symmetrized: p = (model(x) + 1 - model(swap(x))) / 2, which makes
   predict(A,B) = 1 - predict(B,A) hold EXACTLY, by construction.

Features: the diff_* columns plus swap-invariant context (title fight,
scheduled rounds, gender, weight class). Nothing here changes when the
fighters trade corners except the sign of the diffs — that's what makes the
symmetrization sound.
"""

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier, early_stopping

CONTEXT_NUMERIC = ["title_fight", "scheduled_rounds", "gender_num"]
CONTEXT_CATEGORICAL = ["weight_class"]


def feature_frame(df: pd.DataFrame, market_aware: bool = False) -> pd.DataFrame:
    """Model inputs with proper dtypes; swap-invariant except diff signs.

    market_aware=True adds the vig-free market opinion as a differential
    (PRD 5.6). fair1 - fair2 negates under a corner swap like every other
    diff, so the symmetry machinery needs no special cases; unpriced fights
    get NaN, which LightGBM routes natively ("no odds -> use skill").
    NEVER report this variant's accuracy as "our model beat the odds" —
    it IS the odds, plus whatever residual skill the trees find.
    """
    diffs = sorted(c for c in df.columns if c.startswith("diff_"))
    X = df[diffs].astype(float).copy()
    X["title_fight"] = df["title_fight"].astype(float)
    X["scheduled_rounds"] = df["scheduled_rounds"].astype(float)
    X["gender_num"] = (df["gender"] == "F").astype(float)
    X["weight_class"] = df["weight_class"].astype("category")
    if market_aware:
        p1 = 1.0 / df["f1_odds"].astype(float)
        p2 = 1.0 / df["f2_odds"].astype(float)
        X["diff_market"] = (p1 - p2) / (p1 + p2)  # fair1 - fair2, vig removed
    return X


def _augmented(X: pd.DataFrame, y: np.ndarray) -> tuple[pd.DataFrame, np.ndarray]:
    """Append the corner-swapped copy of every row (negated diffs, flipped
    label). Context columns are swap-invariant and stay as they are."""
    flipped = X.copy()
    for col in flipped.columns:
        if col.startswith("diff_"):
            flipped[col] = -flipped[col]
    return pd.concat([X, flipped], ignore_index=True), np.concatenate([y, 1 - y])


def fit(train_df: pd.DataFrame, params: dict, eval_df: pd.DataFrame | None = None,
        seed: int = 42, market_aware: bool = False) -> LGBMClassifier:
    """Fit on augmented training data; optional early stopping on eval_df.

    Early stopping is only used during hyperparameter tuning (where the fold
    window doubles as the stopping set). Final fits use the tuned, FIXED
    n_estimators so evaluation windows are never peeked at.
    """
    X, y = _augmented(feature_frame(train_df, market_aware), train_df["label"].to_numpy())
    model = LGBMClassifier(objective="binary", random_state=seed, verbose=-1, **params)
    kwargs = {}
    if eval_df is not None:
        kwargs = {
            "eval_set": [(feature_frame(eval_df, market_aware), eval_df["label"].to_numpy())],
            "eval_metric": "binary_logloss",
            "callbacks": [early_stopping(stopping_rounds=50, verbose=False)],
        }
    model.fit(X, y, **kwargs)
    return model


def predict_sym(model: LGBMClassifier, df: pd.DataFrame,
                market_aware: bool = False) -> np.ndarray:
    """Symmetrized P(fighter1 wins): exact corner invariance by construction."""
    X = feature_frame(df, market_aware)
    flipped = X.copy()
    for col in flipped.columns:
        if col.startswith("diff_"):
            flipped[col] = -flipped[col]
    p = model.predict_proba(X)[:, 1]
    p_flipped = model.predict_proba(flipped)[:, 1]
    return (p + (1.0 - p_flipped)) / 2.0


def walk_forward_predict(
    df: pd.DataFrame, windows: list[tuple[str, str]], params: dict, seed: int = 42,
    market_aware: bool = False,
) -> pd.Series:
    """Same contract as logistic.walk_forward_predict: for each window,
    train on strictly earlier fights only. No early stopping here."""
    out = pd.Series(np.nan, index=df.index)
    for start, end in windows:
        train = df[df["date"] < start]
        window = df[(df["date"] >= start) & (df["date"] <= end)]
        if len(train) == 0 or len(window) == 0:
            continue
        model = fit(train, params, seed=seed, market_aware=market_aware)
        out.loc[window.index] = predict_sym(model, window, market_aware=market_aware)
    return out


def tune(df: pd.DataFrame, tuning_windows: list[tuple[str, str]],
         n_trials: int = 40, seed: int = 42) -> tuple[dict, float]:
    """Optuna search scored by mean walk-forward log loss over train-era folds.

    Each trial trains with early stopping (the fold window is the stopping
    set — mildly optimistic for iteration count, standard practice); the
    returned params fix n_estimators at the best trial's mean best-iteration
    so later fits never see their evaluation data.
    """
    import optuna

    from octagon.eval.metrics import log_loss

    optuna.logging.set_verbosity(optuna.logging.WARNING)

    def objective(trial: optuna.Trial) -> float:
        params = {
            "n_estimators": 2000,  # ceiling; early stopping picks the real one
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
            "num_leaves": trial.suggest_int("num_leaves", 4, 64, log=True),
            "min_child_samples": trial.suggest_int("min_child_samples", 10, 200, log=True),
            "feature_fraction": trial.suggest_float("feature_fraction", 0.4, 1.0),
            "bagging_fraction": trial.suggest_float("bagging_fraction", 0.5, 1.0),
            "bagging_freq": 1,
            "reg_lambda": trial.suggest_float("reg_lambda", 1e-3, 10.0, log=True),
        }
        losses, best_iters = [], []
        for start, end in tuning_windows:
            train = df[df["date"] < start]
            window = df[(df["date"] >= start) & (df["date"] <= end)]
            if len(train) < 500 or len(window) == 0:
                continue
            model = fit(train, params, eval_df=window, seed=seed)
            losses.append(log_loss(window["label"].to_numpy(), predict_sym(model, window)))
            best_iters.append(model.best_iteration_ or params["n_estimators"])
        trial.set_user_attr("mean_best_iter", float(np.mean(best_iters)))
        return float(np.mean(losses))

    study = optuna.create_study(direction="minimize",
                                sampler=optuna.samplers.TPESampler(seed=seed))
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)

    best = dict(study.best_params)
    best["n_estimators"] = max(20, int(study.best_trial.user_attrs["mean_best_iter"]))
    best["bagging_freq"] = 1
    return best, study.best_value

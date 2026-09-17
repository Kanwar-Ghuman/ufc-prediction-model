"""Round-of-finish via per-round hazards, not a 5-way softmax.

Each training row is oriented so the finisher is corner 1. Hazard h_j is
P(fight ends in round j | it reached j). Unreachable rounds are exactly 0;
the last scheduled round absorbs the remainder.

A multiclass-over-rounds model lost to the historical round split on
five-rounders — it never learned that a 3-round prelim cannot end in R4.
"""

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier

from octagon.models.gbm import _flip, feature_frame

ROUNDS = [1, 2, 3, 4, 5]
FINISH_CHANNELS = ["f1_ko", "f1_sub", "f2_ko", "f2_sub"]
FINISH_METHODS = ("KO/TKO", "SUB")

# Deliberately small. The win model's tuned parameters are sized for 8,600
# fights and a target with real signal; finish timing has ~7,000 at-risk
# rows and much weaker signal, and inheriting those settings produced a
# model that lost to the base rate through sheer overconfidence.
DEFAULT_PARAMS = {
    "n_estimators": 250,
    "learning_rate": 0.03,
    "num_leaves": 8,
    "min_child_samples": 100,
    "feature_fraction": 0.6,
    "bagging_fraction": 0.8,
    "bagging_freq": 1,
    "reg_lambda": 5.0,
}


def outcome_columns() -> list[str]:
    """Every column of the joint distribution, in report order."""
    cols: list[str] = []
    for corner in ("f1", "f2"):
        for group in ("ko", "sub"):
            cols += [f"{corner}_{group}_r{r}" for r in ROUNDS]
        cols.append(f"{corner}_dec")
    return cols


def trainable(df: pd.DataFrame) -> pd.DataFrame:
    """Finishes with a decisive label and a real round — the only rows that
    carry a round to learn from. Decisions, draws, DQs and no-contests say
    nothing about finish timing."""
    return df[df["method"].isin(FINISH_METHODS)
              & df["label"].isin([0, 1])
              & df["end_round"].isin(ROUNDS)]


def scheduled_rounds(df: pd.DataFrame) -> np.ndarray:
    """Fight length, defaulting to the three-round standard when unknown."""
    sched = df["scheduled_rounds"].to_numpy(dtype=float)
    return np.clip(np.nan_to_num(sched, nan=3.0), 1, len(ROUNDS))


def _oriented(X: pd.DataFrame, finisher_is_f1) -> pd.DataFrame:
    """Rewrite each row from its finisher's point of view.

    Only the per-corner columns move; the swap-invariant context (weight
    class, scheduled rounds, ...) is left alone, which also keeps its
    categorical dtype intact for LightGBM.
    """
    flipped = _flip(X)
    mask = np.asarray(finisher_is_f1, dtype=bool)
    sided = [c for c in X.columns if c.startswith(("diff_", "f1_", "f2_"))]
    # One vectorised where over the sided block, then a single concat —
    # assigning ~370 columns one by one fragments the frame and is slow.
    oriented = pd.DataFrame(
        np.where(mask[:, None], X[sided].to_numpy(dtype=float),
                 flipped[sided].to_numpy(dtype=float)),
        columns=sided, index=X.index)
    rest = X[[c for c in X.columns if c not in set(sided)]]
    return pd.concat([oriented, rest], axis=1)[list(X.columns)].copy()


def _design(df: pd.DataFrame, finisher_is_f1, is_ko,
            include_raw: bool = False) -> pd.DataFrame:
    """Matchup features from the finisher's side; the round index is added
    per hazard question, not here."""
    X = _oriented(feature_frame(df, include_raw=include_raw), finisher_is_f1)
    X["finish_ko"] = np.asarray(is_ko, dtype=float)
    return X


def fit(train_df: pd.DataFrame, params: dict | None = None, seed: int = 42,
        include_raw: bool = False) -> LGBMClassifier:
    """Fit the per-round hazard on every round every finish survived into."""
    train = trainable(train_df)
    base = _design(train, train["label"].to_numpy() == 1,
                   train["method"].to_numpy() == "KO/TKO", include_raw)
    sched = scheduled_rounds(train)
    end = np.clip(train["end_round"].to_numpy(dtype=int), 1, sched).astype(int)

    blocks, labels = [], []
    for j in ROUNDS[:-1]:
        # A round is "at risk" if the fight reached it and could have gone
        # past it. The final scheduled round asks no question: a finish
        # that gets there ends there.
        live = (end >= j) & (sched > j)
        if not live.any():
            continue
        block = base[live].copy()
        block["round_index"] = float(j)
        blocks.append(block)
        labels.append((end[live] == j).astype(int))

    model = LGBMClassifier(objective="binary", random_state=seed, verbose=-1,
                           **(params or DEFAULT_PARAMS))
    model.fit(pd.concat(blocks, ignore_index=True), np.concatenate(labels))
    return model


def _chain(hazards: list[np.ndarray], sched: np.ndarray) -> np.ndarray:
    """Per-round hazards -> a distribution over rounds.

    `hazards[j]` is P(ends in round j+1 | still going). Reaching the final
    scheduled round forces a hazard of 1, so the remaining probability
    lands there and every later round gets exactly zero.
    """
    p = np.zeros((len(sched), len(ROUNDS)))
    surviving = np.ones(len(sched))
    for j, h in enumerate(hazards, start=1):
        h = np.where(sched <= j, 1.0, h)
        p[:, j - 1] = surviving * h
        surviving = surviving * (1.0 - h)
    p[:, len(ROUNDS) - 1] = surviving
    return p


def predict_rounds(model: LGBMClassifier, df: pd.DataFrame,
                   include_raw: bool = False) -> pd.DataFrame:
    """P(round | this fighter finishes by this method), one block of five
    columns per channel. Each block sums to 1 over the rounds the fight can
    reach and is exactly invariant to corner order (f1_ko_r2 <-> f2_ko_r2).
    """
    sched = scheduled_rounds(df)
    n = len(df)
    out = {}
    for channel in FINISH_CHANNELS:
        corner, group = channel.split("_")
        X = _design(df, np.full(n, corner == "f1"),
                    np.full(n, group == "ko"), include_raw)
        hazards = []
        for j in ROUNDS[:-1]:
            X["round_index"] = float(j)
            hazards.append(model.predict_proba(X)[:, 1])
        p = _chain(hazards, sched)
        for j, r in enumerate(ROUNDS):
            out[f"{channel}_r{r}"] = p[:, j]
    return pd.DataFrame(out, index=df.index)


def base_rate_rounds(train_df: pd.DataFrame, df: pd.DataFrame) -> pd.DataFrame:
    """The same shape as `predict_rounds`, from history alone: the observed
    round split of finishes with this method and this fight length.

    This is the round model's honest opponent — what a fan could quote from
    memory ("about half of three-round KOs come in the first"). Anything
    the model claims has to be measured against it.
    """
    train = trainable(train_df)
    groups = train["method"].map({"KO/TKO": "ko", "SUB": "sub"})
    lengths = scheduled_rounds(train)
    sched = scheduled_rounds(df)

    out = {}
    for channel in FINISH_CHANNELS:
        group = channel.split("_")[1]
        p = np.zeros((len(df), len(ROUNDS)))
        for length in np.unique(sched):
            rows = train[(groups == group).to_numpy() & (lengths == length)]
            counts = rows["end_round"].value_counts()
            share = np.array([counts.get(r, 0) for r in ROUNDS], dtype=float)
            if share.sum() == 0:  # no precedent: spread over reachable rounds
                share = np.array([r <= length for r in ROUNDS], dtype=float)
            p[sched == length] = share / share.sum()
        for j, r in enumerate(ROUNDS):
            out[f"{channel}_r{r}"] = p[:, j]
    return pd.DataFrame(out, index=df.index)


def blend(base_probs: pd.DataFrame, model_probs: pd.DataFrame,
          weight_base: float) -> pd.DataFrame:
    """Shrink the model's round distribution toward the historical base rate.

    Finish timing carries much less matchup signal than the winner does —
    on its own the hazard model is roughly level with the base rate inside
    a given fight length — so the honest production setting is a mixture,
    not a pure model. `weight_base` is chosen out of sample by
    `tune_base_weight`. Both inputs are already zero on unreachable rounds,
    so the mixture is too.
    """
    return base_probs * weight_base + model_probs * (1.0 - weight_base)


def channel_of_outcome(truth: pd.DataFrame) -> np.ndarray:
    """The finish channel each row actually produced, e.g. 'f2_ko'."""
    corner = np.where(truth["label"].to_numpy() == 1, "f1_", "f2_")
    return corner + truth["method"].map({"KO/TKO": "ko", "SUB": "sub"}).to_numpy()


def actual_channel_probs(probs: pd.DataFrame, truth: pd.DataFrame) -> pd.DataFrame:
    """Narrow a full prediction frame to the five round columns of the
    channel that actually happened — the only ones scoring can use."""
    return pd.DataFrame(
        [probs.loc[i, [f"{ch}_r{r}" for r in ROUNDS]].to_numpy()
         for i, ch in zip(truth.index, channel_of_outcome(truth))],
        index=truth.index, columns=[f"r{r}" for r in ROUNDS])


def walk_forward_predict(df: pd.DataFrame, windows: list[tuple[str, str]],
                         seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Round distributions for every fight in the windows, from a model and
    a base rate that each saw only earlier fights. Returns (model, base)."""
    cols = [f"{ch}_r{r}" for ch in FINISH_CHANNELS for r in ROUNDS]
    model_out = pd.DataFrame(np.nan, index=df.index, columns=cols)
    base_out = pd.DataFrame(np.nan, index=df.index, columns=cols)
    for start, end in windows:
        train = df[df["date"] < start]
        window = df[(df["date"] >= start) & (df["date"] <= end)]
        if len(trainable(train)) < 200 or len(window) == 0:
            continue
        model_out.loc[window.index] = predict_rounds(
            fit(train, seed=seed), window)[cols].to_numpy()
        base_out.loc[window.index] = base_rate_rounds(train, window)[cols].to_numpy()
    return model_out, base_out


def tune_base_weight(df: pd.DataFrame, windows: list[tuple[str, str]],
                     seed: int = 42) -> tuple[float, float]:
    """Pick the base-rate share by walk-forward log loss over the windows.

    Returns (weight, log loss at that weight). A weight near 1 would be the
    model admitting it has nothing to add beyond the era's base rate — a
    result worth reporting rather than hiding.
    """
    model_p, base_p = walk_forward_predict(df, windows, seed=seed)
    scored = trainable(df.loc[model_p.notna().all(axis=1)])
    if len(scored) == 0:
        return 1.0, float("nan")
    m = actual_channel_probs(model_p.loc[scored.index], scored)
    b = actual_channel_probs(base_p.loc[scored.index], scored)
    grid = np.linspace(0.0, 1.0, 21)
    losses = [round_log_loss(scored["end_round"], blend(b, m, w)) for w in grid]
    best = int(np.argmin(losses))
    return float(grid[best]), float(losses[best])


def joint_outcomes(method_probs: pd.DataFrame,
                   round_probs: pd.DataFrame) -> pd.DataFrame:
    """Method probabilities x conditional round probabilities.

    Decision keeps its method probability whole — there is no round to
    split it over — so each row sums to whatever the method probabilities
    summed to (1, after method.condition_on_win_prob).
    """
    out = {}
    for corner in ("f1", "f2"):
        for group in ("ko", "sub"):
            base = method_probs[f"{corner}_{group}"].to_numpy()
            for r in ROUNDS:
                out[f"{corner}_{group}_r{r}"] = (
                    base * round_probs[f"{corner}_{group}_r{r}"].to_numpy())
        out[f"{corner}_dec"] = method_probs[f"{corner}_dec"].to_numpy()
    return pd.DataFrame(out, index=method_probs.index)[outcome_columns()]


def ending_summary(joint: pd.DataFrame) -> pd.DataFrame:
    """Marginalize over who wins and how: P(the fight ends in round r) for
    each round, plus P(it reaches the scorecards)."""
    out = {
        f"r{r}": sum(joint[f"{c}_{g}_r{r}"]
                     for c in ("f1", "f2") for g in ("ko", "sub"))
        for r in ROUNDS
    }
    out["decision"] = joint["f1_dec"] + joint["f2_dec"]
    return pd.DataFrame(out, index=joint.index)


def select_outcome(joint_row, corner: str) -> dict:
    """Choose a coherent method first, then a round conditional on it.

    Taking the largest cell from the full method-by-round grid can call KO
    merely because its timing distribution is more concentrated, even when
    the *total* submission probability is larger.  The prediction question
    is hierarchical: first KO/submission/decision, then (for a finish) the
    most likely round given that method.
    """
    if corner not in ("f1", "f2"):
        raise ValueError("corner must be 'f1' or 'f2'")

    masses = {
        "ko": sum(float(joint_row[f"{corner}_ko_r{r}"]) for r in ROUNDS),
        "sub": sum(float(joint_row[f"{corner}_sub_r{r}"]) for r in ROUNDS),
        "dec": float(joint_row[f"{corner}_dec"]),
    }
    group = max(masses, key=masses.get)
    method_probability = masses[group]
    if group == "dec":
        return {
            "column": f"{corner}_dec",
            "method": "DEC",
            "round": None,
            "method_probability": method_probability,
            "round_probability": None,
            "exact_probability": method_probability,
        }

    round_values = {
        r: float(joint_row[f"{corner}_{group}_r{r}"]) for r in ROUNDS
    }
    round_number = max(round_values, key=round_values.get)
    exact_probability = round_values[round_number]
    conditional_round = (
        exact_probability / method_probability if method_probability > 0 else 0.0
    )
    return {
        "column": f"{corner}_{group}_r{round_number}",
        "method": "KO/TKO" if group == "ko" else "SUB",
        "round": round_number,
        "method_probability": method_probability,
        "round_probability": conditional_round,
        "exact_probability": exact_probability,
    }


def describe(column: str, f1: str, f2: str) -> str:
    """'f1_ko_r2' -> 'Jon Jones by KO/TKO, round 2'."""
    corner, rest = column.split("_", 1)
    name = f1 if corner == "f1" else f2
    if rest == "dec":
        return f"{name} by decision"
    group, rnd = rest.split("_r")
    return f"{name} by {'KO/TKO' if group == 'ko' else 'submission'}, round {rnd}"


def round_log_loss(y_round: pd.Series, probs: pd.DataFrame) -> float:
    """Log loss of the conditional round distribution on actual finishes,
    where `probs` holds the five columns for the channel that happened."""
    p = np.clip(probs.to_numpy(), 1e-12, 1.0)
    idx = [ROUNDS.index(int(r)) for r in y_round]
    return float(-np.mean(np.log(p[np.arange(len(idx)), idx])))

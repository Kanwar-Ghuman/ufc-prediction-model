"""Debut model uses the same corner-swap symmetry as the rest."""

import numpy as np
import pandas as pd

from octagon.features.build import swap_corners
from octagon.models import debut, debut_stack
from tests.test_models import synthetic_features

FAST_PARAMS = {"n_estimators": 40, "num_leaves": 7, "learning_rate": 0.2,
               "min_child_samples": 5}


def test_low_history_mask_is_symmetric_under_corner_swap():
    df = synthetic_features()
    mask = debut.low_history_mask(df)
    flipped = pd.DataFrame([swap_corners(r) for r in df.to_dict("records")])
    flipped_mask = debut.low_history_mask(flipped)
    np.testing.assert_array_equal(mask.to_numpy(), flipped_mask.to_numpy())


def test_debut_model_symmetrized_prediction_is_exactly_symmetric():
    # Every fighter's first few bouts are low-history by construction (n_fights
    # starts at 0), so these rows exist throughout the league regardless of
    # calendar date — no need for a temporal holdout in a pure symmetry check.
    df = synthetic_features()
    model = debut.fit(df, FAST_PARAMS)

    low_hist = debut.low_history_mask(df)
    sample = df[low_hist]
    assert len(sample) > 0, "synthetic league produced no low-history rows"

    p_ab = debut.predict_sym(model, sample)
    flipped = pd.DataFrame([swap_corners(r) for r in sample.to_dict("records")])
    p_ba = debut.predict_sym(model, flipped)
    np.testing.assert_allclose(p_ab, 1.0 - p_ba, atol=1e-12)


def test_debut_walk_forward_only_predicts_low_history_rows_inside_windows():
    df = synthetic_features()
    windows = [("2020-03-01", "2020-03-28")]
    params = {**FAST_PARAMS, "n_estimators": 20}
    pred = debut.walk_forward_predict(df, windows, params)

    low_hist = debut.low_history_mask(df)
    in_window = (df["date"] >= "2020-03-01") & (df["date"] <= "2020-03-28")

    assert pred[~in_window].isna().all()
    assert pred[in_window & ~low_hist].isna().all()
    assert pred[in_window & low_hist].notna().all()


def test_debut_stack_is_symmetric_and_no_intercept():
    """logit(1-p) = -logit(p) for both inputs -> the stack has no free
    intercept to break that, so it must hold for the combined output too."""
    rng = np.random.default_rng(0)
    n = 200
    y = rng.integers(0, 2, size=n).astype(float)
    p_blend = np.clip(rng.random(n), 0.05, 0.95)
    p_debut = np.clip(rng.random(n), 0.05, 0.95)

    a, b = debut_stack.fit_stack(y, p_blend, p_debut)
    p = debut_stack.predict_stack(a, b, p_blend, p_debut)
    p_flipped = debut_stack.predict_stack(a, b, 1 - p_blend, 1 - p_debut)
    np.testing.assert_allclose(p, 1.0 - p_flipped, atol=1e-9)

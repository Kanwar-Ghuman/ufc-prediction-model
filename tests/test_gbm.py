"""GBM + calibration tests. The symmetry requirement applies to EVERY model
(PRD 5.5): the GBM achieves it through augmentation + symmetrized inference
rather than architecture, and the test holds it to machine precision."""

import numpy as np
import pandas as pd

from octagon.features.build import swap_corners
from octagon.models import calibration, gbm
from tests.test_models import synthetic_features

FAST_PARAMS = {"n_estimators": 40, "num_leaves": 7, "learning_rate": 0.2,
               "min_child_samples": 5}


def test_gbm_symmetrized_prediction_is_exactly_symmetric():
    df = synthetic_features()
    model = gbm.fit(df[df["date"] < "2020-04-01"], FAST_PARAMS)
    sample = df[df["date"] >= "2020-04-01"]
    p_ab = gbm.predict_sym(model, sample)
    flipped = pd.DataFrame([swap_corners(r) for r in sample.to_dict("records")])
    p_ba = gbm.predict_sym(model, flipped)
    np.testing.assert_allclose(p_ab, 1.0 - p_ba, atol=1e-12)


def test_gbm_learns_obvious_signal():
    df = synthetic_features()
    model = gbm.fit(df[df["date"] < "2020-04-01"], FAST_PARAMS)
    holdout = df[df["date"] >= "2020-04-01"]
    p = gbm.predict_sym(model, holdout)
    assert ((p > 0.5) == (holdout["label"] == 1)).mean() > 0.7


def test_gbm_walk_forward_only_predicts_inside_windows():
    df = synthetic_features()
    pred = gbm.walk_forward_predict(df, [("2020-03-01", "2020-03-28")], FAST_PARAMS)
    in_window = (df["date"] >= "2020-03-01") & (df["date"] <= "2020-03-28")
    assert pred[in_window].notna().all()
    assert pred[~in_window].isna().all()


def test_isotonic_fixes_systematic_overconfidence():
    rng = np.random.default_rng(0)
    # A model that says 0.8/0.2 on fights that are really 0.6/0.4.
    p_raw = np.where(rng.random(4000) < 0.5, 0.8, 0.2)
    y = (rng.random(4000) < np.where(p_raw == 0.8, 0.6, 0.4)).astype(float)
    iso = calibration.fit_isotonic(y, p_raw)
    p_cal = calibration.apply(iso, p_raw)
    assert abs(p_cal[p_raw == 0.8].mean() - 0.6) < 0.05
    assert abs(p_cal[p_raw == 0.2].mean() - 0.4) < 0.05


def test_calibration_preserves_symmetry():
    """apply(1 - p) must equal 1 - apply(p), or calibrating would silently
    break the corner-invariance the models worked so hard for."""
    rng = np.random.default_rng(1)
    p_raw = rng.random(500)
    y = (rng.random(500) < p_raw).astype(float)
    iso = calibration.fit_isotonic(y, p_raw)
    grid = np.linspace(0.01, 0.99, 25)
    np.testing.assert_allclose(calibration.apply(iso, grid),
                               1.0 - calibration.apply(iso, 1.0 - grid), atol=1e-12)


def test_calibration_never_claims_certainty():
    # All-wins input would push naive isotonic to output 1.0 exactly.
    iso = calibration.fit_isotonic(np.ones(50), np.linspace(0.5, 1.0, 50))
    out = calibration.apply(iso, np.array([0.99]))
    assert 0.0 < out[0] < 1.0


def test_augmentation_doubles_and_flips():
    df = synthetic_features().head(10)
    X, y = gbm._augmented(gbm.feature_frame(df), df["label"].to_numpy())
    assert len(X) == 20 and len(y) == 20
    np.testing.assert_allclose(y[10:], 1 - y[:10])
    np.testing.assert_allclose(X["diff_elo"].iloc[10:].to_numpy(),
                               -X["diff_elo"].iloc[:10].to_numpy())
    # Context columns are swap-invariant and must NOT flip.
    np.testing.assert_allclose(X["scheduled_rounds"].iloc[10:].to_numpy(),
                               X["scheduled_rounds"].iloc[:10].to_numpy())

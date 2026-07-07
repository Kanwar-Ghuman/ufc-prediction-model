"""Method-of-victory model: class mapping, symmetry, conditioning."""

import numpy as np
import pandas as pd
import pytest

from octagon.features.build import swap_corners
from octagon.models import method
from tests.test_gbm import FAST_PARAMS
from tests.test_models import synthetic_features


def test_method_class_mapping():
    assert method.method_class(1, "KO/TKO") == "f1_ko"
    assert method.method_class(0, "SUB") == "f2_sub"
    assert method.method_class(1, "S-DEC") == "f1_dec"
    assert method.method_class(1, "DQ") is None      # untrainable ending
    assert method.method_class(None, "KO/TKO") is None


def _features_with_methods():
    df = synthetic_features()
    # Deterministic method pattern so the model has signal.
    rng = np.random.default_rng(2)
    df["method"] = rng.choice(["KO/TKO", "SUB", "U-DEC"], size=len(df))
    return df


def test_method_prediction_symmetry():
    df = _features_with_methods()
    model = method.fit(df[df["date"] < "2020-04-01"], FAST_PARAMS)
    sample = df[df["date"] >= "2020-04-01"]
    p_ab = method.predict_sym(model, sample)
    flipped = pd.DataFrame([swap_corners(r) for r in sample.to_dict("records")])
    p_ba = method.predict_sym(model, flipped)
    # Swapping corners must permute the classes exactly: f1_ko <-> f2_ko etc.
    np.testing.assert_allclose(p_ab["f1_ko"].to_numpy(), p_ba["f2_ko"].to_numpy(),
                               atol=1e-12)
    np.testing.assert_allclose(p_ab["f2_dec"].to_numpy(), p_ba["f1_dec"].to_numpy(),
                               atol=1e-12)


def test_probabilities_sum_to_one():
    df = _features_with_methods()
    model = method.fit(df[df["date"] < "2020-04-01"], FAST_PARAMS)
    p = method.predict_sym(model, df[df["date"] >= "2020-04-01"])
    np.testing.assert_allclose(p.sum(axis=1).to_numpy(), 1.0, atol=1e-9)


def test_condition_on_win_prob():
    probs = pd.DataFrame([[0.2, 0.1, 0.1, 0.3, 0.2, 0.1]], columns=method.CLASSES)
    out = method.condition_on_win_prob(probs, np.array([0.8]))
    # Fighter1's three classes now sum to the canonical 0.8, ratios preserved.
    assert out[["f1_ko", "f1_sub", "f1_dec"]].sum(axis=1).iat[0] == pytest.approx(0.8)
    assert out["f1_ko"].iat[0] == pytest.approx(0.8 * 0.2 / 0.4)
    assert out[["f2_ko", "f2_sub", "f2_dec"]].sum(axis=1).iat[0] == pytest.approx(0.2)


def test_multiclass_log_loss_known_value():
    probs = pd.DataFrame([[1 / 6] * 6], columns=method.CLASSES)
    assert method.multiclass_log_loss(pd.Series(["f1_ko"]), probs) == pytest.approx(
        np.log(6))

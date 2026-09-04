"""Blend behavior: the weight search must favor the better model."""

import numpy as np
import pytest

from octagon.models.ensemble import blend, tune_weight


def test_tune_weight_prefers_the_informative_model():
    rng = np.random.default_rng(0)
    y = (rng.random(2000) < 0.5).astype(float)
    p_good = np.clip(np.where(y == 1, 0.7, 0.3) + rng.normal(0, 0.05, 2000), 0.01, 0.99)
    p_noise = rng.uniform(0.3, 0.7, 2000)
    assert tune_weight(y, p_good, p_noise) >= 0.9   # ~all weight on the good model
    assert tune_weight(y, p_noise, p_good) <= 0.1   # and symmetric the other way


def test_blend_is_convex_combination():
    p1, p2 = np.array([0.8]), np.array([0.4])
    assert blend(p1, p2, 0.5)[0] == pytest.approx(0.6)
    assert blend(p1, p2, 1.0)[0] == pytest.approx(0.8)
    assert blend(p1, p2, 0.0)[0] == pytest.approx(0.4)


def test_blend_preserves_symmetry():
    # If both inputs flip (p -> 1-p), the blend must flip too.
    rng = np.random.default_rng(1)
    p1, p2 = rng.random(50), rng.random(50)
    np.testing.assert_allclose(blend(1 - p1, 1 - p2, 0.7),
                               1 - blend(p1, p2, 0.7), atol=1e-12)

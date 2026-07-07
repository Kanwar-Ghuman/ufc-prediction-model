"""Market-aware stack: exact symmetry and sane weighting."""

import numpy as np
import pytest

from octagon.models.market import fit_stack, predict_stack


def test_stack_symmetry_is_exact():
    rng = np.random.default_rng(0)
    m, s = rng.uniform(0.1, 0.9, 100), rng.uniform(0.1, 0.9, 100)
    p = predict_stack(1.1, 0.2, m, s)
    p_flipped = predict_stack(1.1, 0.2, 1 - m, 1 - s)
    np.testing.assert_allclose(p_flipped, 1 - p, atol=1e-12)


def test_stack_learns_to_trust_the_better_source():
    rng = np.random.default_rng(1)
    truth = rng.uniform(0.2, 0.8, 5000)
    y = (rng.random(5000) < truth).astype(float)
    p_market = np.clip(truth + rng.normal(0, 0.02, 5000), 0.05, 0.95)  # sharp
    p_skill = np.clip(truth + rng.normal(0, 0.25, 5000), 0.05, 0.95)   # noisy
    a, b = fit_stack(y, p_market, p_skill)
    assert a > 3 * b  # nearly all weight on the sharp source
    assert a > 0 and b >= 0


def test_stack_identity_when_market_is_perfect_and_skill_is_noise():
    rng = np.random.default_rng(2)
    truth = rng.uniform(0.2, 0.8, 8000)
    y = (rng.random(8000) < truth).astype(float)
    noise = rng.uniform(0.3, 0.7, 8000)
    a, b = fit_stack(y, truth, noise)
    assert a == pytest.approx(1.0, abs=0.15)  # calibrated input -> coef ~1
    assert abs(b) < 0.1                        # noise gets ~no weight
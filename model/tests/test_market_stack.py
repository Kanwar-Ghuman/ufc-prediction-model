"""Market-aware stack: exact symmetry and sane weighting."""

import numpy as np
import pytest

from octagon.models.market import (
    apply_market_layer, fit_stack, predict_stack, resolve_research_weight,
)


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


def test_market_layer_keeps_skill_when_unpriced():
    skill = np.array([0.62, 0.41])
    market = np.array([np.nan, np.nan])
    shipped, trapped = apply_market_layer(skill, market, [10, 10], [8, 8],
                                          stack=(1.0, 0.3))
    np.testing.assert_allclose(shipped, skill)
    assert not trapped.any()


def test_market_layer_traps_cepo_shaped_debut_and_stacks_the_rest():
    skill = np.array([0.495, 0.62])
    market = np.array([0.748, 0.55])
    shipped, trapped = apply_market_layer(
        skill, market, [0, 12], [4, 9], stack=(1.0, 0.0))
    assert trapped.tolist() == [True, False]
    assert shipped[0] == 0.5
    assert shipped[1] == pytest.approx(0.55)


def test_dual_debut_with_regional_careers_mixes_skill():
    """Contender Series: both debuts, thick regional records, priced fight.

    Stack with b=0 is pure market. Career-depth research weight should pull
    the shipped number off the board toward skill — the gap the old
    UFC-only history_confidence left on the table.
    """
    skill = np.array([0.70])
    market = np.array([0.55])
    shipped, trapped = apply_market_layer(
        skill, market, [0.0], [0.0],
        stack=(1.0, 0.0), research_weight=0.55,
        career1=[8.0], career2=[9.0])
    assert not trapped.any()
    assert shipped[0] > 0.55
    assert shipped[0] < 0.70


def test_dual_debut_without_regional_careers_stays_on_the_stack():
    skill = np.array([0.70])
    market = np.array([0.55])
    shipped, _ = apply_market_layer(
        skill, market, [0.0], [0.0],
        stack=(1.0, 0.0), research_weight=0.55)
    assert shipped[0] == pytest.approx(0.55)


def test_research_weight_prefers_the_frozen_artifact():
    assert resolve_research_weight({"research_weight": 0.4},
                                   {"model": {"research_weight": 0.55}}) == 0.4
    assert resolve_research_weight({}, {"model": {"research_weight": 0.55}}) == 0.55
    assert resolve_research_weight(None, None) == 0.0
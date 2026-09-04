"""Odds math against hand-computed values."""

import pytest

from octagon.betting.odds import (
    american_to_decimal,
    decimal_to_american,
    expected_value,
    implied_probability,
    kelly_stake,
    remove_vig,
)


def test_american_to_decimal_known_values():
    assert american_to_decimal(150) == pytest.approx(2.5)
    assert american_to_decimal(-200) == pytest.approx(1.5)
    assert american_to_decimal(100) == pytest.approx(2.0)
    assert american_to_decimal(-100) == pytest.approx(2.0)


def test_conversion_round_trip():
    for american in [-450, -150, -110, 110, 150, 450]:
        assert decimal_to_american(american_to_decimal(american)) == pytest.approx(american)


def test_american_zero_rejected():
    with pytest.raises(ValueError):
        american_to_decimal(0)


def test_implied_probability():
    assert implied_probability(2.0) == pytest.approx(0.5)
    assert implied_probability(4.0) == pytest.approx(0.25)
    with pytest.raises(ValueError):
        implied_probability(1.0)


def test_remove_vig_standard_juice():
    # -110/-110 both sides: implied 0.5238 each, fair value is a coin flip.
    p = implied_probability(american_to_decimal(-110))
    fair_a, fair_b = remove_vig(p, p)
    assert fair_a == pytest.approx(0.5)
    assert fair_a + fair_b == pytest.approx(1.0)


def test_remove_vig_preserves_ratio():
    fair_a, fair_b = remove_vig(0.60, 0.44)
    assert fair_a + fair_b == pytest.approx(1.0)
    assert fair_a / fair_b == pytest.approx(0.60 / 0.44)


def test_expected_value_breaks_even_at_implied_probability():
    assert expected_value(0.5, 2.0) == pytest.approx(0.0)
    assert expected_value(0.6, 2.0) == pytest.approx(0.2)   # generous price
    assert expected_value(0.4, 2.0) == pytest.approx(-0.2)  # bad price


def test_kelly_known_value():
    # p=0.6 at even odds: kelly = (0.6*2 - 1) / 1 = 0.2 of bankroll.
    assert kelly_stake(0.6, 2.0) == pytest.approx(0.2)
    # Quarter Kelly scales it down.
    assert kelly_stake(0.6, 2.0, fraction=0.25) == pytest.approx(0.05)


def test_kelly_never_negative():
    assert kelly_stake(0.4, 2.0) == 0.0          # negative edge -> no bet
    assert kelly_stake(0.9, 1.0) == 0.0          # degenerate odds -> no bet

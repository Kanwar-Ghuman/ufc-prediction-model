"""Odds math: conversions, vig removal, expected value, Kelly staking.

Educational module for the PAPER-TRADING simulator only — nothing in this
repo places real bets, and none of this is betting advice.

Vocabulary:
* Decimal odds `d`: total payout per 1 unit staked (stake included).
  d = 2.50 means a winning 1-unit bet returns 2.50 (profit 1.50).
* American odds: +150 means "win 150 on a 100 stake" (underdog);
  -200 means "stake 200 to win 100" (favorite).
* Implied probability 1/d: the win probability at which the bet breaks even.
* Vig (a.k.a. overround): the two sides' implied probabilities sum to MORE
  than 1 — that excess is the sportsbook's margin. To compare our model with
  the market's true opinion we must first strip it out.
"""

import math


def american_to_decimal(american: float) -> float:
    """+150 -> 2.5, -200 -> 1.5."""
    if american == 0:
        raise ValueError("American odds of 0 are undefined")
    if american > 0:
        return 1.0 + american / 100.0
    return 1.0 + 100.0 / abs(american)


def decimal_to_american(decimal: float) -> float:
    """2.5 -> +150, 1.5 -> -200. Requires d > 1 (d=1 pays nothing)."""
    if decimal <= 1.0:
        raise ValueError(f"Decimal odds must exceed 1.0, got {decimal}")
    if decimal >= 2.0:
        return (decimal - 1.0) * 100.0
    return -100.0 / (decimal - 1.0)


def implied_probability(decimal: float) -> float:
    """Break-even win probability of a bet at decimal odds d: 1/d."""
    if not math.isfinite(decimal) or decimal <= 1.0:
        raise ValueError(f"Decimal odds must be finite and exceed 1.0, got {decimal}")
    return 1.0 / decimal


def remove_vig(prob_a: float, prob_b: float) -> tuple[float, float]:
    """Normalize two implied probabilities so they sum to 1.

    Example: odds 1.91/1.91 imply 0.5236 + 0.5236 = 1.047 (4.7% vig).
    The fair market opinion is 0.5/0.5. This simple proportional method is
    the standard first-order correction.
    """
    total = prob_a + prob_b
    if total <= 0:
        raise ValueError("Probabilities must be positive")
    return prob_a / total, prob_b / total


def expected_value(model_prob: float, decimal: float) -> float:
    """EV per 1 unit staked: p*(d-1) - (1-p).

    Positive EV means our model thinks the price is generous. EV is exactly 0
    when model_prob equals the implied probability 1/d — the break-even line.
    """
    return model_prob * (decimal - 1.0) - (1.0 - model_prob)


def kelly_stake(model_prob: float, decimal: float, fraction: float = 1.0) -> float:
    """Kelly-optimal fraction of bankroll, scaled by `fraction` (e.g. 0.25).

    Full Kelly maximizes long-run bankroll growth *if the probabilities are
    right* — but model probabilities are noisy, and over-betting a wrong edge
    is ruinous, so practitioners bet a fraction of Kelly. Never negative:
    a bet with no edge gets a stake of 0.
    """
    b = decimal - 1.0  # net profit per unit staked
    if b <= 0:
        return 0.0
    kelly = (model_prob * decimal - 1.0) / b
    return max(0.0, kelly) * fraction

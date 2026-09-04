"""Market-trap guard: when to refuse a market-led debut pick.

Pinned to the Belgrade postmortem. The failure mode this catches is
shipping a 75% favorite on a debutant the skill model scores as a coin
flip (Čepo). The same card also had market-led debut picks that *hit*
(Oliveira, Milošević, Leka) — those had skill clearly off 0.5, so the
guard must leave them alone.
"""

from octagon.models.market import market_trap_abstain


def test_cepo_shaped_fight_is_abstained():
    """skill≈0.5, market 0.75, debutant — the Belgrade miss."""
    assert market_trap_abstain(0.495, 0.748, f1_n_fights=0, f2_n_fights=4)


def test_oliveira_shaped_fight_is_not_abstained():
    """skill clearly off 0.5 even though market disagrees harder."""
    assert not market_trap_abstain(0.562, 0.252, f1_n_fights=5, f2_n_fights=0)


def test_milosevic_shaped_fight_is_not_abstained():
    assert not market_trap_abstain(0.425, 0.777, f1_n_fights=0, f2_n_fights=3)


def test_leka_shaped_fight_is_not_abstained():
    assert not market_trap_abstain(0.449, 0.657, f1_n_fights=0, f2_n_fights=0)


def test_two_veterans_are_never_caught_by_the_debut_guard():
    assert not market_trap_abstain(0.50, 0.80, f1_n_fights=10, f2_n_fights=8)


def test_small_market_gap_is_not_a_trap():
    assert not market_trap_abstain(0.50, 0.55, f1_n_fights=0, f2_n_fights=4)

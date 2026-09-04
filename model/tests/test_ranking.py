"""Tapology-style ranking nudge for dual-debut (DWCS) fights."""

import math
from pathlib import Path

import pytest

from octagon.models.market import apply_ranking_nudge, ranking_logodds
from octagon.predict import load_card


def test_better_rank_number_favours_that_corner():
    """Lower Tapology rank is better — #21 vs #53 should help fighter 1."""
    delta = ranking_logodds(21, 53)
    assert delta > 0
    flipped = ranking_logodds(53, 21)
    assert flipped == pytest.approx(-delta)


def test_equal_ranks_are_a_wash():
    assert ranking_logodds(60, 60) == pytest.approx(0.0)


def test_missing_or_invalid_ranks_are_zero():
    assert ranking_logodds(None, 91) == 0.0
    assert ranking_logodds(124, None) == 0.0
    assert ranking_logodds(0, 91) == 0.0
    assert ranking_logodds(-10, 91) == 0.0


def test_ranking_nudge_moves_a_dual_debut_and_leaves_veterans():
    p, note = apply_ranking_nudge(0.50, 60, 124, n1=0, n2=0)
    assert p > 0.50
    assert note is not None
    assert "#60" in note and "#124" in note

    untouched, silent = apply_ranking_nudge(0.50, 60, 124, n1=8, n2=10)
    assert untouched == pytest.approx(0.50)
    assert silent is None


def test_ranking_nudge_is_antisymmetric():
    a, _ = apply_ranking_nudge(0.55, 21, 53, n1=0, n2=0)
    b, _ = apply_ranking_nudge(0.45, 53, 21, n1=0, n2=0)
    assert b == pytest.approx(1.0 - a, abs=1e-9)


def test_ranking_nudge_is_capped():
    """A #1 vs #500 gap must not overwrite the skill model."""
    p, _ = apply_ranking_nudge(0.50, 1, 500, n1=0, n2=0)
    assert 0.50 < p < 0.70
    assert math.isfinite(p)


def test_load_card_reads_optional_rankings(tmp_path: Path):
    path = tmp_path / "card.yaml"
    path.write_text(
        "date: '2026-09-01'\n"
        "event: Test\n"
        "fights:\n"
        "  - fighter1: Alice\n"
        "    fighter2: Bob\n"
        "    weight_class: Lightweight\n"
        "    ranking: [60, 124]\n"
        "    region: [Europe, South America]\n",
        encoding="utf-8")
    _, _, fights = load_card(path)
    assert fights[0].ranking == (60, 124)
    assert fights[0].region == ("Europe", "South America")

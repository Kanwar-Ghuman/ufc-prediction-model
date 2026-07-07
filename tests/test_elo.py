"""Elo invariants. The point-in-time test is a leakage guard — never delete it."""

import pytest

from octagon.features.elo import Elo, expected_score, run_history


def test_expected_score_symmetry():
    assert expected_score(1500, 1500) == pytest.approx(0.5)
    # P(A beats B) + P(B beats A) must always be 1.
    assert expected_score(1600, 1450) + expected_score(1450, 1600) == pytest.approx(1.0)


def test_expected_score_400_point_gap_is_10_to_1():
    assert expected_score(1900, 1500) == pytest.approx(10 / 11)


def test_update_is_zero_sum():
    book = Elo()
    book.update("A", "B", 1.0)
    assert book.get("A") + book.get("B") == pytest.approx(2 * book.initial)


def test_upset_transfers_more_points():
    book = Elo()
    book.ratings = {"favorite": 1700.0, "underdog": 1400.0}
    book.update("favorite", "underdog", 0.0)  # underdog wins
    upset_gain = book.get("underdog") - 1400.0

    book.ratings = {"favorite": 1700.0, "underdog": 1400.0}
    book.update("favorite", "underdog", 1.0)  # expected result
    expected_gain = book.get("favorite") - 1700.0

    assert upset_gain > expected_gain > 0


def test_run_history_returns_pre_fight_ratings():
    """The leakage guard: features must be the ratings BEFORE each fight."""
    fights = [
        ("A", "B", "fighter1"),  # both debut at 1500
        ("A", "C", "fighter1"),  # A enters above 1500, C at 1500
        ("B", "A", "fighter1"),  # B enters below 1500 (lost to A), A above
    ]
    pre = run_history(fights)
    assert pre[0] == (1500.0, 1500.0)
    assert pre[1][0] > 1500.0 and pre[1][1] == 1500.0
    assert pre[2][0] < 1500.0 and pre[2][1] > 1500.0


def test_run_history_no_contest_leaves_ratings_untouched():
    pre = run_history([("A", "B", "nc"), ("A", "B", "fighter1")])
    assert pre[1] == (1500.0, 1500.0)


def test_run_history_draw_moves_unequal_ratings_together():
    book = Elo()
    book.ratings = {"A": 1700.0, "B": 1400.0}
    book.update("A", "B", 0.5)
    # A draw is a below-expectation result for the higher-rated fighter.
    assert book.get("A") < 1700.0
    assert book.get("B") > 1400.0

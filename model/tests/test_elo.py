"""Elo pre-fight ratings ignore later results."""

import pytest

from octagon.features.elo import Elo, expected_score, experience_multiplier, run_history


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


def test_per_corner_multipliers_move_the_green_fighter_further():
    book = Elo(k=32.0)
    book.update("rookie", "veteran", 1.0, k_multiplier_a=2.0, k_multiplier_b=1.0)
    assert book.get("rookie") - book.initial == pytest.approx(32.0)
    assert book.initial - book.get("veteran") == pytest.approx(16.0)


def test_experience_multiplier_decays_to_one_and_is_off_by_default():
    assert experience_multiplier(0, boost=0.0) == 1.0
    assert experience_multiplier(0, boost=1.0) == pytest.approx(2.0)
    assert experience_multiplier(3, boost=1.0) == pytest.approx(1.5)
    assert experience_multiplier(6, boost=1.0) == 1.0
    assert experience_multiplier(40, boost=1.0) == 1.0


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


def test_select_k_ignores_labels_after_train_end():
    """Poisoning the valid era must not change the train-era K choice."""
    from octagon.features.elo import select_k

    train = [
        ("2020-01-01", "A", "B", "fighter1"),
        ("2020-06-01", "A", "C", "fighter1"),
        ("2021-01-01", "C", "B", "fighter2"),
        ("2021-07-01", "A", "B", "fighter2"),
    ]
    # Valid-era labels that would pull K if we peeked.
    poisoned = train + [
        ("2022-06-01", "A", "C", "fighter2"),
        ("2023-01-01", "B", "C", "fighter1"),
        ("2023-07-01", "A", "B", "fighter2"),
    ]
    k_train, _ = select_k(train, "2021-12-31")
    k_poisoned, _ = select_k(poisoned, "2021-12-31")
    assert k_train == k_poisoned

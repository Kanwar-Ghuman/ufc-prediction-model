"""Metric implementations against hand-computed values."""

import math

import numpy as np
import pytest

from octagon.eval.metrics import accuracy, brier, ece, log_loss, roc_auc


def test_log_loss_of_coin_flip_is_ln2():
    assert log_loss([1, 0, 1], [0.5, 0.5, 0.5]) == pytest.approx(math.log(2))


def test_log_loss_punishes_confident_wrongness():
    confident_wrong = log_loss([1], [0.1])
    meek_wrong = log_loss([1], [0.45])
    assert confident_wrong == pytest.approx(-math.log(0.1))
    assert confident_wrong > meek_wrong


def test_log_loss_survives_extreme_probabilities():
    assert np.isfinite(log_loss([1, 0], [1.0, 0.0]))


def test_brier_known_values():
    assert brier([1, 0], [0.5, 0.5]) == pytest.approx(0.25)  # always-0.5 scores 0.25
    assert brier([1, 0], [1.0, 0.0]) == pytest.approx(0.0)
    assert brier([1], [0.7]) == pytest.approx(0.09)


def test_accuracy_gives_half_credit_at_exactly_half():
    assert accuracy([1, 0], [0.5, 0.5]) == pytest.approx(0.5)
    assert accuracy([1, 0, 1], [0.9, 0.2, 0.4]) == pytest.approx(2 / 3)


def test_ece_zero_when_perfectly_calibrated():
    # Five fights at 0.2: exactly one hits -> bin gap |0.2 - 0.2| = 0.
    assert ece([0, 0, 0, 0, 1], [0.2] * 5) == pytest.approx(0.0)


def test_ece_catches_overconfidence():
    # Model says 0.9 but wins only half of them.
    assert ece([1, 0, 1, 0], [0.9] * 4) == pytest.approx(0.4)


def test_roc_auc_perfect_ranking():
    assert roc_auc([1, 1, 0, 0], [0.9, 0.8, 0.3, 0.2]) == pytest.approx(1.0)

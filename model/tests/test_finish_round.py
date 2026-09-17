"""Round model: orientation, masking, joint distribution."""

from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from octagon.features.build import build_feature_rows, swap_corners
from octagon.models import finish_round, method
from tests.test_features import make_bout
from tests.test_gbm import FAST_PARAMS


def _finish_features(n_days: int = 240) -> pd.DataFrame:
    """A league where the top half of the roster finishes in round 1 and
    the bottom half grinds to round 3 — so 'which round' is learnable."""
    fighters = [f"F{i}" for i in range(8)]
    rng = np.random.default_rng(3)
    bouts = []
    for day in range(1, n_days + 1):
        a, b = map(int, rng.choice(8, size=2, replace=False))
        winner = min(a, b)
        end_round = 1 if winner < 4 else 3
        bouts.append(make_bout(
            day, str(date(2020, 1, 1) + timedelta(days=day - 1)),
            fighters[a], fighters[b],
            winner="fighter1" if a < b else "fighter2",
            method="KO/TKO" if winner % 2 == 0 else "SUB",
            end_round=end_round, duration_s=300 * end_round))
    return pd.DataFrame(build_feature_rows(bouts, {}))


def _fitted(df: pd.DataFrame):
    return finish_round.fit(df[df["date"] < "2020-06-01"], FAST_PARAMS)


def _channel_of_winner(frame: pd.DataFrame) -> list[str]:
    corners = np.where(frame["label"] == 1, "f1", "f2")
    groups = frame["method"].map({"KO/TKO": "ko", "SUB": "sub"}).to_numpy()
    return [f"{c}_{g}" for c, g in zip(corners, groups)]


def test_trainable_keeps_only_finishes_with_a_round():
    df = _finish_features(40)
    df.loc[df.index[:5], "method"] = "U-DEC"      # decisions have no round
    df.loc[df.index[5:8], "end_round"] = np.nan   # unknown round is unusable
    train = finish_round.trainable(df)
    assert set(train["method"]) <= set(finish_round.FINISH_METHODS)
    assert train["end_round"].notna().all()
    assert len(train) == len(df) - 8


def test_round_prediction_permutes_exactly_under_a_corner_swap():
    df = _finish_features()
    model = _fitted(df)
    sample = df[df["date"] >= "2020-06-01"]
    p_ab = finish_round.predict_rounds(model, sample)
    flipped = pd.DataFrame([swap_corners(r) for r in sample.to_dict("records")])
    p_ba = finish_round.predict_rounds(model, flipped)
    for r in finish_round.ROUNDS:
        np.testing.assert_allclose(p_ab[f"f1_ko_r{r}"].to_numpy(),
                                   p_ba[f"f2_ko_r{r}"].to_numpy(), atol=1e-12)
        np.testing.assert_allclose(p_ab[f"f2_sub_r{r}"].to_numpy(),
                                   p_ba[f"f1_sub_r{r}"].to_numpy(), atol=1e-12)


def test_each_channel_is_a_probability_distribution():
    df = _finish_features()
    p = finish_round.predict_rounds(_fitted(df), df[df["date"] >= "2020-06-01"])
    for channel in finish_round.FINISH_CHANNELS:
        block = p[[f"{channel}_r{r}" for r in finish_round.ROUNDS]]
        np.testing.assert_allclose(block.sum(axis=1).to_numpy(), 1.0, atol=1e-9)
        assert (block.to_numpy() >= 0).all()


def test_rounds_the_fight_cannot_reach_are_exactly_zero():
    df = _finish_features()
    model = _fitted(df)
    sample = df[df["date"] >= "2020-06-01"].copy()
    sample["scheduled_rounds"] = np.where(
        np.arange(len(sample)) % 2 == 0, 3.0, 5.0)
    p = finish_round.predict_rounds(model, sample)
    three = sample["scheduled_rounds"].to_numpy() == 3
    for channel in finish_round.FINISH_CHANNELS:
        for r in (4, 5):
            assert (p.loc[three, f"{channel}_r{r}"] == 0.0).all()
    # A championship fight keeps all five rounds live, not rounded away.
    assert (p.loc[~three, [f"f1_ko_r{r}" for r in (4, 5)]].sum(axis=1) > 0).all()


def test_unscheduled_fights_fall_back_to_three_rounds():
    df = _finish_features()
    sample = df[df["date"] >= "2020-06-01"].copy()
    sample["scheduled_rounds"] = np.nan
    p = finish_round.predict_rounds(_fitted(df), sample)
    assert (p[[f"f1_ko_r{r}" for r in (4, 5)]] == 0.0).all().all()


def test_chain_turns_hazards_into_a_distribution():
    """The hazard recursion is the whole reason fight length is structural
    rather than learned, so pin its arithmetic down by hand."""
    hazards = [np.array([0.5, 0.5]), np.array([0.5, 0.5]),
               np.array([0.5, 0.5]), np.array([0.5, 0.5])]
    p = finish_round._chain(hazards, np.array([3.0, 5.0]))
    # Three-rounder: 0.5, then 0.25, and round 3 absorbs the remaining 0.25.
    np.testing.assert_allclose(p[0], [0.5, 0.25, 0.25, 0.0, 0.0])
    # Five-rounder: the halving continues and round 5 absorbs the rest.
    np.testing.assert_allclose(p[1], [0.5, 0.25, 0.125, 0.0625, 0.0625])
    np.testing.assert_allclose(p.sum(axis=1), 1.0)


def test_base_rate_reproduces_the_historical_split():
    df = _finish_features()
    train = df[df["date"] < "2020-06-01"]
    sample = df[df["date"] >= "2020-06-01"]
    p = finish_round.base_rate_rounds(train, sample)

    ko = finish_round.trainable(train)
    ko = ko[ko["method"] == "KO/TKO"]
    expected_r1 = (ko["end_round"] == 1).mean()
    np.testing.assert_allclose(p["f1_ko_r1"].to_numpy(), expected_r1, atol=1e-12)
    np.testing.assert_allclose(p["f2_ko_r1"].to_numpy(), expected_r1, atol=1e-12)
    for channel in finish_round.FINISH_CHANNELS:
        block = p[[f"{channel}_r{r}" for r in finish_round.ROUNDS]]
        np.testing.assert_allclose(block.sum(axis=1).to_numpy(), 1.0, atol=1e-12)


def test_blending_toward_the_base_rate_stays_a_distribution():
    df = _finish_features()
    train = df[df["date"] < "2020-06-01"]
    sample = df[df["date"] >= "2020-06-01"]
    mixed = finish_round.blend(finish_round.base_rate_rounds(train, sample),
                               finish_round.predict_rounds(_fitted(df), sample), 0.6)
    for channel in finish_round.FINISH_CHANNELS:
        block = mixed[[f"{channel}_r{r}" for r in finish_round.ROUNDS]]
        np.testing.assert_allclose(block.sum(axis=1).to_numpy(), 1.0, atol=1e-9)
        assert (block.to_numpy() >= 0).all()


def test_tuned_base_weight_is_a_valid_share():
    df = _finish_features(400)  # enough history to clear the model's minimum
    weight, loss = finish_round.tune_base_weight(
        df, [("2020-10-01", "2020-10-31"), ("2020-11-01", "2020-11-30")])
    assert 0.0 <= weight <= 1.0
    assert loss > 0.0


def test_model_learns_which_fighters_finish_early():
    df = _finish_features()
    model = _fitted(df)
    holdout = finish_round.trainable(df[df["date"] >= "2020-06-01"])
    p = finish_round.predict_rounds(model, holdout)
    p_r1 = np.array([p.loc[i, f"{ch}_r1"]
                     for i, ch in zip(holdout.index, _channel_of_winner(holdout))])
    fast = holdout["end_round"].to_numpy() == 1
    assert p_r1[fast].mean() > p_r1[~fast].mean() + 0.2


def test_joint_outcomes_sum_to_one_and_keep_the_method_marginals():
    df = _finish_features()
    sample = df[df["date"] >= "2020-06-01"]
    rounds = finish_round.predict_rounds(_fitted(df), sample)
    methods = pd.DataFrame(
        np.tile([0.2, 0.1, 0.2, 0.15, 0.15, 0.2], (len(sample), 1)),
        columns=method.CLASSES, index=sample.index)
    joint = finish_round.joint_outcomes(methods, rounds)

    assert list(joint.columns) == finish_round.outcome_columns()
    np.testing.assert_allclose(joint.sum(axis=1).to_numpy(), 1.0, atol=1e-9)
    for corner in ("f1", "f2"):
        for group in ("ko", "sub"):
            spread = joint[[f"{corner}_{group}_r{r}" for r in finish_round.ROUNDS]]
            np.testing.assert_allclose(spread.sum(axis=1).to_numpy(),
                                       methods[f"{corner}_{group}"].to_numpy(),
                                       atol=1e-9)
        # A decision is one outcome, not five — it passes through untouched.
        np.testing.assert_allclose(joint[f"{corner}_dec"].to_numpy(),
                                   methods[f"{corner}_dec"].to_numpy(), atol=1e-12)


def test_ending_summary_marginalizes_over_fighter_and_method():
    joint = pd.DataFrame([dict.fromkeys(finish_round.outcome_columns(), 0.0)])
    joint.loc[0, "f1_ko_r1"] = 0.3
    joint.loc[0, "f2_sub_r1"] = 0.1
    joint.loc[0, "f1_sub_r3"] = 0.2
    joint.loc[0, "f1_dec"] = 0.25
    joint.loc[0, "f2_dec"] = 0.15
    summary = finish_round.ending_summary(joint)
    assert summary["r1"].iat[0] == pytest.approx(0.4)
    assert summary["r3"].iat[0] == pytest.approx(0.2)
    assert summary["decision"].iat[0] == pytest.approx(0.4)
    assert summary.sum(axis=1).iat[0] == pytest.approx(1.0)


def test_describe_reads_as_english():
    assert finish_round.describe("f1_ko_r2", "Jones", "Gane") == \
        "Jones by KO/TKO, round 2"
    assert finish_round.describe("f2_sub_r5", "Jones", "Gane") == \
        "Gane by submission, round 5"
    assert finish_round.describe("f2_dec", "Jones", "Gane") == "Gane by decision"


def test_select_outcome_chooses_marginal_method_before_conditional_round():
    """Three smaller SUB cells must beat one concentrated but smaller KO mass."""
    row = dict.fromkeys(finish_round.outcome_columns(), 0.0)
    row.update({
        "f1_ko_r1": 0.20,
        "f1_sub_r1": 0.12,
        "f1_sub_r2": 0.12,
        "f1_sub_r3": 0.12,
        "f1_dec": 0.14,
    })
    selected = finish_round.select_outcome(pd.Series(row), "f1")
    assert selected["column"] == "f1_sub_r1"
    assert selected["method"] == "SUB"
    assert selected["round"] == 1
    assert selected["method_probability"] == pytest.approx(0.36)
    assert selected["round_probability"] == pytest.approx(1 / 3)
    assert selected["exact_probability"] == pytest.approx(0.12)


def test_select_outcome_has_no_round_for_decision():
    row = dict.fromkeys(finish_round.outcome_columns(), 0.0)
    row.update({"f2_ko_r1": 0.1, "f2_sub_r2": 0.2, "f2_dec": 0.3})
    selected = finish_round.select_outcome(pd.Series(row), "f2")
    assert selected["column"] == "f2_dec"
    assert selected["method"] == "DEC"
    assert selected["round"] is None
    assert selected["round_probability"] is None


def test_round_log_loss_of_a_uniform_guess():
    probs = pd.DataFrame([[1 / 3, 1 / 3, 1 / 3, 0.0, 0.0]],
                         columns=[f"r{r}" for r in finish_round.ROUNDS])
    assert finish_round.round_log_loss(pd.Series([2]), probs) == pytest.approx(
        np.log(3))

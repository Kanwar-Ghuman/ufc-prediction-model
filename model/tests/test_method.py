"""Method-of-victory model: how the winner wins, not who wins.

The 6-class joint (f1_ko, f1_sub, ...) spent its capacity on the winner
and then split finish probability across KO and submission, so a fight
that was 55% to finish still 'called' a decision. These tests pin the
replacement: a 3-class model of the winner's method, oriented so the
winner sits in corner 1, with swap-invariance on the 6-class output.
"""

from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from octagon.features.build import build_feature_rows, swap_corners
from octagon.models import method
from tests.test_features import make_bout
from tests.test_gbm import FAST_PARAMS


def _method_features(n_days: int = 240) -> pd.DataFrame:
    """Fighters 0-3 finish by KO when they win; 4-7 grind to a decision."""
    fighters = [f"F{i}" for i in range(8)]
    rng = np.random.default_rng(3)
    bouts = []
    for day in range(1, n_days + 1):
        a, b = map(int, rng.choice(8, size=2, replace=False))
        winner = min(a, b)  # lower index always wins, so 0-3 accumulate KO wins
        how = "KO/TKO" if winner < 4 else "U-DEC"
        end_round = 1 if how == "KO/TKO" else 3
        bouts.append(make_bout(
            day, str(date(2020, 1, 1) + timedelta(days=day - 1)),
            fighters[a], fighters[b],
            winner="fighter1" if a == winner else "fighter2",
            method=how, end_round=end_round,
            duration_s=60 if how == "KO/TKO" else 900))
    return pd.DataFrame(build_feature_rows(bouts, {}))


def test_each_corner_is_a_how_given_win_distribution():
    """predict_sym answers P(KO/sub/dec | this corner wins), so each trio sums to 1."""
    df = _method_features(80)
    model = method.fit(df[df["date"] < "2020-03-01"], FAST_PARAMS)
    p = method.predict_sym(model, df[df["date"] >= "2020-03-01"])
    np.testing.assert_allclose(p[method.CLASSES[:3]].sum(axis=1), 1.0, atol=1e-9)
    np.testing.assert_allclose(p[method.CLASSES[3:]].sum(axis=1), 1.0, atol=1e-9)


def test_method_prediction_permutes_exactly_under_a_corner_swap():
    df = _method_features()
    model = method.fit(df[df["date"] < "2020-06-01"], FAST_PARAMS)
    sample = df[df["date"] >= "2020-06-01"]
    p_ab = method.predict_sym(model, sample)
    flipped = pd.DataFrame([swap_corners(r) for r in sample.to_dict("records")])
    p_ba = method.predict_sym(model, flipped)
    for group in method.GROUPS:
        np.testing.assert_allclose(p_ab[f"f1_{group}"].to_numpy(),
                                   p_ba[f"f2_{group}"].to_numpy(), atol=1e-12)
        np.testing.assert_allclose(p_ab[f"f2_{group}"].to_numpy(),
                                   p_ba[f"f1_{group}"].to_numpy(), atol=1e-12)


def test_a_finisher_is_called_to_finish_when_they_win():
    """The whole point: KO artists must not be predicted as decision grinders."""
    df = _method_features()
    model = method.fit(df[df["date"] < "2020-06-01"], FAST_PARAMS)
    holdout = df[df["date"] >= "2020-06-01"].copy()
    p = method.predict_sym(model, holdout)
    # Corner 1 is the favourite in this synthetic (lower index wins). When
    # that favourite is a KO artist, P(KO | they win) should dominate.
    knockout = holdout["f1_name"].str.extract(r"(\d+)", expand=False).astype(int) < 4
    assert p.loc[knockout[knockout].index, "f1_ko"].mean() > 0.55
    assert p.loc[~knockout, "f1_dec"].mean() > 0.55


def test_condition_on_win_prob_keeps_the_how_split():
    how = pd.DataFrame(
        [[0.6, 0.1, 0.3, 0.2, 0.5, 0.3]],
        columns=method.CLASSES)
    out = method.condition_on_win_prob(how, np.array([0.8]))
    assert out.iloc[0, :3].sum() == pytest.approx(0.8)
    assert out.iloc[0, 3:].sum() == pytest.approx(0.2)
    assert out["f1_ko"].iat[0] / 0.8 == pytest.approx(0.6)
    assert out["f2_sub"].iat[0] / 0.2 == pytest.approx(0.5)


def test_base_rate_is_how_given_win_and_symmetric():
    train = pd.DataFrame({
        "label": [1, 0, 1, 0] * 15,
        "method": ["KO/TKO", "U-DEC", "SUB", "KO/TKO"] * 15,
        "weight_class": ["Heavyweight"] * 60,
        "scheduled_rounds": [3] * 60,
        "date": ["2024-01-01"] * 60,
    })
    upcoming = pd.DataFrame({
        "weight_class": ["Heavyweight"], "scheduled_rounds": [3],
    })
    base = method.base_rate_methods(method.trainable(train), upcoming)
    row = base.iloc[0]
    assert abs(row[method.CLASSES[:3]].sum() - 1.0) < 1e-9
    assert abs(row[method.CLASSES[3:]].sum() - 1.0) < 1e-9
    for group in method.GROUPS:
        assert abs(row[f"f1_{group}"] - row[f"f2_{group}"]) < 1e-12


def test_base_rate_prefers_the_recent_era():
    """A division that used to go the distance but now finishes should not
    be priced off 2016."""
    old = pd.DataFrame({
        "label": [1] * 80,
        "method": ["U-DEC"] * 80,
        "weight_class": ["Welterweight"] * 80,
        "scheduled_rounds": [3] * 80,
        "date": ["2016-01-01"] * 80,
    })
    recent = pd.DataFrame({
        "label": [1] * 80,
        "method": ["KO/TKO"] * 80,
        "weight_class": ["Welterweight"] * 80,
        "scheduled_rounds": [3] * 80,
        "date": ["2024-01-01"] * 80,
    })
    train = pd.concat([old, recent], ignore_index=True)
    upcoming = pd.DataFrame({
        "weight_class": ["Welterweight"], "scheduled_rounds": [3],
    })
    base = method.base_rate_methods(method.trainable(train), upcoming)
    assert base["f1_ko"].iat[0] > 0.7

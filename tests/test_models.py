"""Model-level tests. The symmetry test here is the PRD 5.5 requirement:
predict(A, B) must equal 1 - predict(B, A) — held to machine precision
because the logistic reference model is antisymmetric by architecture."""

import numpy as np
import pandas as pd
import pytest

from octagon.features.build import build_feature_rows, swap_corners
from octagon.models import baselines, logistic
from tests.test_features import make_bout


def synthetic_features(n_days: int = 120) -> pd.DataFrame:
    """A little league of 8 fighters with deterministic outcomes so the
    model has real signal to find (lower-numbered fighters are better)."""
    fighters = [f"F{i}" for i in range(8)]
    rng = np.random.default_rng(0)
    bouts = []
    for day in range(1, n_days + 1):
        a, b = map(int, rng.choice(8, size=2, replace=False))
        bouts.append(make_bout(
            day, f"2020-{(day - 1) // 28 + 1:02d}-{(day - 1) % 28 + 1:02d}",
            fighters[a], fighters[b],
            winner="fighter1" if a < b else "fighter2"))
    return pd.DataFrame(build_feature_rows(bouts, {}))


def test_model_symmetry_predict_ab_equals_one_minus_predict_ba():
    df = synthetic_features()
    model = logistic.fit(df[df["date"] < "2020-04-01"])
    sample = df[df["date"] >= "2020-04-01"]
    p_ab = logistic.predict(model, sample)
    flipped = pd.DataFrame([swap_corners(r) for r in sample.to_dict("records")])
    p_ba = logistic.predict(model, flipped)
    np.testing.assert_allclose(p_ab, 1.0 - p_ba, atol=1e-12)


def test_model_learns_obvious_signal():
    df = synthetic_features()
    model = logistic.fit(df[df["date"] < "2020-04-01"])
    holdout = df[df["date"] >= "2020-04-01"]
    p = logistic.predict(model, holdout)
    hit = ((p > 0.5) == (holdout["label"] == 1)).mean()
    assert hit > 0.7  # deterministic league -> should be easy


def test_walk_forward_only_predicts_inside_windows():
    df = synthetic_features()
    pred = logistic.walk_forward_predict(df, [("2020-03-01", "2020-03-28")])
    in_window = (df["date"] >= "2020-03-01") & (df["date"] <= "2020-03-28")
    assert pred[in_window].notna().all()
    assert pred[~in_window].isna().all()


def test_coin_flip_baseline():
    df = synthetic_features()
    assert (baselines.coin_flip(df) == 0.5).all()


def test_better_record_baseline_picks_the_veteran():
    bouts = [
        make_bout(1, "2020-01-01", "Alice", "Bob"),          # Alice wins
        make_bout(2, "2020-02-01", "Alice", "Carol"),        # Alice wins again
        make_bout(3, "2020-03-01", "Alice", "Dana"),
    ]
    df = pd.DataFrame(build_feature_rows(bouts, {}))
    row = df[df["fight_id"] == 3]
    p = baselines.better_record(row)[0]
    # Alice (2-0) must be picked over debutant Dana regardless of corner swap.
    alice_is_f1 = row["f1_name"].iat[0] == "Alice"
    assert p == (1.0 if alice_is_f1 else 0.0)


def test_market_baseline_only_where_priced():
    df = synthetic_features()
    p = baselines.market(df)
    assert np.isnan(p).all()  # synthetic bouts carry no odds


def test_market_baseline_removes_vig():
    bout = make_bout(1, "2020-01-01", "Alice", "Bob")
    bout.odds1, bout.odds2 = 1.91, 1.91  # -110 both sides
    df = pd.DataFrame(build_feature_rows([bout], {}))
    p1 = baselines.market(df)[0]
    assert p1 == pytest.approx(0.5)

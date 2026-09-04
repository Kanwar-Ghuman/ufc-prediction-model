"""Symmetrized SHAP must be an exact decomposition of the symmetrized
log-odds score — otherwise the explanations describe a model we don't use."""

import numpy as np

from octagon.models import gbm
from octagon.eval.explain import _flipped, shap_symmetrized
from tests.test_gbm import FAST_PARAMS
from tests.test_models import synthetic_features


def test_symmetrized_shap_adds_up_to_the_symmetrized_score():
    df = synthetic_features()
    model = gbm.fit(df[df["date"] < "2020-04-01"], FAST_PARAMS)
    sample = df[df["date"] >= "2020-04-01"]

    contributions, X = shap_symmetrized(model, sample)
    raw = model.booster_.predict(X, raw_score=True)
    raw_flipped = model.booster_.predict(_flipped(X), raw_score=True)
    expected_score = (raw - raw_flipped) / 2.0  # base values cancel to 0

    np.testing.assert_allclose(contributions.sum(axis=1).to_numpy(),
                               expected_score, atol=1e-6)


def test_context_features_explain_no_corner_preference():
    """A title flag or weight class can't favor fighter1 or fighter2 — its
    symmetrized main effect must be tiny relative to the diff features."""
    df = synthetic_features()
    model = gbm.fit(df[df["date"] < "2020-04-01"], FAST_PARAMS)
    contributions, _ = shap_symmetrized(model, df[df["date"] >= "2020-04-01"])
    context_mass = contributions[["title_fight", "scheduled_rounds",
                                  "gender_num", "weight_class"]].abs().mean().sum()
    diff_mass = contributions[[c for c in contributions.columns
                               if c.startswith("diff_")]].abs().mean().sum()
    assert context_mass < 0.05 * max(diff_mass, 1e-9)

"""Market-aware stack (PRD 5.6) — the best predictor this project can build.

Architecture matters here. Feeding odds in as one feature among fifty
DILUTES them (most training rows are unpriced, and trees split on noisier
columns): that variant scored WORSE than the market alone. What works is
market-as-base: combine the two probabilities in log-odds space,

    p = sigmoid(a * logit(p_market) + b * logit(p_skill))

with (a, b) fit on train-era out-of-sample priced fights. Fitted values are
roughly a=1.06, b=0.17: take the market, sharpen it slightly (best-line
odds are a touch underconfident), add a whisper of skill.

Honesty rules, non-negotiable (PRD 5.6):
* Never report this model's numbers as "our model beat the odds" — it IS
  the odds, lightly seasoned.
* On validation it edges the market by ~0.003 log loss on 697 fights —
  inside this project's demonstrated noise band, and far smaller than the
  vig. It does not make betting profitable.

No intercept, so symmetry is exact: logit(1-p) = -logit(p), both inputs
negate under a corner swap, and the output flips to 1-p precisely.
"""

import numpy as np
from scipy.special import expit, logit
from sklearn.linear_model import LogisticRegression

_EPS = 1e-6


def fit_stack(y: np.ndarray, p_market: np.ndarray, p_skill: np.ndarray
              ) -> tuple[float, float]:
    """Fit (a, b) on held-out (train-era OOS) priced predictions."""
    X = np.column_stack([logit(np.clip(p_market, _EPS, 1 - _EPS)),
                         logit(np.clip(p_skill, _EPS, 1 - _EPS))])
    model = LogisticRegression(fit_intercept=False)
    model.fit(X, y)
    return float(model.coef_[0][0]), float(model.coef_[0][1])


def predict_stack(a: float, b: float, p_market: np.ndarray, p_skill: np.ndarray
                  ) -> np.ndarray:
    return expit(a * logit(np.clip(p_market, _EPS, 1 - _EPS))
                 + b * logit(np.clip(p_skill, _EPS, 1 - _EPS)))

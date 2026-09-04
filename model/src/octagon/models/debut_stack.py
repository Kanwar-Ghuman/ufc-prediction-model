"""Logit-space mix of the main blend and the debut model.

    p = sigmoid(a * logit(p_blend) + b * logit(p_debut))

No intercept, so corner swap is exact. Only fit when the debut model wins
on held-out low-history fights.
"""

import numpy as np
from scipy.special import expit, logit

from octagon.models.market import fit_stack as _fit_stack_impl

_EPS = 1e-6


def fit_stack(y: np.ndarray, p_blend: np.ndarray, p_debut: np.ndarray
              ) -> tuple[float, float]:
    """Fit (a, b) on held-out (train-era OOS) low-history predictions."""
    return _fit_stack_impl(y, p_blend, p_debut)


def predict_stack(a: float, b: float, p_blend: np.ndarray, p_debut: np.ndarray
                  ) -> np.ndarray:
    return expit(a * logit(np.clip(p_blend, _EPS, 1 - _EPS))
                 + b * logit(np.clip(p_debut, _EPS, 1 - _EPS)))

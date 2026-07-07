"""Probability calibration (PRD Phase B step 4).

A model can rank fights well and still be systematically over- or
under-confident. Isotonic regression learns a monotone map from raw
predicted probability to observed frequency — it fixes calibration without
changing the ranking (AUC is preserved).

The leak to avoid: the calibrator must never be fit on the fights it will
be judged on. We fit it on TRAIN-ERA out-of-sample predictions (from the
walk-forward tuning folds, all dated before validation starts) and then
apply it, frozen, to validation/test predictions.
"""

import numpy as np
from sklearn.isotonic import IsotonicRegression


def fit_isotonic(y: np.ndarray, p: np.ndarray) -> IsotonicRegression:
    """Map raw probabilities -> calibrated ones, clipped away from 0/1.

    y_min/y_max keep the calibrator from ever outputting exactly 0 or 1 —
    an isotonic step that happens to be pure wins would otherwise claim
    certainty, and one upset would cost infinite log loss.
    """
    iso = IsotonicRegression(y_min=0.02, y_max=0.98, out_of_bounds="clip")
    iso.fit(np.asarray(p, dtype=float), np.asarray(y, dtype=float))
    return iso


def apply(iso: IsotonicRegression, p: np.ndarray) -> np.ndarray:
    calibrated = iso.predict(np.asarray(p, dtype=float))
    # Preserve exact corner symmetry on the 0.5 point: isotonic regression
    # has no reason to map 0.5 -> 0.5, but a coin-flip prediction should
    # stay a coin flip. We re-center by symmetrizing the map.
    mirrored = 1.0 - iso.predict(1.0 - np.asarray(p, dtype=float))
    return (calibrated + mirrored) / 2.0

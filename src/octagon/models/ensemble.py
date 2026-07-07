"""Phase C step 5: blend the logistic regression and the GBM.

Why a blend helps when the GBM alone couldn't beat the LR on log loss: the
two models err differently — the LR is linear and superbly calibrated, the
GBM captures interactions and ranks a little better. Averaging their
probabilities keeps both strengths; the mixing weight is chosen on
TRAIN-ERA out-of-sample predictions only, so validation stays untouched
until scoring time.

A weighted average of two symmetric models is itself symmetric:
w*(1-p_lr(BA)) + (1-w)*(1-p_gbm(BA)) = 1 - blend(AB). No new symmetry risk.
"""

import numpy as np

from octagon.eval.metrics import log_loss


def blend(p_lr: np.ndarray, p_gbm: np.ndarray, weight_lr: float) -> np.ndarray:
    return weight_lr * p_lr + (1.0 - weight_lr) * p_gbm


def tune_weight(y: np.ndarray, p_lr: np.ndarray, p_gbm: np.ndarray) -> float:
    """Grid-search the LR weight on held-out (train-era OOS) predictions.

    A 1-D grid beats fancier meta-learners here: with one parameter there's
    almost nothing to overfit, and the answer is easy to read.
    """
    grid = np.linspace(0.0, 1.0, 21)
    losses = [log_loss(y, blend(p_lr, p_gbm, w)) for w in grid]
    return float(grid[int(np.argmin(losses))])

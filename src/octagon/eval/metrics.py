"""Evaluation metrics (PRD section 2). Accuracy is the headline number
people ask about, but it's the LEAST informative one here — a coin flip gets
50% and 'always pick the favorite' gets ~65%. Log loss, Brier and ECE score
the *probabilities*, which is what this project is actually about."""

import numpy as np


def _clip(p: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """Keep log() finite; a model claiming 0 or 1 gets clipped, not rewarded."""
    return np.clip(np.asarray(p, dtype=float), eps, 1 - eps)


def accuracy(y: np.ndarray, p: np.ndarray) -> float:
    """Share of fights called correctly; an exact 0.5 earns half credit
    (a coin flip should score 0.5, not depend on tie-breaking direction)."""
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    return float(np.mean(np.where(p == 0.5, 0.5, (p > 0.5) == (y == 1.0))))


def log_loss(y: np.ndarray, p: np.ndarray) -> float:
    """Mean negative log-likelihood. Punishes confident wrongness hard —
    predicting 0.9 on a loser costs ~2.3, predicting 0.55 costs ~0.8."""
    y = np.asarray(y, dtype=float)
    p = _clip(p)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def brier(y: np.ndarray, p: np.ndarray) -> float:
    """Mean squared error of the probability. Bounded [0, 1], less spiky
    than log loss; 0.25 is the score of always saying 0.5."""
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    return float(np.mean((p - y) ** 2))


def roc_auc(y: np.ndarray, p: np.ndarray) -> float:
    """P(random winner's predicted prob > random loser's) — discrimination
    regardless of calibration."""
    from sklearn.metrics import roc_auc_score

    return float(roc_auc_score(y, p))


def ece(y: np.ndarray, p: np.ndarray, n_bins: int = 10) -> float:
    """Expected Calibration Error with equal-width bins.

    Bin fights by predicted probability; in each bin compare the average
    prediction with the actual win rate; average the gaps weighted by bin
    size. 'When the model says 70%, does it happen ~70% of the time?'
    """
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    total = 0.0
    for lo, hi in zip(edges[:-1], edges[1:]):
        mask = (p >= lo) & (p < hi) if hi < 1.0 else (p >= lo) & (p <= hi)
        if mask.sum() == 0:
            continue
        total += mask.mean() * abs(y[mask].mean() - p[mask].mean())
    return float(total)


def summarize(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    """All PRD metrics for one model's predictions."""
    return {
        "n": int(len(y)),
        "accuracy": accuracy(y, p),
        "log_loss": log_loss(y, p),
        "brier": brier(y, p),
        "roc_auc": roc_auc(y, p),
        "ece": ece(y, p),
    }


def reliability_diagram(named_predictions: dict[str, tuple[np.ndarray, np.ndarray]],
                        path, n_bins: int = 10) -> None:
    """Plot predicted probability vs. observed win rate for several models.

    A calibrated model hugs the diagonal. Points far above it mean
    underconfidence, far below it mean overconfidence.
    """
    import matplotlib

    matplotlib.use("Agg")  # no display needed; we only save files
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="perfect calibration")
    edges = np.linspace(0.0, 1.0, n_bins + 1)
    for name, (y, p) in named_predictions.items():
        y = np.asarray(y, dtype=float)
        p = np.asarray(p, dtype=float)
        xs, ys = [], []
        for lo, hi in zip(edges[:-1], edges[1:]):
            mask = (p >= lo) & (p < hi) if hi < 1.0 else (p >= lo) & (p <= hi)
            if mask.sum() >= 20:  # skip bins too small to mean anything
                xs.append(p[mask].mean())
                ys.append(y[mask].mean())
        ax.plot(xs, ys, marker="o", label=name)
    ax.set_xlabel("predicted probability")
    ax.set_ylabel("observed win rate")
    ax.set_title("Reliability diagram")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)

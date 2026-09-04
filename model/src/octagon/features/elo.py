"""Elo ratings. Pre-fight rating is captured before the update."""

import math
from dataclasses import dataclass, field
from typing import Iterable

# Score values from the winner column in the fights table.
_SCORES = {"fighter1": 1.0, "fighter2": 0.0, "draw": 0.5}


def expected_score(rating_a: float, rating_b: float) -> float:
    """P(A beats B) implied by the ratings — the classic logistic curve.

    A 400-point gap means 10:1 expected odds; equal ratings mean 0.5.
    """
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / 400.0))


@dataclass
class Elo:
    """Mutable book of ratings, updated one fight at a time, in date order."""

    initial: float = 1500.0
    k: float = 32.0
    ratings: dict[str, float] = field(default_factory=dict)

    def get(self, fighter: str) -> float:
        """Current rating; unseen fighters start at `initial`."""
        return self.ratings.get(fighter, self.initial)

    def update(self, fighter_a: str, fighter_b: str, score_a: float,
               k_multiplier: float = 1.0,
               k_multiplier_a: float = 1.0,
               k_multiplier_b: float = 1.0) -> tuple[float, float]:
        """Apply a result. Returns pre-fight ratings (the feature values).

        k_multiplier scales both corners (e.g. finishes). Per-corner
        multipliers can make the update non-zero-sum so a newcomer's rating
        moves faster than a veteran's.
        """
        pre_a, pre_b = self.get(fighter_a), self.get(fighter_b)
        exp_a = expected_score(pre_a, pre_b)
        k = self.k * k_multiplier
        self.ratings[fighter_a] = pre_a + k * k_multiplier_a * (score_a - exp_a)
        self.ratings[fighter_b] = pre_b + k * k_multiplier_b * (
            (1.0 - score_a) - (1.0 - exp_a))
        return pre_a, pre_b


def experience_multiplier(n_prior_fights: int, boost: float,
                          settle_after: int = 6) -> float:
    """How much faster a green fighter's rating should move.

    1 + boost on their first fight, decaying linearly to 1 by the
    `settle_after`-th. boost = 0 recovers plain Elo exactly.
    """
    if boost <= 0 or n_prior_fights >= settle_after:
        return 1.0
    return 1.0 + boost * (settle_after - n_prior_fights) / settle_after


def _binary_log_loss(y: float, p: float) -> float:
    p = min(1.0 - 1e-15, max(1e-15, p))
    return -(y * math.log(p) + (1.0 - y) * math.log(1.0 - p))


def train_era_log_loss(
    fights: Iterable[tuple[str, str, str, str]],
    k: float,
    train_end: str,
    initial: float = 1500.0,
) -> float:
    """Mean Elo log loss on fights dated <= train_end, in date order.

    Later fights are ignored for both scoring and rating updates — so a K
    chosen here cannot peek at validation or test labels.
    Each item is (iso_date, fighter1, fighter2, winner).
    """
    book = Elo(initial=initial, k=k)
    total, n = 0.0, 0
    for date, fighter1, fighter2, winner in sorted(fights, key=lambda row: row[0]):
        if date > train_end:
            continue
        if winner == "nc":
            continue
        score = _SCORES.get(winner)
        if score is None:
            continue
        p = expected_score(book.get(fighter1), book.get(fighter2))
        if winner in ("fighter1", "fighter2"):
            total += _binary_log_loss(score, p)
            n += 1
        book.update(fighter1, fighter2, score)
    return total / n if n else math.inf


def select_k(
    fights: Iterable[tuple[str, str, str, str]],
    train_end: str,
    candidates: Iterable[float] = (8, 16, 32, 48, 64, 80, 96, 112, 128),
    initial: float = 1500.0,
) -> tuple[float, dict[float, float]]:
    """Pick K by train-era Elo log loss only. Never scores dates after train_end."""
    losses = {float(k): train_era_log_loss(fights, float(k), train_end, initial)
              for k in candidates}
    best = min(losses, key=losses.get)
    return best, losses


def run_history(
    fights: Iterable[tuple[str, str, str]], initial: float = 1500.0, k: float = 32.0
) -> list[tuple[float, float]]:
    """Replay chronological (fighter1, fighter2, winner) fights.

    Returns each fight's pre-fight rating pair, aligned with the input order.
    'nc' (no contest) fights pass through without touching ratings — nothing
    was decided in them.
    """
    book = Elo(initial=initial, k=k)
    pre_ratings: list[tuple[float, float]] = []
    for fighter1, fighter2, winner in fights:
        if winner == "nc":
            pre_ratings.append((book.get(fighter1), book.get(fighter2)))
            continue
        pre_ratings.append(book.update(fighter1, fighter2, _SCORES[winner]))
    return pre_ratings

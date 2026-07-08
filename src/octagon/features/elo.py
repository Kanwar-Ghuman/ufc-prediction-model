"""Elo ratings for fighters (opponent-adjusted skill, PRD 5.3).

Why Elo? A fighter's raw record ignores who they fought. Elo transfers
points from loser to winner, scaled by how surprising the result was, so
beating a champion is worth more than beating a debutant. The *difference*
in pre-fight Elo becomes one of our strongest features.

Point-in-time discipline: a fight's feature must be the rating each fighter
walked in with — captured BEFORE the update. `run_history` enforces this by
construction; tests/test_elo.py locks it in.
"""

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
               k_multiplier: float = 1.0) -> tuple[float, float]:
        """Record a result (score_a: 1 win, 0.5 draw, 0 loss for A).

        Returns the PRE-fight ratings — the only values allowed as features.
        The update is zero-sum: whatever A gains, B loses. k_multiplier
        implements margin-of-victory: a first-round knockout is stronger
        evidence of a skill gap than a split decision, so it moves ratings
        further (PRD 5.3's optional MOV adjustment).
        """
        pre_a, pre_b = self.get(fighter_a), self.get(fighter_b)
        exp_a = expected_score(pre_a, pre_b)
        k = self.k * k_multiplier
        self.ratings[fighter_a] = pre_a + k * (score_a - exp_a)
        self.ratings[fighter_b] = pre_b + k * ((1.0 - score_a) - (1.0 - exp_a))
        return pre_a, pre_b


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

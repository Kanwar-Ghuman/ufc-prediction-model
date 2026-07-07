"""Paper-trading backtest (PRD Phase D). SIMULATION ONLY.

This module exists to teach expected value, staking, and drawdown — not to
make money. The error analysis (M5) already showed the model loses its
disagreements with the market ~61/39, so the honest prior is that this
simulation LOSES units. Running it anyway, and reporting that plainly, is
the point.

Mechanics:
* For each priced fight we compare the model's probability with the
  vig-free market probability on both sides; if the best edge clears the
  threshold, we bet that side at the listed decimal odds.
* Staking: 'flat' bets 1 unit; 'kelly' bets quarter-Kelly (configurable)
  of a running 100-unit bankroll — compounding, like a real bankroll.
* Metrics include a bootstrap CI on ROI because a few hundred bets of
  variance can dress a losing strategy up as a winner (and vice versa).

Known bias, disclosed everywhere: odds are best-available-line (betmma),
so simulated prices are kinder than any single book's. True closing line
value (CLV) needs opening odds we don't have; we report the model-vs-close
edge instead and say so.
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from octagon.betting.odds import expected_value, implied_probability, kelly_stake, remove_vig

DISCLAIMER = (
    "THIS IS A SIMULATION for educational purposes. No real money, no betting "
    "advice. Past simulated results do not predict future returns; the odds "
    "used are best-available lines that flatter results; and the model "
    "demonstrably knows less than the market."
)


@dataclass
class Bet:
    date: str
    fight_id: int
    side: str          # 'fighter1' | 'fighter2'
    p_model: float
    fair_prob: float   # vig-free market probability for the chosen side
    decimal_odds: float
    edge: float        # p_model - fair_prob
    stake: float
    pnl: float


def run_backtest(preds: pd.DataFrame, prob_col: str, staking: str,
                 edge_threshold: float, kelly_fraction: float = 0.25,
                 initial_bankroll: float = 100.0) -> list[Bet]:
    """Walk the priced fights chronologically and place simulated bets."""
    priced = preds[preds["f1_odds"].notna() & preds["f2_odds"].notna()]
    priced = priced.sort_values(["date", "fight_id"])
    bankroll = initial_bankroll
    bets: list[Bet] = []

    for _, row in priced.iterrows():
        p1 = float(row[prob_col])
        fair1, fair2 = remove_vig(implied_probability(row["f1_odds"]),
                                  implied_probability(row["f2_odds"]))
        candidates = [
            ("fighter1", p1, fair1, row["f1_odds"]),
            ("fighter2", 1.0 - p1, fair2, row["f2_odds"]),
        ]
        side, p, fair, odds = max(candidates, key=lambda c: c[1] - c[2])
        edge = p - fair
        if edge < edge_threshold or expected_value(p, odds) <= 0:
            continue

        if staking == "flat":
            stake = 1.0
        elif staking == "kelly":
            if bankroll <= 0:
                break  # busted — a lesson in itself
            stake = kelly_stake(p, odds, fraction=kelly_fraction) * bankroll
            if stake <= 0:
                continue
        else:
            raise ValueError(f"unknown staking '{staking}'")

        won = (row["label"] == 1) == (side == "fighter1")
        pnl = stake * (odds - 1.0) if won else -stake
        bankroll += pnl
        bets.append(Bet(row["date"], int(row["fight_id"]), side, p, fair,
                        float(odds), edge, stake, pnl))
    return bets


def summarize(bets: list[Bet], seed: int = 42) -> dict:
    """ROI, drawdown, hit rate, edge stats, bootstrap CI on ROI."""
    if not bets:
        return {"n_bets": 0}
    pnl = np.array([b.pnl for b in bets])
    stakes = np.array([b.stake for b in bets])
    equity = np.cumsum(pnl)
    running_peak = np.maximum.accumulate(np.concatenate([[0.0], equity]))[1:]
    roi = pnl.sum() / stakes.sum()

    # Bootstrap: resample bets with replacement; how much of the ROI is luck?
    rng = np.random.default_rng(seed)
    samples = []
    for _ in range(2000):
        idx = rng.integers(0, len(bets), len(bets))
        samples.append(pnl[idx].sum() / stakes[idx].sum())
    lo, hi = np.percentile(samples, [2.5, 97.5])

    return {
        "n_bets": len(bets),
        "total_staked": float(stakes.sum()),
        "total_pnl_units": float(pnl.sum()),
        "roi": float(roi),
        "roi_ci95": (float(lo), float(hi)),
        "hit_rate": float(np.mean(pnl > 0)),
        "max_drawdown_units": float(np.max(running_peak - equity)),
        "avg_edge_vs_close": float(np.mean([b.edge for b in bets])),
        "avg_odds": float(np.mean([b.decimal_odds for b in bets])),
    }


def equity_curve(bets: list[Bet]):
    """(dates, cumulative pnl) for plotting."""
    return [b.date for b in bets], np.cumsum([b.pnl for b in bets])

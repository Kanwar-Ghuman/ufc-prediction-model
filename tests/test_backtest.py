"""Backtest arithmetic on hand-built fixtures. If the simulator's math is
wrong, every lesson it teaches is wrong."""

import numpy as np
import pandas as pd
import pytest

from octagon.betting.backtest import run_backtest, summarize


def make_preds(rows):
    """rows: (date, fight_id, p_blend, f1_odds, f2_odds, label)"""
    return pd.DataFrame(rows, columns=["date", "fight_id", "p_blend",
                                       "f1_odds", "f2_odds", "label"])


def test_flat_staking_pnl_by_hand():
    preds = make_preds([
        # Model says 0.70, fair market ~0.50 at 2.0/2.0 -> bet f1, edge 0.20.
        ("2023-01-01", 1, 0.70, 2.0, 2.0, 1),   # win: +1.0 unit
        ("2023-01-08", 2, 0.70, 2.0, 2.0, 0),   # lose: -1.0 unit
        # Edge on fighter2: p1=0.3 -> p2=0.7 vs fair 0.5 -> bet f2 at 2.0.
        ("2023-01-15", 3, 0.30, 2.0, 2.0, 0),   # f2 wins: +1.0 unit
    ])
    bets = run_backtest(preds, "p_blend", "flat", edge_threshold=0.05)
    assert [b.side for b in bets] == ["fighter1", "fighter1", "fighter2"]
    assert [b.pnl for b in bets] == [1.0, -1.0, 1.0]
    s = summarize(bets)
    assert s["total_pnl_units"] == pytest.approx(1.0)
    assert s["roi"] == pytest.approx(1.0 / 3.0)
    assert s["hit_rate"] == pytest.approx(2 / 3)
    assert s["max_drawdown_units"] == pytest.approx(1.0)  # peak +1 -> trough 0


def test_edge_threshold_filters_thin_edges():
    preds = make_preds([
        ("2023-01-01", 1, 0.52, 2.0, 2.0, 1),   # edge 0.02 — below threshold
        ("2023-01-08", 2, 0.60, 2.0, 2.0, 1),   # edge 0.10 — bet
    ])
    bets = run_backtest(preds, "p_blend", "flat", edge_threshold=0.05)
    assert [b.fight_id for b in bets] == [2]


def test_no_bet_without_positive_ev():
    # Model edge vs fair prob exists, but the PRICE is bad: p=0.55 at 1.70
    # (EV = 0.55*0.7 - 0.45 < 0). Vig-free edge alone must not trigger a bet.
    preds = make_preds([("2023-01-01", 1, 0.55, 1.70, 2.10, 1)])
    assert run_backtest(preds, "p_blend", "flat", edge_threshold=0.0) == []


def test_kelly_compounds_on_bankroll():
    preds = make_preds([
        ("2023-01-01", 1, 0.60, 2.0, 2.0, 1),
        ("2023-01-08", 2, 0.60, 2.0, 2.0, 1),
    ])
    bets = run_backtest(preds, "p_blend", "kelly", edge_threshold=0.05,
                        kelly_fraction=0.25, initial_bankroll=100.0)
    # Quarter Kelly at p=0.6, d=2.0: full kelly 0.2 -> stake 5% of bankroll.
    assert bets[0].stake == pytest.approx(5.0)
    assert bets[1].stake == pytest.approx(0.05 * 105.0)  # bankroll grew by +5


def test_unpriced_fights_are_ignored():
    preds = make_preds([("2023-01-01", 1, 0.99, np.nan, np.nan, 1)])
    assert run_backtest(preds, "p_blend", "flat", edge_threshold=0.0) == []


def test_bootstrap_ci_brackets_the_point_estimate():
    preds = make_preds([
        (f"2023-01-{d:02d}", d, 0.65, 2.0, 2.0, d % 2) for d in range(1, 29)
    ])
    s = summarize(run_backtest(preds, "p_blend", "flat", edge_threshold=0.05))
    lo, hi = s["roi_ci95"]
    assert lo <= s["roi"] <= hi

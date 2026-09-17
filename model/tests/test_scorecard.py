"""Grading a past card: outcome mapping, base rates, and the aggregates.

The failure mode worth guarding against is a scorecard that flatters
itself, so the properties pinned here are the ones that would let it: that
grading reads the frozen claim rather than a refit, that a bout falling off
the card can't shift the others, and that the no-skill reference is a real
comparison rather than a decoration.
"""

import sqlite3

import pytest

from octagon.db.schema import SCHEMA
from octagon.eval import scorecard
from octagon.models import finish_round

import pandas as pd


def _frozen(*fights) -> pd.DataFrame:
    """A frozen prediction frame: (f1, f2, p_f1_wins, cell overrides...)."""
    rows = []
    for f1, f2, p, cells in fights:
        row = {"date": "2026-01-10", "event": "Test Card", "f1_name": f1,
               "f2_name": f2, "weight_class": "Lightweight",
               "scheduled_rounds": 3.0, "p_f1_wins": p}
        row.update(dict.fromkeys(finish_round.outcome_columns(), 0.0))
        row.update(cells)
        rows.append(row)
    return pd.DataFrame(rows)


def _conn(results=(), history=()) -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    for i, (f1, f2, winner, method, end_round) in enumerate(results):
        conn.execute(
            "INSERT INTO fights (fight_id, event_id, date, fighter1, fighter2, "
            "winner, method, end_round, scheduled_rounds, source) "
            "VALUES (?, 1, '2026-01-10', ?, ?, ?, ?, ?, 3, 'test')",
            (i + 1, f1, f2, winner, method, end_round))
    for j, (method, end_round) in enumerate(history):
        conn.execute(
            "INSERT INTO fights (fight_id, event_id, date, fighter1, fighter2, "
            "winner, method, end_round, scheduled_rounds, source) "
            "VALUES (?, 1, '2025-01-01', 'A', 'B', 'fighter1', ?, ?, 3, 'test')",
            (1000 + j, method, end_round))
    return conn


@pytest.mark.parametrize("winner,method,end_round,expected", [
    ("fighter1", "KO/TKO", 2, "f1_ko_r2"),
    ("fighter2", "SUB", 1, "f2_sub_r1"),
    ("fighter1", "U-DEC", 3, "f1_dec"),
    ("fighter2", "S-DEC", 3, "f2_dec"),
])
def test_outcome_column_maps_results_onto_the_joint(winner, method, end_round, expected):
    result = {"fighter1": "Alice", "fighter2": "Bob", "winner": winner,
              "method": method, "end_round": end_round}
    assert scorecard.outcome_column(result, "fighter1") == expected


def test_outcome_column_follows_the_card_ordering_not_the_database():
    """The card may list the fighters in the opposite order to ufcstats."""
    result = {"fighter1": "Alice", "fighter2": "Bob", "winner": "fighter1",
              "method": "KO/TKO", "end_round": 2}
    assert scorecard.outcome_column(result, "fighter2") == "f2_ko_r2"


def test_draws_and_unmapped_methods_are_not_gradable():
    for winner, method in (("draw", "U-DEC"), ("fighter1", "DQ"), ("fighter1", None)):
        result = {"fighter1": "Alice", "fighter2": "Bob", "winner": winner,
                  "method": method, "end_round": 3}
        assert scorecard.outcome_column(result, "fighter1") is None


def test_grading_reads_the_frozen_probability():
    conn = _conn([("Alice", "Bob", "fighter1", "KO/TKO", 2)])
    graded = scorecard.grade(conn, _frozen(("Alice", "Bob", 0.72, {"f1_ko_r2": 0.3})),
                             (0.45, 0.55))
    fight = graded["fights"][0]
    assert fight["p_f1_wins"] == pytest.approx(0.72)
    assert fight["correct"] is True
    assert fight["p_actual"] == pytest.approx(0.3)


def test_grading_respects_the_cards_corner_order():
    """ufcstats lists Alice first; the card listed Bob first."""
    conn = _conn([("Alice", "Bob", "fighter1", "KO/TKO", 2)])
    graded = scorecard.grade(conn, _frozen(("Bob", "Alice", 0.28, {"f2_ko_r2": 0.3})),
                             (0.45, 0.55))
    fight = graded["fights"][0]
    assert fight["winner"] == "Alice"
    assert fight["correct"] is True           # 0.28 on Bob = a pick of Alice
    assert fight["p_actual"] == pytest.approx(0.3)


def test_a_cancelled_bout_is_skipped_not_misaligned():
    conn = _conn([("Cara", "Dee", "fighter1", "U-DEC", 3)])
    graded = scorecard.grade(
        conn, _frozen(("Alice", "Bob", 0.72, {}), ("Cara", "Dee", 0.61, {})),
        (0.45, 0.55))
    assert [f["f1"] for f in graded["fights"]] == ["Cara"]
    assert graded["fights"][0]["p_f1_wins"] == pytest.approx(0.61)
    assert graded["skipped"][0]["status"] == "did not take place"


def test_grading_matches_fighters_when_the_card_carries_a_middle_name():
    """Belgrade: card said 'Nina Nikolija Milošević', ufcstats said 'Nina Milosevic'."""
    conn = _conn([("Nina Milosevic", "Hailey Cowan", "fighter1", "KO/TKO", 1)])
    graded = scorecard.grade(
        conn,
        _frozen(("Nina Nikolija Milošević", "Hailey Cowan", 0.76,
                 {"f1_ko_r1": 0.2})),
        (0.45, 0.55))
    assert len(graded["fights"]) == 1
    assert graded["skipped"] == []
    assert graded["fights"][0]["correct"] is True
    assert graded["fights"][0]["winner"] == "Nina Milosevic"


def test_grading_matches_a_fighter_competing_under_a_nickname():
    """Perth: card said 'Giovanna Canuto', ufcstats said 'Gigi Canuto'."""
    conn = _conn([("Gigi Canuto", "Carol Foro", "fighter2", "U-DEC", 3)])
    graded = scorecard.grade(
        conn, _frozen(("Giovanna Canuto", "Carol Foro", 0.32, {"f2_dec": 0.2})),
        (0.45, 0.55))
    assert graded["skipped"] == []
    assert graded["fights"][0]["correct"] is True    # 0.32 on Canuto = a pick of Foro
    assert graded["fights"][0]["winner"] == "Carol Foro"
    assert graded["fights"][0]["p_actual"] == pytest.approx(0.2)


def test_surname_fallback_needs_the_bout_to_be_unambiguous():
    """Two bouts sharing both surnames: refuse to guess rather than mis-grade."""
    conn = _conn([("Gigi Canuto", "Carol Foro", "fighter2", "U-DEC", 3),
                  ("Ana Canuto", "Luiza Foro", "fighter1", "KO/TKO", 1)])
    graded = scorecard.grade(
        conn, _frozen(("Giovanna Canuto", "Carol Foro", 0.32, {})), (0.45, 0.55))
    assert graded["fights"] == []
    assert graded["skipped"][0]["status"] == "did not take place"


def test_abstain_band_marks_a_fight_as_no_call():
    conn = _conn([("Alice", "Bob", "fighter1", "U-DEC", 3)])
    graded = scorecard.grade(conn, _frozen(("Alice", "Bob", 0.52, {})), (0.45, 0.55))
    assert graded["fights"][0]["called"] is False
    assert graded["aggregates"]["n_called"] == 0


def test_base_rates_come_from_history_and_respect_fight_length():
    conn = _conn(history=[("KO/TKO", 1)] * 6 + [("U-DEC", 3)] * 4)
    base = scorecard.base_rate_joint(conn, "2026-01-10")[3]
    assert sum(base.values()) == pytest.approx(1.0)
    assert base["f1_ko_r1"] == pytest.approx(0.3)     # 60% KO, split two corners
    assert base["f1_dec"] == pytest.approx(0.2)
    assert base["f1_ko_r4"] == 0.0                    # unreachable in a 3-rounder


def test_aggregates_count_winners_methods_and_rounds():
    conn = _conn([("Alice", "Bob", "fighter1", "KO/TKO", 2),
                  ("Cara", "Dee", "fighter2", "U-DEC", 3)])
    graded = scorecard.grade(conn, _frozen(
        ("Alice", "Bob", 0.70, {"f1_ko_r2": 0.6, "f1_dec": 0.4}),
        ("Cara", "Dee", 0.70, {"f1_dec": 0.6, "f1_ko_r1": 0.4}),
    ), (0.45, 0.55))
    a = graded["aggregates"]
    assert (a["n"], a["winners_correct"]) == (2, 1)
    assert a["method_correct"] == 2               # KO called, then decision called
    assert (a["round_correct"], a["n_finishes"]) == (1, 1)
    assert a["log_loss"] > 0.0


def test_a_split_finish_does_not_outvote_the_modal_decision():
    """35% KO + 25% sub does NOT beat a 40% decision: the call is the mode.

    Pooling KO and submission into 'a finish' and then resolving it was
    measured to be worse than argmax on both the validation and test eras,
    because KO takes ~65% of finishes and so swallowed almost every
    resolved finish. See `scorecard.called_method`.
    """
    conn = _conn([("Alice", "Bob", "fighter1", "KO/TKO", 1)])
    graded = scorecard.grade(conn, _frozen(
        ("Alice", "Bob", 0.70, {"f1_ko_r1": 0.35, "f1_sub_r1": 0.25, "f1_dec": 0.40}),
    ), (0.45, 0.55))
    assert graded["fights"][0]["method_called"] == "dec"
    assert graded["fights"][0]["method_correct"] is False


def test_grading_calls_the_same_method_the_card_reported():
    """The scorecard must grade the rule `select_outcome` printed.

    These are two code paths answering one question. When they disagree a
    card can report 'by decision' and then be graded as having said KO.
    """
    for cells in (
        {"f1_ko_r1": 0.35, "f1_sub_r1": 0.25, "f1_dec": 0.40},
        {"f1_ko_r1": 0.50, "f1_sub_r1": 0.10, "f1_dec": 0.40},
        {"f1_ko_r1": 0.10, "f1_sub_r2": 0.55, "f1_dec": 0.35},
    ):
        row = dict.fromkeys(finish_round.outcome_columns(), 0.0)
        row.update(cells)
        series = pd.Series(row)
        reported = finish_round.select_outcome(series, "f1")["method"]
        graded = scorecard.called_method(row)
        assert graded == {"KO/TKO": "ko", "SUB": "sub", "DEC": "dec"}[reported]

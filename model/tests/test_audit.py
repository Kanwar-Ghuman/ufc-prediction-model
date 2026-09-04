"""Audit guards: split disjointness must be pairwise, not a three-way AND."""

import pandas as pd

from octagon.eval.audit import check_chronological_splits


def _frame(rows):
    return pd.DataFrame(rows)


def test_pairwise_overlap_fails_even_if_the_third_split_is_clean():
    df = _frame([
        {"fight_id": 1, "date": "2020-01-01", "f1_name": "A", "f2_name": "B"},
        {"fight_id": 1, "date": "2022-06-01", "f1_name": "A", "f2_name": "B"},
        {"fight_id": 2, "date": "2025-01-01", "f1_name": "C", "f2_name": "D"},
    ])
    name, ok, _ = check_chronological_splits(df, "2021-12-31", "2023-12-31")
    assert name == "chronological split boundaries hold"
    assert ok is False


def test_unique_fight_ids_inside_one_split_still_required():
    df = _frame([
        {"fight_id": 1, "date": "2020-01-01", "f1_name": "A", "f2_name": "B"},
        {"fight_id": 1, "date": "2020-06-01", "f1_name": "C", "f2_name": "D"},
        {"fight_id": 2, "date": "2022-06-01", "f1_name": "E", "f2_name": "F"},
        {"fight_id": 3, "date": "2025-01-01", "f1_name": "G", "f2_name": "H"},
    ])
    _, ok, _ = check_chronological_splits(df, "2021-12-31", "2023-12-31")
    assert ok is False


def test_clean_chronological_splits_pass():
    df = _frame([
        {"fight_id": 1, "date": "2020-01-01", "f1_name": "A", "f2_name": "B"},
        {"fight_id": 2, "date": "2022-06-01", "f1_name": "B", "f2_name": "A"},
        {"fight_id": 3, "date": "2025-01-01", "f1_name": "C", "f2_name": "D"},
    ])
    _, ok, detail = check_chronological_splits(df, "2021-12-31", "2023-12-31")
    assert ok is True
    assert "1 rematch" in detail

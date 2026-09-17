"""Regression tests for upstream Greco CSV serialization changes."""

import pytest

from octagon.db.greco import _parse_count


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("0", 0), ("3", 3), ("0.0", 0), ("3.0", 3), (" 2.0 ", 2)],
)
def test_parse_count_accepts_integer_and_float_serializations(raw, expected):
    assert _parse_count(raw) == expected


@pytest.mark.parametrize("raw", [None, "", "--", "nan", "inf", "-1", "1.5"])
def test_parse_count_rejects_missing_or_non_count_values(raw):
    assert _parse_count(raw) is None

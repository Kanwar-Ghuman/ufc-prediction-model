"""Shared parsers against real quirks observed in both raw data sources."""

import pytest

from octagon.db.parsing import (
    fight_duration_seconds,
    normalize_name,
    parse_bout,
    parse_dob,
    parse_height_to_cm,
    parse_long_date,
    parse_method,
    parse_mmss_to_seconds,
    parse_of_pair,
    parse_outcome,
    parse_reach_to_cm,
    parse_time_format,
    parse_valid_odds,
    parse_weightclass,
    parse_weight_to_kg,
)


def test_parse_height_both_spellings():
    assert parse_height_to_cm("5'11\"") == pytest.approx(180.34)
    assert parse_height_to_cm("5' 11\"") == pytest.approx(180.34)
    assert parse_height_to_cm("--") is None


def test_parse_reach():
    assert parse_reach_to_cm('66"') == pytest.approx(167.64)
    assert parse_reach_to_cm("--") is None


def test_parse_weight_both_spellings():
    assert parse_weight_to_kg("155lbs.") == pytest.approx(70.31, abs=0.01)
    assert parse_weight_to_kg("155 lbs.") == pytest.approx(70.31, abs=0.01)
    assert parse_weight_to_kg("--") is None


def test_parse_dob_both_spellings():
    assert parse_dob("Jul13,1978") == "1978-07-13"
    assert parse_dob("Jul 13, 1978") == "1978-07-13"
    assert parse_dob("--") is None


def test_parse_long_date():
    assert parse_long_date("May 16, 2026") == "2026-05-16"
    assert parse_long_date("garbage") is None


def test_parse_valid_odds_rejects_inf_and_degenerate():
    # The bootstrap CSV really contains 'inf' odds — they must not load.
    assert parse_valid_odds("inf") is None
    assert parse_valid_odds("1.0") is None
    assert parse_valid_odds("nan") is None
    assert parse_valid_odds("2.88") == pytest.approx(2.88)


def test_parse_of_pair():
    assert parse_of_pair("9 of 12") == (9, 12)
    assert parse_of_pair("---") == (None, None)


def test_parse_mmss():
    assert parse_mmss_to_seconds("1:44") == 104
    assert parse_mmss_to_seconds("5:00") == 300
    assert parse_mmss_to_seconds("--") is None


def test_parse_time_format():
    assert parse_time_format("3 Rnd (5-5-5)") == [5, 5, 5]
    assert parse_time_format("1 Rnd + OT (12-3)") == [12, 3]
    assert parse_time_format("1 Rnd (20)") == [20]
    assert parse_time_format("No Time Limit") is None


def test_fight_duration():
    # Ends 2:30 into round 3 of a standard 5-5-5 bout.
    assert fight_duration_seconds(3, 150, [5, 5, 5]) == 750
    # Old format: ends 1:00 into the 3-minute OT of a (12-3) bout.
    assert fight_duration_seconds(2, 60, [12, 3]) == 780
    # Unknown format falls back to 5-minute rounds.
    assert fight_duration_seconds(2, 60, None) == 360
    assert fight_duration_seconds(None, 60, [5, 5, 5]) is None


def test_parse_weightclass():
    assert parse_weightclass("Featherweight Bout") == ("Featherweight", False)
    assert parse_weightclass("UFC Featherweight Title Bout") == ("Featherweight", True)
    # Longest-first matters: these must not match the shorter class name.
    assert parse_weightclass("Light Heavyweight Bout") == ("Light Heavyweight", False)
    assert parse_weightclass("Women's Flyweight Bout") == ("Women's Flyweight", False)


def test_parse_method():
    assert parse_method("Decision - Unanimous ") == ("U-DEC", None)
    assert parse_method("Submission") == ("SUB", None)
    assert parse_method("TKO - Doctor's Stoppage") == ("KO/TKO", "Doctor's Stoppage")
    assert parse_method("DQ") == ("DQ", None)  # unmapped values pass through


def test_parse_outcome():
    assert parse_outcome("W/L") == "fighter1"
    assert parse_outcome("L/W") == "fighter2"
    assert parse_outcome("D/D") == "draw"
    assert parse_outcome("NC/NC") == "nc"
    assert parse_outcome("??") is None


def test_parse_bout():
    assert parse_bout("Arnold Allen vs. Melquizael Costa") == ("Arnold Allen", "Melquizael Costa")
    assert parse_bout("no separator here") is None


def test_normalize_name_handles_accents_and_order():
    # The exact mismatches that break naive joins between our two sources.
    assert normalize_name("José Aldo") == normalize_name("Jose Aldo")
    assert normalize_name("Weili Zhang") == normalize_name("Zhang Weili")
    assert normalize_name("Ovince Saint Preux") == normalize_name("ovince saint preux")
    assert normalize_name("Jon Jones") != normalize_name("Jon Bones")
    # ł does not NFKD-decompose — without an explicit fold, Błachowicz
    # would never match the ASCII spelling in ufcstats.
    assert normalize_name("Jan Błachowicz") == normalize_name("Jan Blachowicz")
    assert normalize_name("Ľudovít Klein") == normalize_name("Ludovit Klein")

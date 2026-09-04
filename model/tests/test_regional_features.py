"""Pre-UFC regional features are point-in-time."""

import json

import pytest

from octagon.db.regional import load_regional_records
from octagon.db.schema import connect, init_db
from octagon.features.regional import career_snapshot, load_regional, regional_snapshot


def test_regional_features_use_only_pre_debut_fights():
    """Verify that regional_snapshot only counts fights before the snapshot date."""
    fights = [
        {"date": "2018-01-01", "result": "win", "method": "KO/TKO", "org": "Bellator", "is_amateur": 0},
        {"date": "2018-06-01", "result": "loss", "method": "SUB", "org": "PRIDE", "is_amateur": 0},
        {"date": "2019-03-15", "result": "win", "method": "DEC", "org": "Regional", "is_amateur": 0},
        {"date": "2020-12-01", "result": "draw", "method": None, "org": "Amateur", "is_amateur": 1},
    ]

    # Take snapshot before 2019-06-01: should include first 3 fights only
    snapshot = regional_snapshot(fights, "2019-06-01")
    assert snapshot["pre_ufc_fights"] == 3
    assert snapshot["pre_ufc_wins"] == 2
    assert snapshot["pre_ufc_losses"] == 1
    assert snapshot["pre_ufc_draws"] is None  # draw not before this date
    assert snapshot["pre_ufc_amateur_bouts"] is None

    # Take snapshot before 2021-01-01: should include all 4 fights
    snapshot_all = regional_snapshot(fights, "2021-01-01")
    assert snapshot_all["pre_ufc_fights"] == 4
    assert snapshot_all["pre_ufc_wins"] == 2
    assert snapshot_all["pre_ufc_losses"] == 1
    assert snapshot_all["pre_ufc_draws"] == 1
    assert snapshot_all["pre_ufc_amateur_bouts"] == 1


def test_regional_snapshot_empty():
    """Empty fight list should produce None values."""
    snapshot = regional_snapshot([], "2020-01-01")
    assert snapshot["pre_ufc_fights"] is None
    assert snapshot["pre_ufc_wins"] is None
    assert snapshot["pre_ufc_win_pct"] is None
    # v3.2/v3.3 keys are always present, so f1/f2 snapshots share one key set.
    for key in ("pre_ufc_ko_rate", "pre_ufc_streak", "pre_ufc_layoff_days",
                "pre_ufc_major_org_share", "pre_ufc_career_years", "pre_ufc_elo"):
        assert snapshot[key] is None


def test_regional_snapshot_profile_features():
    """Finish profile, durability, streak, layoff, activity and pedigree (v3.2)."""
    fights = [
        {"date": "2021-01-10", "result": "loss", "method": "KO/TKO", "org": "Local Show 3",
         "is_amateur": 0},
        {"date": "2022-03-01", "result": "win", "method": "SUB", "org": "LFA 120",
         "is_amateur": 0},
        {"date": "2023-06-01", "result": "win", "method": "KO/TKO",
         "org": "CW 150 - Cage Warriors 150", "is_amateur": 0},
        {"date": "2024-01-01", "result": "win", "method": "DEC", "org": "Fury FC 90",
         "is_amateur": 0},
    ]
    snap = regional_snapshot(fights, "2024-07-01")
    assert snap["pre_ufc_fights"] == 4
    assert snap["pre_ufc_ko_rate"] == pytest.approx(0.25)
    assert snap["pre_ufc_sub_rate"] == pytest.approx(0.25)
    assert snap["pre_ufc_finish_loss_rate"] == pytest.approx(0.25)
    assert snap["pre_ufc_streak"] == 3
    assert snap["pre_ufc_layoff_days"] == 182
    assert snap["pre_ufc_fights_24m"] == 2          # 2023-06-01 and 2024-01-01
    assert snap["pre_ufc_career_years"] == pytest.approx(3.47, abs=0.01)
    assert snap["pre_ufc_major_org_share"] == pytest.approx(0.75)   # LFA, CW, Fury
    # Three wins after one loss against a mixed org slate should sit above 1500.
    assert snap["pre_ufc_elo"] > 1500.0


def test_career_snapshot_merges_ufc_and_regional_chronologically():
    ufc = [("2023-09-01", "win", "U-DEC"), ("2024-02-01", "loss", "KO/TKO")]
    regional = [
        {"date": "2022-01-01", "result": "win", "method": "KO/TKO", "org": "LFA"},
        {"date": "2022-08-01", "result": "win", "method": "SUB", "org": "LFA"},
        # Future relative to the snapshot date — must be ignored.
        {"date": "2025-01-01", "result": "win", "method": "KO/TKO", "org": "PFL"},
    ]
    snap = career_snapshot(ufc, regional, "2024-06-01")
    assert snap["career_n_fights"] == 4
    assert snap["career_wins"] == 3
    assert snap["career_losses"] == 1
    assert snap["career_win_pct"] == pytest.approx((3 + 1) / (4 + 2))
    assert snap["career_streak"] == -1
    assert snap["career_finish_rate"] == pytest.approx(0.5)      # two finish wins
    assert snap["career_finished_rate"] == pytest.approx(0.25)   # one KO loss
    assert snap["career_layoff_days"] == 121
    assert snap["career_years"] == pytest.approx(2.41, abs=0.01)


def test_career_snapshot_is_the_regional_record_for_a_debutant():
    regional = [{"date": "2023-01-01", "result": "win", "method": "SUB", "org": "LFA"}]
    snap = career_snapshot([], regional, "2024-01-01")
    assert snap["career_n_fights"] == 1
    assert snap["career_layoff_days"] == 365
    assert career_snapshot([], [], "2024-01-01")["career_n_fights"] is None


def _write_cache(path, fights):
    path.write_text(json.dumps({
        "michael oliveira": {"name": "Michael Oliveira", "regional_fights": fights},
    }), encoding="utf-8")
    return path


def test_a_corrected_scrape_replaces_the_fighters_rows(tmp_path):
    """Re-scraping is how a wrong-person match gets fixed, so it must not merge.

    Sherdog's name search first gave us a different Michael Oliveira, whose
    only bout was a loss in 2001. Loading the corrected 9-0 record on top of
    that left the phantom loss in place and the model scored him 9-1.
    """
    db = connect(tmp_path / "t.db")
    init_db(db)
    cache = tmp_path / "sherdog.json"
    empty_media = tmp_path / "media.json"
    empty_media.write_text("{}", encoding="utf-8")

    wrong = [{"date": "2001-04-14", "result": "loss", "method": "SUB",
              "org": "MD 1 - Mass Destruction 1", "is_amateur": 0}]
    right = [{"date": "2025-10-14", "result": "win", "method": "KO/TKO",
              "org": "Jungle Fight 110", "is_amateur": 0}]

    load_regional_records(db, _write_cache(cache, wrong), empty_media)
    load_regional_records(db, _write_cache(cache, right), empty_media)

    rows = load_regional(db)["michael oliveira"]
    assert [f["date"] for f in rows] == ["2025-10-14"]
    assert regional_snapshot(rows, "2026-08-01")["pre_ufc_losses"] is None


def test_reloading_the_same_cache_twice_is_not_a_double_count(tmp_path):
    db = connect(tmp_path / "t.db")
    init_db(db)
    cache = tmp_path / "sherdog.json"
    empty_media = tmp_path / "media.json"
    empty_media.write_text("{}", encoding="utf-8")

    fights = [{"date": "2024-05-01", "result": "win", "method": "DEC",
               "org": "Cage Warriors", "is_amateur": 0}]
    _write_cache(cache, fights)
    load_regional_records(db, cache, empty_media)
    load_regional_records(db, cache, empty_media)

    assert len(load_regional(db)["michael oliveira"]) == 1


def _insert_ufc_fight(db, fighter: str, date: str) -> None:
    db.execute("INSERT INTO events (event_id, name, date, source) VALUES (?, ?, ?, 'test')",
               (hash((fighter, date)) % 10**6, "UFC Test", date))
    db.execute(
        "INSERT INTO fights (event_id, date, fighter1, fighter2, winner, title_fight, source) "
        "VALUES (?, ?, ?, ?, 'fighter1', 0, 'test')",
        (hash((fighter, date)) % 10**6, date, fighter, "Somebody Else"))
    db.commit()


def _cache_with_fetched(path, fights, fetched="2026-08-01T12:00:00"):
    path.write_text(json.dumps({
        "michael oliveira": {"name": "Michael Oliveira", "regional_fights": fights,
                             "fetched": fetched},
    }), encoding="utf-8")
    return path


def test_identity_guard_rejects_a_sherdog_page_missing_the_fighters_ufc_bouts(tmp_path):
    """A UFC veteran's real Sherdog page lists his UFC fights; a namesake's does not."""
    db = connect(tmp_path / "t.db")
    init_db(db)
    _insert_ufc_fight(db, "Michael Oliveira", "2019-05-04")
    empty_media = tmp_path / "media.json"
    empty_media.write_text("{}", encoding="utf-8")

    namesake = [{"date": "2001-04-14", "result": "loss", "method": "SUB",
                 "org": "MD 1 - Mass Destruction 1", "is_amateur": 0}]
    counts = load_regional_records(
        db, _cache_with_fetched(tmp_path / "wrong.json", namesake), empty_media)
    assert counts["rejected_identity"] == 1
    assert "michael oliveira" not in load_regional(db)

    genuine = namesake + [{"date": "2019-05-04", "result": "win", "method": "U-DEC",
                           "org": "UFC Fight Night 150", "is_amateur": 0}]
    counts = load_regional_records(
        db, _cache_with_fetched(tmp_path / "right.json", genuine), empty_media)
    assert counts["rejected_identity"] == 0
    # The UFC bout itself is still excluded (already in `fights`); the
    # regional bout is kept.
    assert [f["date"] for f in load_regional(db)["michael oliveira"]] == ["2001-04-14"]


def test_identity_guard_accepts_true_debutants_and_very_recent_ufc_bouts(tmp_path):
    db = connect(tmp_path / "t.db")
    init_db(db)
    empty_media = tmp_path / "media.json"
    empty_media.write_text("{}", encoding="utf-8")
    regional = [{"date": "2025-10-14", "result": "win", "method": "KO/TKO",
                 "org": "Jungle Fight 110", "is_amateur": 0}]

    # No UFC fights on file: nothing to check against, accept.
    counts = load_regional_records(
        db, _cache_with_fetched(tmp_path / "debut.json", regional), empty_media)
    assert counts["rejected_identity"] == 0

    # A UFC debut three days before the scrape: Sherdog may not list it yet.
    _insert_ufc_fight(db, "Michael Oliveira", "2026-07-29")
    counts = load_regional_records(
        db, _cache_with_fetched(tmp_path / "recent.json", regional), empty_media)
    assert counts["rejected_identity"] == 0


def test_regional_elo_beats_a_major_org_more_than_a_local_show():
    """Org quality is the opponent proxy: same record, different pedigree."""
    from octagon.features.regional import regional_elo

    win_major = [{"date": "2024-01-01", "result": "win", "method": "KO/TKO",
                  "org": "LFA 180", "is_amateur": 0}]
    win_local = [{"date": "2024-01-01", "result": "win", "method": "KO/TKO",
                  "org": "Gym Show 3", "is_amateur": 0}]
    assert regional_elo(win_major, "2025-01-01") > regional_elo(win_local, "2025-01-01")


def test_regional_elo_ignores_fights_on_or_after_the_snapshot_date():
    from octagon.features.regional import regional_elo

    fights = [
        {"date": "2024-01-01", "result": "win", "method": "DEC",
         "org": "LFA", "is_amateur": 0},
        {"date": "2025-06-01", "result": "win", "method": "KO/TKO",
         "org": "LFA", "is_amateur": 0},
    ]
    before = regional_elo(fights, "2025-01-01")
    after = regional_elo(fights[:1], "2025-01-01")
    assert before == after
    assert regional_elo([], "2025-01-01") is None

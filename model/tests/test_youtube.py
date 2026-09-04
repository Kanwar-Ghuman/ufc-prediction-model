"""YouTube buzz scoring — no network. The API client is stubbed elsewhere."""

from octagon.scraping import youtube
from octagon.scraping.context import soft_adjust_p_f1


def test_explicit_title_pick_leans_the_named_fighter():
    videos = [{"video_id": "a", "title": "UFC Belgrade Picks: Taking Medic by KO"}]
    buzz = youtube.score_bout_buzz(
        "Uros Medic", "Daniel Rodriguez", videos, {"a": []})
    assert buzz["lean_f1"] > 0.5
    assert buzz["preferred"] == "Uros Medic"
    assert buzz["n_signals"] >= 1


def test_comments_can_swing_the_lean():
    videos = [{"video_id": "a", "title": "Medic vs Rodriguez preview"}]
    comments = {
        "a": [
            "Rodriguez by decision all day",
            "taking D-Rod, Medic gets finished",
            "Rodriguez wins this easy",
        ],
    }
    # Surname match: Rodriguez is in the pick patterns via "wins"
    buzz = youtube.score_bout_buzz(
        "Uros Medic", "Daniel Rodriguez", videos, comments)
    assert buzz["lean_f1"] < 0
    assert buzz["n_signals"] >= 2


def test_thin_scrape_has_no_preferred_fighter():
    videos = [{"video_id": "a", "title": "UFC Fight Night highlights"}]
    buzz = youtube.score_bout_buzz("Alice", "Bob", videos, {"a": ["great card"]})
    assert buzz["preferred"] is None
    assert buzz["n_signals"] == 0


def test_youtube_nudge_only_when_skill_is_near_a_coin_flip():
    # Skill decisive → note only, no move.
    p, notes = soft_adjust_p_f1(
        0.75, 10, 10, None, None, None, None,
        has_market_odds=True, youtube_lean=0.8, youtube_n_signals=12,
        skill_p=0.75)
    assert p == 0.75
    assert any("not applied" in n for n in notes)

    # Skill coin flip → small nudge toward the crowd.
    p2, notes2 = soft_adjust_p_f1(
        0.50, 0, 4, None, None, None, None,
        has_market_odds=True, youtube_lean=0.8, youtube_n_signals=12,
        skill_p=0.50)
    assert p2 > 0.50
    assert any("nudged" in n for n in notes2)


def test_agreement_note_flags_disagreement():
    note = youtube.agreement_note(
        0.75, youtube_lean=-0.6, n_signals=10,
        f1="Uros Medic", f2="Daniel Rodriguez")
    assert note is not None
    assert "disagrees" in note
    assert "Rodriguez" in note

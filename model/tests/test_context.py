"""Unit tests for day-before context and style clash features."""

import pytest

from octagon.features.style import style_matchup, style_scores
from octagon.db.parsing import normalize_name
from octagon.scraping.context import (
    parse_circumstances,
    parse_pro_record,
    soft_adjust_p_f1,
)


def test_parse_pro_record():
    rec = parse_pro_record("16-2-0")
    assert rec is not None
    assert rec["wins"] == 16 and rec["losses"] == 2
    assert 0.8 < rec["win_pct"] < 0.95


def test_parse_circumstances_short_notice():
    background = (
        "Navajo Stirling steps in against Jan Blachowicz on less than "
        "three weeks' notice after Bogdan Guskov was moved."
    )
    names = ["Jan Błachowicz", "Navajo Stirling", "Uroš Medić"]
    flags = parse_circumstances(background, names)
    stirling = flags["navajo stirling"]
    assert stirling["short_notice"] is True
    assert stirling["notes"]
    # The weeks'-notice phrase should not falsely pin the veteran opponent.
    assert flags[normalize_name("Jan Błachowicz")]["short_notice"] is False


def test_soft_adjust_debut_prior_raises_good_record():
    p, notes = soft_adjust_p_f1(
        0.50, f1_n_fights=0, f2_n_fights=5,
        f1_record={"wins": 16, "losses": 2, "draws": 0, "win_pct": 0.89},
        f2_record=None, f1_flags=None, f2_flags=None,
        has_market_odds=False,
    )
    assert p > 0.50
    assert any("debut prior" in n for n in notes)


def test_soft_adjust_short_notice_dampens_even_with_odds():
    p, notes = soft_adjust_p_f1(
        0.80, f1_n_fights=10, f2_n_fights=5,
        f1_record=None, f2_record=None,
        f1_flags=None,
        f2_flags={"short_notice": True, "late_replacement": False, "notes": []},
        has_market_odds=True,
    )
    assert p < 0.80
    assert any("short notice" in n for n in notes)


def test_soft_adjust_skips_debut_prior_when_priced():
    p, notes = soft_adjust_p_f1(
        0.55, f1_n_fights=0, f2_n_fights=5,
        f1_record={"wins": 16, "losses": 2, "draws": 0, "win_pct": 0.89},
        f2_record=None, f1_flags=None, f2_flags=None,
        has_market_odds=True,
    )
    assert p == 0.55
    assert notes == []


def test_replacement_is_attributed_to_the_incoming_fighter():
    """The man who arrives on short notice gets the flag, not the man who
    withdrew — UFC 330's Ochoa -> Chapolin swap read backwards before."""
    background = (
        "Jose Ochoa was scheduled to face former LFA Flyweight Champion "
        "Charles Johnson in a flyweight bout. However, Ochoa pulled out for "
        "undisclosed reasons three days before the event and was replaced by "
        "promotional newcomer and fellow former LFA flyweight champion "
        "Eduardo Henrique in a 130 pound catchweight bout."
    )
    flags = parse_circumstances(
        background, ["Charles Johnson", "Eduardo Chapolin"],
        aliases={"Eduardo Henrique": "Eduardo Chapolin"})

    incoming = flags[normalize_name("Eduardo Chapolin")]
    assert incoming["short_notice"] is True
    assert incoming["late_replacement"] is True
    # The opponent who kept his booking is not the one on short notice.
    assert flags[normalize_name("Charles Johnson")]["short_notice"] is False


def test_replacement_without_a_time_cue_is_not_short_notice():
    """An opponent swap announced well in advance is a different animal."""
    background = ("However, Neal had to withdraw for undisclosed reasons "
                  "and was replaced by Joel Alvarez.")
    flags = parse_circumstances(background, ["Chidi Njokuani", "Joel Alvarez"])

    alvarez = flags[normalize_name("Joel Alvarez")]
    assert alvarez["late_replacement"] is True
    assert alvarez["short_notice"] is False


def test_resolver_refuses_ambiguous_shared_surnames():
    """'Johnson' names two men on the UFC 330 card — guessing is worse than
    admitting defeat, so the resolver must decline."""
    from octagon.scraping.context import build_resolver

    resolve = build_resolver(["Charles Johnson", "Donte Johnson",
                              "Eduardo Chapolin"])
    assert resolve("Johnson") is None
    assert resolve("Charles Johnson") == normalize_name("Charles Johnson")
    # A unique token still resolves.
    assert resolve("Chapolin") == normalize_name("Eduardo Chapolin")


def test_bout_features_are_swap_invariant():
    """bout_* must be symmetric — the whole symmetry machinery leaves them
    untouched, so an asymmetric one would silently leak corner identity."""
    from octagon.features.build import bout_features

    a = {
        "finish_involvement": 0.7, "ko_win_rate": 0.5, "sub_win_rate": 0.1,
        "dec_win_rate": 0.2, "late_finish_rate": 0.1, "avg_end_round": 1.8,
        "r1_win_rate": 0.4, "r1_loss_rate": 0.1, "times_koed": 1,
        "times_subbed": 0, "n_fights": 10, "kd15_l5": 0.8, "sub15_l5": 0.2,
        "slpm_l5": 5.0, "ctrl_pct_l5": 0.1, "layoff_days": 200, "age": 31.0,
        "elo": 1700.0, "ko_share": 0.7, "ko_end_rate_l5": 0.6, "sub_end_rate_l5": 0.1,
    }
    b = {
        "finish_involvement": 0.2, "ko_win_rate": 0.1, "sub_win_rate": 0.05,
        "dec_win_rate": 0.6, "late_finish_rate": 0.4, "avg_end_round": 2.9,
        "r1_win_rate": 0.05, "r1_loss_rate": 0.2, "times_koed": 3,
        "times_subbed": 2, "n_fights": 20, "kd15_l5": 0.1, "sub15_l5": 0.6,
        "slpm_l5": 2.5, "ctrl_pct_l5": 0.4, "layoff_days": 400, "age": 36.0,
        "elo": 1500.0, "ko_share": 0.2, "ko_end_rate_l5": 0.2, "sub_end_rate_l5": 0.05,
    }
    assert bout_features(a, b) == bout_features(b, a)
    assert bout_features(a, b)["bout_elo_gap"] == pytest.approx(200.0)
    assert bout_features(a, b)["bout_finish_max"] == pytest.approx(0.7)


def test_bout_features_separate_finishers_from_grinders():
    """A differential cannot tell these apart — that was the bug."""
    from octagon.features.build import bout_features

    killer = {"finish_involvement": 0.9, "ko_win_rate": 0.8,
              "avg_end_round": 1.2, "n_fights": 10}
    grinder = {"finish_involvement": 0.1, "ko_win_rate": 0.05,
               "avg_end_round": 3.0, "n_fights": 10}
    two_killers = bout_features(killer, killer)
    two_grinders = bout_features(grinder, grinder)
    assert two_killers["bout_finish_involvement"] > two_grinders["bout_finish_involvement"]
    assert two_killers["bout_ko_rate"] > two_grinders["bout_ko_rate"]
    assert two_killers["bout_finish_max"] > two_grinders["bout_finish_max"]
    assert two_killers["bout_avg_end_round"] < two_grinders["bout_avg_end_round"]


def test_method_base_rate_is_symmetric_and_normalised():
    import pandas as pd

    from octagon.models import method

    train = pd.DataFrame({
        "label": [1, 0, 1, 0] * 15,
        "method": ["KO/TKO", "U-DEC", "SUB", "KO/TKO"] * 15,
        "weight_class": ["Heavyweight"] * 60,
        "scheduled_rounds": [3] * 60,
    })
    upcoming = pd.DataFrame({
        "weight_class": ["Heavyweight"], "scheduled_rounds": [3],
    })
    base = method.base_rate_methods(method.trainable(train), upcoming)
    row = base.iloc[0]
    assert abs(row[method.CLASSES[:3]].sum() - 1.0) < 1e-9
    assert abs(row[method.CLASSES[3:]].sum() - 1.0) < 1e-9
    for group in method.GROUPS:
        assert abs(row[f"f1_{group}"] - row[f"f2_{group}"]) < 1e-12


def test_style_scores_and_matchup_antisymmetry():
    striker = {
        "slpm_l5": 6.0, "head_share_l5": 0.7, "kd15_l5": 0.5,
        "td15_l5": 0.2, "td_acc_l5": 0.2, "ctrl_pct_l5": 0.1,
        "ground_share_l5": 0.1, "sub15_l5": 0.0, "sub_win_rate": 0.0,
        "clinch_share_l5": 0.1, "td_def_l5": 0.8,
        "ground_absorbed_share_l5": 0.2,
    }
    wrestler = {
        "slpm_l5": 2.0, "head_share_l5": 0.4, "kd15_l5": 0.05,
        "td15_l5": 4.0, "td_acc_l5": 0.6, "ctrl_pct_l5": 0.5,
        "ground_share_l5": 0.5, "sub15_l5": 0.3, "sub_win_rate": 0.2,
        "clinch_share_l5": 0.3, "td_def_l5": 0.4,
        "ground_absorbed_share_l5": 0.4,
    }
    assert style_scores(striker)["striker"] > style_scores(wrestler)["striker"]
    assert style_scores(wrestler)["wrestler"] > style_scores(striker)["wrestler"]
    fwd = style_matchup(striker, wrestler)
    rev = style_matchup(wrestler, striker)
    for key in fwd:
        if fwd[key] is None:
            assert rev[key] is None
        else:
            assert abs(fwd[key] + rev[key]) < 1e-9, key


def test_an_unquoted_card_date_is_coerced_before_the_scrape_is_saved(tmp_path,
                                                                    monkeypatch):
    """PyYAML turns `date: 2026-08-08` into a date object, which json.dumps
    rejects — and it used to do so only at save time, after the whole scrape
    (and its YouTube quota) had been spent."""
    import json

    from octagon.scraping import context as ctx

    card = tmp_path / "cards" / "c.yaml"
    card.parent.mkdir(parents=True)
    card.write_text(
        "date: 2026-08-08\nevent: Test Card\n"
        "fights:\n  - fighter1: A One\n    fighter2: B Two\n",
        encoding="utf-8")

    # Keep the test offline: every network helper returns something empty.
    monkeypatch.setattr(ctx, "event_background", lambda page: "")
    monkeypatch.setattr(ctx, "news_headlines", lambda *a, **k: [])
    monkeypatch.setattr(ctx, "_wiki_summary", lambda name: {})

    payload = ctx.fetch_card_context(card, media_cache={}, delay=0.0)

    assert payload["date"] == "2026-08-08"
    json.dumps(payload)  # the failure this test exists for

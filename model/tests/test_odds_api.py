"""Odds API matching and consensus — no network."""

from octagon.betting.odds_api import (
    consensus_h2h,
    match_bout,
    write_odds_to_card,
)


def _event(home, away, commence, books):
    return {
        "home_team": home,
        "away_team": away,
        "commence_time": commence,
        "bookmakers": [
            {"markets": [{"key": "h2h", "outcomes": [
                {"name": home, "price": prices[0]},
                {"name": away, "price": prices[1]},
            ]}]}
            for prices in books
        ],
    }


def test_consensus_is_the_median_across_books():
    event = _event("Islam Makhachev", "Arman Tsarukyan",
                   "2026-07-11T00:00:00Z",
                   [(1.40, 3.10), (1.50, 2.70), (1.44, 2.90)])
    prices = consensus_h2h(event)
    assert prices["Islam Makhachev"] == 1.44
    assert prices["Arman Tsarukyan"] == 2.90


def test_match_survives_name_order_and_accents():
    events = [_event("Zhang Weili", "Tatiana Suarez",
                     "2026-08-22T03:00:00Z", [(1.55, 2.50)])]
    # Card lists given-name first; book lists family name first.
    matched = match_bout("Weili Zhang", "Tatiana Suarez", "2026-08-21", events)
    assert matched == (1.55, 2.50)


def test_match_allows_short_given_names():
    events = [_event("Stan Dorsainvil", "Gauge Young",
                     "2026-08-22T22:15:00Z", [(2.10, 1.75)])]
    matched = match_bout("Gauge Young", "Stanley Dorsainvil", "2026-08-22", events)
    assert matched == (1.75, 2.10)


def test_unmatched_bout_stays_empty():
    events = [_event("A", "B", "2026-01-01T00:00:00Z", [(1.8, 2.0)])]
    assert match_bout("C", "D", "2026-01-01", events) is None


def test_write_odds_fills_card_order_not_home_away():
    events = [_event("Bob", "Alice", "2026-05-01T00:00:00Z", [(2.20, 1.70)])]
    card = {
        "date": "2026-05-01",
        "fights": [
            {"fighter1": "Alice", "fighter2": "Bob", "odds": None},
            {"fighter1": "Nobody", "fighter2": "Else", "odds": None},
        ],
    }
    updated, n = write_odds_to_card(card, events)
    assert n == 1
    assert updated["fights"][0]["odds"] == [1.70, 2.20]
    assert updated["fights"][1]["odds"] is None


def test_keep_existing_odds_when_overwrite_is_false():
    events = [_event("Alice", "Bob", "2026-05-01T00:00:00Z", [(1.10, 8.00)])]
    card = {"date": "2026-05-01",
            "fights": [{"fighter1": "Alice", "fighter2": "Bob", "odds": [1.45, 2.85]}]}
    updated, n = write_odds_to_card(card, events, overwrite=False)
    assert n == 0
    assert updated["fights"][0]["odds"] == [1.45, 2.85]

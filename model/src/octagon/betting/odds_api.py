"""Upcoming moneylines from The Odds API — predict-time only.

The free tier returns current/upcoming events, not historical backfill, so
these numbers never enter training or the 2024+ holdout. They are written
onto card YAMLs so `predict` can ship the market-aware stack without a
hand-pasted line.

API key: environment variable named in config (`ODDS_API_KEY`), never committed.
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from statistics import median
from typing import Any

import requests

from octagon.db.parsing import normalize_name

ODDS_API = "https://api.the-odds-api.com/v4/sports/{sport}/odds"
DEFAULT_SPORT = "mma_mixed_martial_arts"
DEFAULT_REGIONS = "us"
USER_AGENT = "octagon-oracle/0.1 (educational UFC prediction project)"


def consensus_h2h(event: dict) -> dict[str, float]:
    """Median decimal moneyline per fighter across bookmakers."""
    buckets: dict[str, list[float]] = {}
    for book in event.get("bookmakers") or []:
        for market in book.get("markets") or []:
            if market.get("key") != "h2h":
                continue
            for outcome in market.get("outcomes") or []:
                name, price = outcome.get("name"), outcome.get("price")
                if not name or not isinstance(price, (int, float)) or price <= 1:
                    continue
                buckets.setdefault(name, []).append(float(price))
    return {name: float(median(prices)) for name, prices in buckets.items()
            if prices}


def _event_date(event: dict) -> date | None:
    raw = event.get("commence_time")
    if not raw:
        return None
    try:
        stamp = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return stamp.astimezone(timezone.utc).date()


def _event_names(event: dict) -> set[str]:
    return {normalize_name(event.get("home_team") or ""),
            normalize_name(event.get("away_team") or "")} - {""}


def names_compatible(a: str, b: str) -> bool:
    """True when two listings are the same person, including Stan/Stanley.

    Tokens are compared as a bag (so 'Zhang Weili' matches 'Weili Zhang').
    If the bags differ by one token, a prefix given-name is allowed.
    """
    if not a or not b:
        return False
    left, right = set(normalize_name(a).split()), set(normalize_name(b).split())
    if not left or not right:
        return False
    if left == right:
        return True
    if len(left) != len(right):
        return False
    only_a, only_b = left - right, right - left
    if len(only_a) != 1 or len(only_b) != 1:
        return False
    given_a, given_b = only_a.pop(), only_b.pop()
    return given_a.startswith(given_b) or given_b.startswith(given_a)


def _pair_event(fighter1: str, fighter2: str, event: dict) -> bool:
    home, away = event.get("home_team") or "", event.get("away_team") or ""
    return ((names_compatible(fighter1, home) and names_compatible(fighter2, away))
            or (names_compatible(fighter1, away) and names_compatible(fighter2, home)))


def _date_close(event: dict, iso_date: str, slack_days: int = 1) -> bool:
    event_day = _event_date(event)
    if event_day is None:
        return True
    try:
        card_day = date.fromisoformat(iso_date)
    except ValueError:
        return True
    return abs((event_day - card_day).days) <= slack_days


def match_bout(
    fighter1: str,
    fighter2: str,
    iso_date: str,
    events: list[dict],
) -> tuple[float, float] | None:
    """Decimal odds for (fighter1, fighter2), or None if unmatched."""
    want = {normalize_name(fighter1), normalize_name(fighter2)}
    if len(want) != 2:
        return None
    hits = [event for event in events if _event_names(event) == want]
    if not hits:
        hits = [event for event in events if _pair_event(fighter1, fighter2, event)]
    if not hits:
        return None
    dated = [event for event in hits if _date_close(event, iso_date)]
    event = (dated or hits)[0]
    prices = {normalize_name(name): price
              for name, price in consensus_h2h(event).items()}
    left = prices.get(normalize_name(fighter1))
    right = prices.get(normalize_name(fighter2))
    if left is None or right is None:
        # Nickname / short-given-name path: map via compatible().
        for name, price in consensus_h2h(event).items():
            if left is None and names_compatible(fighter1, name):
                left = price
            elif right is None and names_compatible(fighter2, name):
                right = price
    if left is None or right is None:
        return None
    return (round(left, 3), round(right, 3))


def fetch_mma_odds(
    api_key: str,
    sport: str = DEFAULT_SPORT,
    regions: str = DEFAULT_REGIONS,
    session: requests.Session | None = None,
    timeout: float = 30.0,
) -> tuple[list[dict], dict[str, str]]:
    """Pull upcoming MMA h2h odds. Returns (events, response headers of interest)."""
    http = session or requests.Session()
    response = http.get(
        ODDS_API.format(sport=sport),
        params={
            "apiKey": api_key,
            "regions": regions,
            "markets": "h2h",
            "oddsFormat": "decimal",
        },
        headers={"User-Agent": USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict):
        raise ValueError(str(payload.get("message") or payload))
    events = payload if isinstance(payload, list) else []
    meta = {
        "remaining": response.headers.get("x-requests-remaining", ""),
        "used": response.headers.get("x-requests-used", ""),
    }
    return events, meta


def write_odds_to_card(
    card: dict[str, Any],
    events: list[dict],
    overwrite: bool = True,
) -> tuple[dict[str, Any], int]:
    """Fill `fights[].odds` from matched Odds API events. Returns (card, n_filled)."""
    iso_date = str(card.get("date") or "")
    filled = 0
    for fight in card.get("fights") or []:
        if not overwrite and fight.get("odds"):
            continue
        matched = match_bout(fight["fighter1"], fight["fighter2"], iso_date, events)
        if matched is None:
            continue
        fight["odds"] = [matched[0], matched[1]]
        filled += 1
    return card, filled

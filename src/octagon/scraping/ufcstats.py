"""Parsers for ufcstats.com pages.

Scope for M1: the completed-events index and event pages (fight results +
per-fight stat totals). Fight-details and fighter pages come in M2 when the
feature builder needs them.

Parsers take HTML strings (from the cache — see fetch.py) and return plain
dicts, so they can be re-run and tested without any network access. Every
URL on ufcstats embeds a stable hex ID (e.g. /event-details/<id>); we keep
those IDs because names are not unique.
"""

import re
from datetime import datetime

from bs4 import BeautifulSoup

BASE_URL = "http://ufcstats.com"
COMPLETED_EVENTS_URL = f"{BASE_URL}/statistics/events/completed?page=all"


def _id_from_url(url: str) -> str:
    """'http://ufcstats.com/event-details/abc123' -> 'abc123'."""
    return url.rstrip("/").rsplit("/", 1)[-1]


def _parse_date(text: str) -> str | None:
    """'September 16, 2023' -> '2023-09-16'."""
    try:
        return datetime.strptime(text.strip(), "%B %d, %Y").date().isoformat()
    except ValueError:
        return None


def parse_events_index(html: str) -> list[dict]:
    """Parse the completed-events listing into event dicts.

    Returns [{'event_id', 'name', 'url', 'date', 'location'}, ...] sorted as
    listed (newest first). Rows without a parseable date (e.g. the 'next
    event' teaser row) are skipped.
    """
    soup = BeautifulSoup(html, "lxml")
    events = []
    for row in soup.select("tr.b-statistics__table-row"):
        link = row.select_one("a.b-link")
        date_span = row.select_one("span.b-statistics__date")
        if link is None or date_span is None:
            continue
        date = _parse_date(date_span.get_text())
        if date is None:
            continue
        cols = row.select("td")
        location = cols[-1].get_text(strip=True) if len(cols) >= 2 else None
        events.append({
            "event_id": _id_from_url(link["href"]),
            "name": link.get_text(strip=True),
            "url": link["href"],
            "date": date,
            "location": location,
        })
    return events


def parse_event_page(html: str) -> list[dict]:
    """Parse one event page into a list of fight dicts.

    Each fight: fighter names + ufcstats IDs, winner ('fighter1'/'fighter2'/
    'draw'/'nc' — ufcstats lists the winner first), per-fighter Kd/Str/Td/Sub
    totals, weight class, method (+detail), round, time, and the
    fight-details URL for deeper stats later.
    """
    soup = BeautifulSoup(html, "lxml")
    fights = []
    for row in soup.select("tr.b-fight-details__table-row[data-link]"):
        cols = row.select("td.b-fight-details__table-col")
        if len(cols) < 10:
            continue

        fighter_links = cols[1].select("a")
        if len(fighter_links) != 2:
            continue
        names = [a.get_text(strip=True) for a in fighter_links]
        ids = [_id_from_url(a["href"]) for a in fighter_links]

        # The W/L column: 'win' on the first fighter means fighter1 won;
        # draws and no-contests are flagged with 'draw'/'nc' text.
        flags = [f.get_text(strip=True).lower() for f in cols[0].select("a, i")]
        flag_text = " ".join(flags)
        if "nc" in flag_text:
            winner = "nc"
        elif "draw" in flag_text:
            winner = "draw"
        elif "win" in flag_text:
            winner = "fighter1"
        else:
            winner = None  # upcoming fight on a future card

        def pair(col_idx: int) -> tuple[int | None, int | None]:
            """Stat columns hold one <p> per fighter."""
            values = [p.get_text(strip=True) for p in cols[col_idx].select("p")]
            if len(values) != 2:
                return None, None
            try:
                return int(values[0]), int(values[1])
            except ValueError:
                return None, None

        method_ps = [p.get_text(strip=True) for p in cols[7].select("p")]
        method = method_ps[0] if method_ps else None
        method_detail = method_ps[1] if len(method_ps) > 1 and method_ps[1] else None

        round_text = cols[8].get_text(strip=True)
        fights.append({
            "fight_url": row["data-link"],
            "fight_id": _id_from_url(row["data-link"]),
            "fighter1": names[0], "fighter1_id": ids[0],
            "fighter2": names[1], "fighter2_id": ids[1],
            "winner": winner,
            "kd": pair(2), "sig_str": pair(3), "td": pair(4), "sub": pair(5),
            "weight_class": cols[6].get_text(strip=True) or None,
            "method": method, "method_detail": method_detail,
            "end_round": int(round_text) if re.fullmatch(r"\d+", round_text) else None,
            "end_time": cols[9].get_text(strip=True) or None,
        })
    return fights

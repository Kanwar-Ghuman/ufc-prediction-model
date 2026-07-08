"""Fetch upcoming UFC cards from Wikipedia (the ethical scrape).

ufcstats.com is bot-walled; Wikipedia has a proper API, a permissive
license, and — crucially for us — the announced fight card of every
upcoming UFC event, updated by fans within hours of changes. Two requests
per card build: the events list, then the event page.

Caveats printed on every generated card: Wikipedia fighter spellings can
differ from ufcstats ('Alexander Volkanovski' vs 'Alex Volkanovski' style);
`octagon predict` flags any fighter it can't find, and the YAML is meant
to be reviewed by a human before predicting. Odds are left null — add
decimal odds by hand if you want the market comparison and the stack.
"""

import re
from datetime import date, datetime

import requests
from bs4 import BeautifulSoup

API = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "octagon-oracle/0.1 (educational UFC prediction project)"


def _page_html(title: str) -> str:
    resp = requests.get(API, params={
        "action": "parse", "page": title, "prop": "text",
        "format": "json", "formatversion": 2,
    }, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    return resp.json()["parse"]["text"]


def _clean(cell) -> str:
    return " ".join(cell.get_text(" ", strip=True).split())


def next_event(today: date | None = None) -> tuple[str, str, str]:
    """(wiki page title, event name, ISO date) of the nearest future event."""
    today = today or date.today()
    soup = BeautifulSoup(_page_html("List of UFC events"), "lxml")
    header = soup.find(id="Scheduled_events")
    table = header.find_next("table")
    best = None
    for row in table.select("tr"):
        cells = row.select("td")
        if len(cells) < 2:
            continue
        try:
            when = datetime.strptime(_clean(cells[1]), "%b %d, %Y").date()
        except ValueError:
            continue
        link = cells[0].find("a")
        if when >= today and link and (best is None or when < best[2]):
            best = (link["title"], _clean(cells[0]), when)
    if best is None:
        raise SystemExit("No scheduled UFC event found on Wikipedia.")
    return best[0], best[1], best[2].isoformat()


def fight_card(page_title: str) -> list[dict]:
    """Announced bouts: [{weight_class, fighter1, fighter2, title_fight}]."""
    soup = BeautifulSoup(_page_html(page_title), "lxml")
    bouts = []
    for row in soup.select("table tr"):
        cells = [_clean(c) for c in row.select("td")]
        if len(cells) >= 4 and cells[2] == "vs.":
            weight, f1, f2 = cells[0], cells[1], cells[3]
            title = "(c)" in f1 or "(c)" in f2 or "Title" in weight
            bouts.append({
                "weight_class": re.sub(r"\s*Title.*$", "", weight).strip(),
                "fighter1": f1.replace("(c)", "").strip(),
                "fighter2": f2.replace("(c)", "").strip(),
                "title_fight": title,
            })
    return bouts


def card_yaml(event_name: str, iso_date: str, bouts: list[dict]) -> dict:
    """The dict that predict's card loader consumes (see cards/*.yaml)."""
    fights = []
    for i, b in enumerate(bouts):
        fights.append({
            "fighter1": b["fighter1"],
            "fighter2": b["fighter2"],
            "weight_class": b["weight_class"],
            "title_fight": b["title_fight"],
            # Main event and title fights are five rounds.
            "rounds": 5 if (i == 0 or b["title_fight"]) else 3,
            "odds": None,  # add [f1_decimal, f2_decimal] by hand if desired
        })
    return {"date": iso_date, "event": event_name, "fights": fights}

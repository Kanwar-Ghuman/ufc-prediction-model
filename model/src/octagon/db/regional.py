"""Load regional fights from Sherdog/Wikipedia caches.

UFC bouts on Sherdog are dropped by organization name, not by debut date.
"""

import json
import re
import sqlite3
from datetime import date, timedelta
from pathlib import Path

_UFC_ORG = re.compile(r"\bUFC\b", re.IGNORECASE)

# A Sherdog page is only trusted for a fighter with UFC fights in our DB if
# it lists at least one of those UFC bouts on (about) the same date. Bouts
# newer than this many days before the scrape are excused — Sherdog lags a
# live card by a few days.
_RECENT_GRACE_DAYS = 14


def _ufc_dates(conn: sqlite3.Connection) -> dict[str, set[date]]:
    """Every fighter's UFC fight dates as known to the canonical table."""
    out: dict[str, set[date]] = {}
    try:
        rows = conn.execute("SELECT fighter1, fighter2, date FROM fights").fetchall()
    except sqlite3.OperationalError:
        return out
    for f1, f2, d in rows:
        day = date.fromisoformat(str(d)[:10])
        out.setdefault(f1, set()).add(day)
        out.setdefault(f2, set()).add(day)
    return out


def _is_same_person(record: dict, known_ufc: set[date]) -> bool:
    """Does this Sherdog record belong to the fighter our fights table knows?

    Sherdog's name search returns the first fighter with a matching name,
    and for common names that can be a different athlete entirely. For a
    fighter who has already fought in the UFC the page has to prove itself:
    Sherdog carries UFC bouts too, so a genuine match lists at least one UFC
    fight within a day of one in our DB. Pure debutants (no UFC fights on
    file) cannot be checked this way and are accepted as before.
    """
    if not known_ufc:
        return True
    fetched = str(record.get("fetched") or "")[:10]
    try:
        cutoff = date.fromisoformat(fetched) - timedelta(days=_RECENT_GRACE_DAYS)
    except ValueError:
        cutoff = date.max
    checkable = {d for d in known_ufc if d <= cutoff}
    if not checkable:
        return True
    sherdog_ufc: set[date] = set()
    for fight in record.get("regional_fights", []):
        if fight.get("date") and _UFC_ORG.search(fight.get("org") or ""):
            try:
                sherdog_ufc.add(date.fromisoformat(fight["date"]))
            except ValueError:
                continue
    if not sherdog_ufc:
        return False
    return any(abs((a - b).days) <= 1 for a in checkable for b in sherdog_ufc)


def load_regional_records(
    conn: sqlite3.Connection,
    sherdog_cache_path: Path,
    media_cache_path: Path,
) -> dict[str, int]:
    """Load regional fights and titles into the DB.

    Returns a dict of table -> row count inserted (plus how many cached
    fighters were rejected as a different person, see _is_same_person).
    """
    conn.row_factory = sqlite3.Row

    sherdog_data = _load_json(sherdog_cache_path)
    wiki_data = _load_json(media_cache_path)
    ufc_dates = _ufc_dates(conn)

    regional_count = 0
    title_count = 0
    rejected = 0

    for cache_key, record in sherdog_data.items():
        # The cache is keyed by normalize_name() (sorted, folded tokens) —
        # the real display name for this row is record["name"].
        fighter_name = record.get("name", cache_key)
        # The cache is the source of truth for this fighter, so clear them out
        # first rather than merging into whatever a previous run left behind.
        # A re-scrape is often a *correction* — Sherdog's name search had
        # matched a different Michael Oliveira — and merging would keep the
        # phantom bout alongside the real record instead of replacing it.
        conn.execute("DELETE FROM regional_fights WHERE fighter_name = ? "
                     "AND source = ?", (fighter_name, "sherdog"))
        if not _is_same_person(record, ufc_dates.get(fighter_name, set())):
            rejected += 1
            continue
        for fight in record.get("regional_fights", []):
            fight_date = fight.get("date")
            org = fight.get("org") or ""
            if not fight_date or _UFC_ORG.search(org):
                continue  # no date to anchor on, or already in `fights`

            try:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO regional_fights
                    (fighter_name, date, opponent, result, method, org, is_amateur, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        fighter_name,
                        fight_date,
                        fight.get("opponent"),
                        fight.get("result", ""),
                        fight.get("method"),
                        org,
                        fight.get("is_amateur", 0),
                        fight.get("source", "sherdog"),
                    ),
                )
                regional_count += 1
            except sqlite3.IntegrityError:
                pass  # duplicate row, skip

    for cache_key, record in wiki_data.items():
        if not isinstance(record, dict):
            continue
        fighter_name = record.get("name", cache_key)
        for title in record.get("other_org_titles") or []:
            if not title:
                continue
            try:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO other_org_titles
                    (fighter_name, org, title, date_won, source)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        fighter_name,
                        _extract_org_from_title(title),
                        title,
                        None,  # date_won not available from Wikipedia yet
                        "wikipedia",
                    ),
                )
                title_count += 1
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    return {
        "regional_fights": regional_count,
        "other_org_titles": title_count,
        "rejected_identity": rejected,
    }


def _load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, IOError):
        return {}


def _extract_org_from_title(title: str) -> str:
    """Extract organization name from a title string like 'Bellator champion'."""
    if "champion" in title.lower():
        parts = title.split()
        if len(parts) > 0:
            return parts[0]
    return title[:30]  # Fallback to first 30 chars

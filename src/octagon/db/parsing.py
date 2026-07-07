"""Pure parsing helpers shared by all data loaders (unit-tested, no I/O).

Both raw sources (bootstrap CSVs and the Greco ufcstats scrape) encode the
same facts slightly differently — '155lbs.' vs '155 lbs.', 'Jul13,1978' vs
'Jul 13, 1978' — so every parser here accepts both spellings.
"""

import math
import re
import unicodedata
from datetime import datetime

MISSING = {"", "--", "---", "nan", "NA", None}


def parse_float(s: str | None) -> float | None:
    if s in MISSING:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def parse_valid_odds(s: str | None) -> float | None:
    """Decimal odds, or None if unusable.

    The bootstrap contains literal 'inf' strings (54 rows) which float()
    happily accepts — those and anything <= 1.0 (no payout) are garbage.
    """
    value = parse_float(s)
    if value is None or not math.isfinite(value) or value <= 1.0:
        return None
    return value


def parse_height_to_cm(s: str | None) -> float | None:
    """`5'11"` or `5' 11"` -> 180.34 cm."""
    m = re.match(r"(\d+)'\s*(\d+)\"", s or "")
    if not m:
        return None
    inches = int(m.group(1)) * 12 + int(m.group(2))
    return round(inches * 2.54, 2)


def parse_reach_to_cm(s: str | None) -> float | None:
    """'66"' -> 167.64 cm."""
    m = re.match(r"([\d.]+)\"", (s or "").strip())
    return round(float(m.group(1)) * 2.54, 2) if m else None


def parse_weight_to_kg(s: str | None) -> float | None:
    """'155lbs.' or '155 lbs.' -> 70.31 kg."""
    m = re.match(r"([\d.]+)\s*lbs", (s or "").strip())
    return round(float(m.group(1)) * 0.453592, 2) if m else None


def parse_dob(s: str | None) -> str | None:
    """'Jul13,1978' or 'Jul 13, 1978' -> '1978-07-13' (ISO, sortable)."""
    if s in MISSING:
        return None
    try:
        return datetime.strptime((s or "").replace(" ", ""), "%b%d,%Y").date().isoformat()
    except ValueError:
        return None


def parse_long_date(s: str | None) -> str | None:
    """'May 16, 2026' -> '2026-05-16' (event dates on ufcstats)."""
    if s in MISSING:
        return None
    try:
        return datetime.strptime((s or "").strip(), "%B %d, %Y").date().isoformat()
    except ValueError:
        return None


def parse_percent(s: str | None) -> float | None:
    """'38%' -> 0.38."""
    m = re.match(r"([\d.]+)%", s or "")
    return float(m.group(1)) / 100 if m else None


def parse_of_pair(s: str | None) -> tuple[int | None, int | None]:
    """'9 of 12' -> (9, 12): landed of attempted."""
    m = re.match(r"(\d+)\s+of\s+(\d+)", (s or "").strip())
    if not m:
        return None, None
    return int(m.group(1)), int(m.group(2))


def parse_mmss_to_seconds(s: str | None) -> int | None:
    """'1:44' -> 104 seconds (control time, end time)."""
    m = re.match(r"(\d+):(\d+)", (s or "").strip())
    if not m:
        return None
    return int(m.group(1)) * 60 + int(m.group(2))


def parse_time_format(s: str | None) -> list[int] | None:
    """'3 Rnd (5-5-5)' -> [5, 5, 5] round lengths in minutes.

    Old-era formats like '1 Rnd (20)' or '1 Rnd + OT (12-3)' parse too;
    'No Time Limit' returns None.
    """
    m = re.search(r"\((\d+(?:-\d+)*)\)", s or "")
    if not m:
        return None
    return [int(x) for x in m.group(1).split("-")]


def fight_duration_seconds(
    end_round: int | None, end_time_s: int | None, round_minutes: list[int] | None
) -> int | None:
    """Total fight length: full rounds before the last one, plus end time.

    Needed for per-minute stat rates. Falls back to 5-minute rounds when the
    format is unknown (true for every modern fight).
    """
    if end_round is None or end_time_s is None:
        return None
    full_rounds = range(end_round - 1)
    if round_minutes is None or len(round_minutes) < end_round:
        prior = sum(5 * 60 for _ in full_rounds)
    else:
        prior = sum(round_minutes[i] * 60 for i in full_rounds)
    return prior + end_time_s


# --- fight_results-specific decoding -------------------------------------

# Longest-first so 'Light Heavyweight' wins over 'Heavyweight' and
# "Women's X" wins over 'X'.
_WEIGHT_CLASSES = [
    "Women's Strawweight", "Women's Flyweight", "Women's Bantamweight",
    "Women's Featherweight", "Light Heavyweight", "Heavyweight",
    "Middleweight", "Welterweight", "Lightweight", "Featherweight",
    "Bantamweight", "Flyweight", "Strawweight", "Catch Weight", "Open Weight",
]

_METHOD_MAP = {
    "Decision - Unanimous": ("U-DEC", None),
    "Decision - Split": ("S-DEC", None),
    "Decision - Majority": ("M-DEC", None),
    "KO/TKO": ("KO/TKO", None),
    "Submission": ("SUB", None),
    "TKO - Doctor's Stoppage": ("KO/TKO", "Doctor's Stoppage"),
}

_OUTCOME_MAP = {"W/L": "fighter1", "L/W": "fighter2", "D/D": "draw", "NC/NC": "nc"}


def parse_weightclass(s: str | None) -> tuple[str | None, bool]:
    """'UFC Featherweight Title Bout' -> ('Featherweight', True)."""
    text = (s or "").strip()
    title = "Title" in text
    for wc in _WEIGHT_CLASSES:
        if wc in text:
            return wc, title
    return None, title


def parse_method(s: str | None) -> tuple[str | None, str | None]:
    """Normalize Greco method strings to the short codes used everywhere."""
    text = (s or "").strip()
    if not text:
        return None, None
    return _METHOD_MAP.get(text, (text, None))


def parse_outcome(s: str | None) -> str | None:
    """'W/L' -> 'fighter1' (first-listed won), 'L/W' -> 'fighter2', etc."""
    return _OUTCOME_MAP.get((s or "").strip())


def parse_bout(s: str) -> tuple[str, str] | None:
    """'Arnold Allen vs. Melquizael Costa' -> both names."""
    parts = s.strip().split(" vs. ")
    if len(parts) != 2:
        return None
    return parts[0].strip(), parts[1].strip()


def normalize_name(s: str) -> str:
    """Accent/order/case-insensitive key for matching names across sources.

    'Weili Zhang' and 'Zhang Weili' must collide, as must 'José Aldo' and
    'Jose Aldo' — so: strip accents, lowercase, split into tokens, sort.
    """
    decomposed = unicodedata.normalize("NFKD", s)
    ascii_only = "".join(c for c in decomposed if not unicodedata.combining(c))
    tokens = re.findall(r"[a-z]+", ascii_only.lower())
    return " ".join(sorted(tokens))

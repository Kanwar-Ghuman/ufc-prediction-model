"""Polite, cached HTTP fetching for ufcstats.com.

Two rules, both non-negotiable:
1. Rate limit: at most ~1 request/second (configurable). We are guests.
2. Cache everything: every fetched page is written to data/raw/html/ so
   re-parsing NEVER re-scrapes. Parsing bugs are fixed against the cache.

Cache layout: <cache_dir>/<sha1(url)>.html plus a human-readable index at
<cache_dir>/cache_index.tsv mapping hash -> url -> fetch timestamp.
"""

import hashlib
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

USER_AGENT = "octagon-oracle/0.1 (educational ML project; polite scraper)"

_last_request_time = 0.0


class BotChallengeError(RuntimeError):
    """The site served an anti-bot challenge instead of content.

    As of mid-2026 ufcstats.com sits behind a JavaScript proof-of-work
    bot check. We do NOT try to bypass it — that's their call to make.
    Use the published Greco1899/scrape_ufc_stats CSVs as the data refresh
    path instead (see README).
    """


def _looks_like_challenge(html: str) -> bool:
    """Heuristic for anti-bot interstitials rather than real content."""
    head = html[:2000].lower()
    return "checking your browser" in head or "this site requires javascript" in head


def _cache_path(cache_dir: Path, url: str) -> Path:
    return cache_dir / (hashlib.sha1(url.encode()).hexdigest() + ".html")


def fetch(
    url: str,
    cache_dir: Path,
    rate_limit_seconds: float = 1.0,
    timeout_seconds: float = 30.0,
    force: bool = False,
) -> str:
    """Return the page HTML, from cache when available.

    `force=True` re-downloads (e.g. to refresh an upcoming-event page whose
    card changed) — the cache file is overwritten, never duplicated.
    """
    global _last_request_time
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = _cache_path(cache_dir, url)

    if path.exists() and not force:
        return path.read_text(encoding="utf-8")

    # Sleep off whatever remains of the rate-limit window before hitting the site.
    elapsed = time.monotonic() - _last_request_time
    if elapsed < rate_limit_seconds:
        time.sleep(rate_limit_seconds - elapsed)

    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout_seconds)
    _last_request_time = time.monotonic()
    resp.raise_for_status()

    # Never cache a challenge page — it would silently poison every re-parse.
    if _looks_like_challenge(resp.text):
        raise BotChallengeError(f"Anti-bot challenge served for {url}")

    path.write_text(resp.text, encoding="utf-8")
    with open(cache_dir / "cache_index.tsv", "a", encoding="utf-8") as fh:
        fh.write(f"{path.stem}\t{url}\t{datetime.now(timezone.utc).isoformat()}\n")
    return resp.text

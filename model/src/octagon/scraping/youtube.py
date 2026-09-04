"""YouTube preview-video search + comment lean for `octagon fetch-context`.

Needs YOUTUBE_API_KEY. search.list is 100 quota units per bout.
"""

from __future__ import annotations

import html
import re
from typing import Any
from urllib.parse import urlencode

import requests

from octagon.db.parsing import normalize_name
from octagon.scraping.fighters import _same_person, _tokens
from octagon.scraping.wikipedia import USER_AGENT

YT_SEARCH = "https://www.googleapis.com/youtube/v3/search"
YT_COMMENTS = "https://www.googleapis.com/youtube/v3/commentThreads"

# Title/comment phrases that look like an explicit pick. `<<NAME>>` is filled
# with the fighter's surname at match time (not str.format — regex quantifiers
# like {0,40} would collide with format fields).
PICK_PATTERNS = [
    (r"\b(?:pick|picks?|taking|leaning|locking in|going with|"
     r"betting on|money on|side with)\b.{0,40}?\b<<NAME>>\b", re.I | re.S),
    (r"\b<<NAME>>\b.{0,20}?\b(?:by\s+(?:ko|tko|sub|decision|"
     r"ud|sd)|wins?|finishes|destroys|smokes)\b", re.I),
]


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def search_preview_videos(api_key: str, f1: str, f2: str, event: str | None,
                          max_results: int = 4,
                          session: requests.Session | None = None) -> list[dict]:
    """Find recent preview / picks videos for one bout."""
    session = session or _session()
    query = f"{f1} vs {f2} UFC preview picks"
    if event:
        # Keep the event name short so it doesn't drown the fighter query.
        short = re.sub(r"^UFC\s+(Fight Night:\s*)?", "", event, flags=re.I)
        query = f"{f1} vs {f2} {short} UFC"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "order": "relevance",
        "relevanceLanguage": "en",
        "safeSearch": "none",
        "key": api_key,
    }
    try:
        resp = session.get(f"{YT_SEARCH}?{urlencode(params)}", timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return []

    videos = []
    for item in data.get("items", []):
        vid = (item.get("id") or {}).get("videoId")
        snip = item.get("snippet") or {}
        if not vid:
            continue
        videos.append({
            "video_id": vid,
            "title": html.unescape(snip.get("title") or ""),
            "channel": html.unescape(snip.get("channelTitle") or ""),
            "published_at": snip.get("publishedAt") or "",
            "url": f"https://www.youtube.com/watch?v={vid}",
        })
    return videos


def top_comments(api_key: str, video_id: str, max_results: int = 25,
                 session: requests.Session | None = None) -> list[str]:
    """Top-level comment texts for a video (relevance order)."""
    session = session or _session()
    params = {
        "part": "snippet",
        "videoId": video_id,
        "maxResults": max_results,
        "order": "relevance",
        "textFormat": "plainText",
        "key": api_key,
    }
    try:
        resp = session.get(f"{YT_COMMENTS}?{urlencode(params)}", timeout=30)
        # Comments disabled → 403; treat as empty, not a hard failure.
        if resp.status_code in (403, 404):
            return []
        resp.raise_for_status()
        data = resp.json()
    except (requests.RequestException, ValueError):
        return []

    texts = []
    for item in data.get("items", []):
        try:
            text = (item["snippet"]["topLevelComment"]["snippet"]
                    ["textDisplay"])
        except (KeyError, TypeError):
            continue
        if text:
            texts.append(text)
    return texts


def _name_hits(text: str, name: str) -> int:
    """How many times this fighter is clearly referenced in `text`."""
    tokens = _tokens(name)
    if not tokens:
        return 0
    # Surname alone is enough in a bout-scoped comment ("Medic by KO").
    surname = re.escape(tokens[-1])
    return len(re.findall(rf"\b{surname}\b", text, flags=re.I))


def _explicit_pick(text: str, f1: str, f2: str) -> str | None:
    """Return 'f1' / 'f2' if the text looks like an explicit pick, else None."""
    for fighter, label in ((f1, "f1"), (f2, "f2")):
        surname = re.escape(_tokens(fighter)[-1]) if _tokens(fighter) else ""
        if not surname:
            continue
        for template, flags in PICK_PATTERNS:
            if re.search(template.replace("<<NAME>>", surname), text, flags):
                return label
    return None


def score_bout_buzz(f1: str, f2: str, videos: list[dict],
                    comments_by_video: dict[str, list[str]]) -> dict[str, Any]:
    """Turn titles + comments into a lean toward fighter1 in [-1, 1].

    lean > 0 means the YouTube crowd prefers f1. `n_signals` is how many
    title/comment hits contributed — used downstream as a confidence gate.
    """
    f1_score = f2_score = 0.0
    n_signals = 0
    title_picks: list[str] = []

    for video in videos:
        title = video.get("title") or ""
        pick = _explicit_pick(title, f1, f2)
        if pick == "f1":
            f1_score += 2.0
            n_signals += 1
            title_picks.append(f"title→{f1}: {title[:80]}")
        elif pick == "f2":
            f2_score += 2.0
            n_signals += 1
            title_picks.append(f"title→{f2}: {title[:80]}")
        else:
            h1, h2 = _name_hits(title, f1), _name_hits(title, f2)
            # Titles almost always name both; only count a lean if one dominates.
            if h1 > h2:
                f1_score += 0.5
                n_signals += 1
            elif h2 > h1:
                f2_score += 0.5
                n_signals += 1

        for comment in comments_by_video.get(video["video_id"], []):
            pick = _explicit_pick(comment, f1, f2)
            if pick == "f1":
                f1_score += 1.0
                n_signals += 1
            elif pick == "f2":
                f2_score += 1.0
                n_signals += 1
            else:
                h1, h2 = _name_hits(comment, f1), _name_hits(comment, f2)
                if h1 == 0 and h2 == 0:
                    continue
                if h1 > h2:
                    f1_score += 0.4
                    n_signals += 1
                elif h2 > h1:
                    f2_score += 0.4
                    n_signals += 1

    total = f1_score + f2_score
    lean = 0.0 if total == 0 else (f1_score - f2_score) / total
    return {
        "lean_f1": round(lean, 3),          # -1 (all f2) .. +1 (all f1)
        "f1_score": round(f1_score, 2),
        "f2_score": round(f2_score, 2),
        "n_signals": n_signals,
        "n_videos": len(videos),
        "n_comments": sum(len(v) for v in comments_by_video.values()),
        "title_picks": title_picks[:6],
        "preferred": (f1 if lean > 0.15 else f2 if lean < -0.15 else None),
    }


def fetch_bout_youtube(api_key: str, f1: str, f2: str, event: str | None,
                       max_videos: int = 4, max_comments: int = 25,
                       session: requests.Session | None = None) -> dict:
    """Full fetch for one bout: videos + comments + scored lean."""
    session = session or _session()
    videos = search_preview_videos(api_key, f1, f2, event, max_videos, session)
    comments_by_video = {}
    for video in videos:
        comments_by_video[video["video_id"]] = top_comments(
            api_key, video["video_id"], max_comments, session)
    buzz = score_bout_buzz(f1, f2, videos, comments_by_video)
    return {
        "fighter1": f1,
        "fighter2": f2,
        "videos": videos,
        **buzz,
    }


def fetch_card_youtube(api_key: str, fights: list[dict], event: str | None,
                       max_videos: int = 4, max_comments: int = 25) -> list[dict]:
    """Fetch YouTube buzz for every bout on a card."""
    session = _session()
    out = []
    for fight in fights:
        out.append(fetch_bout_youtube(
            api_key, fight["fighter1"], fight["fighter2"], event,
            max_videos=max_videos, max_comments=max_comments, session=session))
    return out


def agreement_note(model_p_f1: float, youtube_lean: float | None,
                   n_signals: int, f1: str, f2: str,
                   min_signals: int = 4) -> str | None:
    """One-line comparison of model pick vs YouTube lean, or None if thin."""
    if youtube_lean is None or n_signals < min_signals:
        return None
    model_pick = f1 if model_p_f1 >= 0.5 else f2
    yt_pick = f1 if youtube_lean > 0.15 else f2 if youtube_lean < -0.15 else None
    if yt_pick is None:
        return (f"YouTube buzz mixed (lean={youtube_lean:+.2f}, "
                f"n={n_signals}) — no crowd call")
    if _same_person(model_pick, yt_pick) or normalize_name(model_pick) == normalize_name(yt_pick):
        return (f"YouTube agrees with {model_pick} "
                f"(lean={youtube_lean:+.2f}, n={n_signals})")
    return (f"YouTube disagrees: crowd → {yt_pick}, model → {model_pick} "
            f"(lean={youtube_lean:+.2f}, n={n_signals})")

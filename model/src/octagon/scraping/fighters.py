"""Fighter portraits, records, flags. `octagon fetch-media`.

Order: ufc.com/athlete (robots.txt crawl-delay 15), then Wikipedia/Wikidata,
then Sherdog for debutants with no UFC page. Name-guarded: a page only
counts if its own name matches the query.
"""

import json
import re
import time
import unicodedata
from datetime import date
from functools import lru_cache
from pathlib import Path

import requests

from octagon.db.parsing import normalize_name

UFC_ATHLETE = "https://www.ufc.com/athlete/"
SHERDOG_HOST = "https://www.sherdog.com"
WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
WIKIDATA_API = "https://www.wikidata.org/w/api.php"
COMMONS_FILE = "https://commons.wikimedia.org/wiki/File:"

# ufc.com serves the roster pages only to browser-shaped clients; the
# educational purpose and contact are in the comment header of this file
# rather than a spoofed identity we can't back up.
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36")
WIKI_UA = "octagon-oracle/0.1 (educational UFC prediction project)"

BATCH = 50          # the API caps titles=/ids= at 50 for anonymous clients
THUMB_PX = 640
WIKI_SEARCH_DELAY = 1.0   # title searches can't be batched; don't machine-gun them

# Regex for Wikipedia record / title extraction.
RECORD_PATTERN = re.compile(
    r"(?P<w>\d+)\s*[-–]\s*(?P<l>\d+)(?:\s*[-–]\s*(?P<d>\d+))?"
)
AMATEUR_RECORD_PATTERN = re.compile(
    r"amateur\s+(?:record|mixed martial arts?)\s+(?:of\s+)?(?P<record>\d+[-–]\d+(?:[-–]\d+)?)",
    re.IGNORECASE
)
TITLE_PATTERN = re.compile(
    r"(?P<org>Bellator|PRIDE|ONE Championship|Strikeforce|Dream|Rings|WAMMA|CW.*?)\s+"
    r"(?:champion|title|belt|heavyweight|light heavyweight|middleweight|welterweight|"
    r"lightweight|featherweight|bantamweight|flyweight|women)",
    re.IGNORECASE
)

CACHE_PATH = "data/fighter_media.json"
IMAGE_DIR = "data/fighter_images"

# Letters NFKD refuses to decompose, but which every slug generator folds.
FOLD = str.maketrans({"ł": "l", "Ł": "l", "ø": "o", "Ø": "o", "đ": "d",
                      "Đ": "d", "ð": "d", "þ": "th", "ß": "ss", "æ": "ae",
                      "Æ": "ae", "œ": "oe", "Œ": "oe", "ı": "i"})


def slug(name: str) -> str:
    """'Uroš Medić' -> 'uros-medic', the shape ufc.com uses for its URLs."""
    folded = unicodedata.normalize("NFKD", name.translate(FOLD))
    ascii_only = "".join(c for c in folded if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", "-", ascii_only.lower()).strip("-")


def _tokens(name: str) -> list[str]:
    folded = unicodedata.normalize("NFKD", name.translate(FOLD))
    ascii_only = "".join(c for c in folded if not unicodedata.combining(c))
    return re.findall(r"[a-z]+", ascii_only.lower())


def _same_person(found: str, asked: str) -> bool:
    """Is the page we landed on about the fighter we asked for?

    Exact match after folding accents and word order, or one name carrying a
    middle name the other doesn't ('Nina Nikolija Milošević' on the card,
    'Nina Milosevic' on the roster) — with the surname still required to
    agree, so a shared first name alone can't pass.
    """
    a, b = _tokens(found), _tokens(asked)
    if not a or not b:
        return False
    if sorted(a) == sorted(b):
        return True
    return a[-1] == b[-1] and (set(a) <= set(b) or set(b) <= set(a))


def _blank(name: str) -> dict:
    """A cached miss. Same shape as a hit, so consumers never branch on None."""
    return {"name": name, "key": normalize_name(name), "ufc_name": None,
            "nickname": None, "record": None, "rank": None, "division": None,
            "status": None, "birthplace": None, "country": None,
            "country_code": None, "profile": None, "image": None,
            "image_full": None, "image_source": None, "image_credit": None,
            "headshot": None, "portrait": None, "wiki_page": None,
            "description": None, "fetched": date.today().isoformat()}


# --------------------------------------------------------------------------
# ufc.com — the official roster page
# --------------------------------------------------------------------------

# ufc.com answers "no photo shoot yet" with a black silhouette rather than a
# 404. Passing that through would put a featureless shadow next to real
# portraits; the initials fallback reads as missing, which is the truth.
PLACEHOLDER_IMAGES = ("silhouette", "shadow_fighter", "default_")


def _real_photo(url: str | None) -> str | None:
    if not url or any(mark in url.lower() for mark in PLACEHOLDER_IMAGES):
        return None
    return url


def _text(soup, selector: str) -> str | None:
    node = soup.select_one(selector)
    return " ".join(node.get_text(" ", strip=True).split()) if node else None


def slug_candidates(name: str) -> list[str]:
    """URL slugs worth trying for a fighter, most likely first.

    Card sources carry the full legal name ('Nina Nikolija Milošević') where
    ufc.com lists the fighting name ('Nina Milosevic'), so a middle name is
    the one systematic difference worth a second request.
    """
    parts = name.split()
    candidates = [slug(name)]
    if len(parts) > 2:
        candidates.append(slug(f"{parts[0]} {parts[-1]}"))
    return list(dict.fromkeys(c for c in candidates if c))


def ufc_profile(name: str, session: requests.Session,
                retry_pause: float = 2.0) -> dict | None:
    """Scrape one athlete page, or None if it doesn't exist / isn't them."""
    from bs4 import BeautifulSoup

    resp = None
    for i, candidate in enumerate(slug_candidates(name)):
        if i:
            time.sleep(retry_pause)
        url = UFC_ATHLETE + candidate
        try:
            # A slug that doesn't exist 302s to the search page; don't follow
            # it and then try to parse a result list as a person.
            attempt = session.get(url, timeout=30, allow_redirects=False)
        except requests.RequestException:
            return None
        if attempt.status_code == 200:
            resp = attempt
            break
    if resp is None:
        return None

    soup = BeautifulSoup(resp.text, "lxml")
    found = _text(soup, ".hero-profile__name")
    if not found or not _same_person(found, name):
        return None

    # "#4 Light Heavyweight Division" / "Heavyweight Division" / "Active"
    rank, division = None, _text(soup, ".hero-profile__division-title")
    for tag in soup.select(".hero-profile__tag"):
        label = " ".join(tag.get_text(" ", strip=True).split())
        match = re.match(r"#(\d+)\s+(.*)", label)
        if match:
            rank, division = match.group(1), match.group(2)

    fields = {}
    for field in soup.select(".c-bio__field"):
        label = _text(field, ".c-bio__label")
        value = _text(field, ".c-bio__text")
        if label and value:
            fields[label.lower()] = value

    # Two official images: og:image is the head-and-shoulders cut-out, and
    # the bio page also carries the standing full-body one the fight cards
    # use. The site wants the tall one and falls back to the head shot.
    headshot = soup.select_one('meta[property="og:image"]')
    full_body = re.search(r'https://[^"\']*athlete_bio_full_body[^"\']*\.(?:png|jpg)',
                          resp.text)
    headshot_url = headshot["content"] if headshot and headshot.get("content") else None
    full_body_url = full_body.group(0) if full_body else None
    record = _text(soup, ".hero-profile__division-body") or ""
    birthplace = fields.get("place of birth")
    return {
        "ufc_name": found,
        "nickname": (_text(soup, ".hero-profile__nickname") or "").strip('"') or None,
        "record": record.replace("(W-L-D)", "").strip() or None,
        "rank": rank,
        "division": (division or "").replace(" Division", "").strip() or None,
        "status": fields.get("status"),
        "birthplace": birthplace,
        "country": birthplace.split(",")[-1].strip() if birthplace else None,
        "profile": url,
        "image": _real_photo(headshot_url),
        "image_full": _real_photo(full_body_url),
        "image_source": "ufc.com",
        "image_credit": url,
    }


# --------------------------------------------------------------------------
# Wikipedia + Wikidata — flags, descriptions, backup photos
# --------------------------------------------------------------------------

def _wiki_get(url: str, params: dict, attempts: int = 4) -> dict:
    """A Wikimedia API call that backs off instead of falling over.

    Batched lookups are one request each, but the per-miss title searches
    fire in a row and the anonymous rate limit notices. A 429 here is a
    "slow down", not an error — so wait the interval it asks for (or an
    exponentially growing one) rather than losing a five-minute crawl.
    """
    for attempt in range(attempts):
        resp = requests.get(url, params={**params, "format": "json",
                                         "formatversion": 2},
                            headers={"User-Agent": WIKI_UA}, timeout=30)
        if resp.status_code in (429, 503) and attempt < attempts - 1:
            wait = float(resp.headers.get("Retry-After") or 2 ** attempt)
            time.sleep(min(wait, 30.0))
            continue
        resp.raise_for_status()
        return resp.json()
    return {}


def _chunks(items: list, size: int = BATCH):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def _search_title(name: str) -> str | None:
    """Find an article for a name whose exact title didn't resolve.

    Only an exact normalized match counts — this recovers accent cases
    ('Uros Medic' -> 'Uroš Medić') without inventing a biography for a
    debutant who has no article at all.
    """
    data = _wiki_get(WIKIPEDIA_API, {"action": "query", "list": "search",
                                     "srlimit": 5,
                                     "srsearch": f"{name} mixed martial artist"})
    for hit in data.get("query", {}).get("search", []):
        if _same_person(hit["title"], name):
            return hit["title"]
    return None


def _pages(titles: list[str]) -> dict[str, dict]:
    """Wikipedia pages for these titles, keyed by the title we asked for.

    `redirects=1` collapses alternate spellings onto the real article, so a
    response can come back under a different title than the request — the
    `normalized`/`redirects` hops map it back.
    """
    found: dict[str, dict] = {}
    for chunk in _chunks(titles):
        query = _wiki_get(WIKIPEDIA_API, {
            "action": "query", "titles": "|".join(chunk), "redirects": 1,
            "prop": "pageimages|pageprops", "piprop": "thumbnail",
            "pithumbsize": THUMB_PX,
        }).get("query", {})
        alias = {hop["from"]: hop["to"] for step in ("normalized", "redirects")
                 for hop in query.get(step, [])}
        by_title = {p["title"]: p for p in query.get("pages", [])
                    if not p.get("missing")}
        for asked in chunk:
            resolved = asked
            for _ in range(3):        # normalized, then redirected, at most
                resolved = alias.get(resolved, resolved)
            if resolved in by_title:
                found[asked] = by_title[resolved]
    return found


def _entities(qids: list[str], props: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for chunk in _chunks(sorted(set(qids))):
        data = _wiki_get(WIKIDATA_API, {"action": "wbgetentities",
                                        "ids": "|".join(chunk), "props": props,
                                        "languages": "en"})
        out.update(data.get("entities", {}))
    return out


def _claim_ids(entity: dict, prop: str) -> list[str]:
    """Values of a Wikidata item-valued claim, preferred rank first."""
    claims = entity.get("claims", {}).get(prop, [])
    ordered = sorted(claims, key=lambda c: c.get("rank") != "preferred")
    values = [c.get("mainsnak", {}).get("datavalue", {}).get("value")
              for c in ordered]
    return [v["id"] for v in values if isinstance(v, dict) and v.get("id")]


def _iso_codes(entity: dict) -> list[str]:
    """ISO 3166-1 codes, falling back to 3166-2 for the home nations.

    Wales, Scotland and England have no alpha-2 of their own but plenty of
    fighters, and 'GB-WLS' is enough for the site to draw the right flag.
    """
    for prop in ("P297", "P300"):
        codes = [c["mainsnak"]["datavalue"]["value"]
                 for c in entity.get("claims", {}).get(prop, [])
                 if c.get("mainsnak", {}).get("datavalue")]
        if codes:
            return codes
    return []


def _country_codes(qids: list[str]) -> dict[str, dict]:
    """Country item -> {country label, ISO code for the flag}."""
    out = {}
    for qid, entity in _entities(qids, "claims|labels").items():
        iso = _iso_codes(entity)
        out[qid] = {"country": entity.get("labels", {}).get("en", {}).get("value"),
                    "country_code": iso[0] if iso else None}
    return out


@lru_cache(maxsize=256)
def iso_for_country(name: str) -> str | None:
    """ISO code for a country ufc.com named but Wikidata didn't confirm.

    One search per country rather than a hand-maintained table of the sixty
    nations on the UFC roster — and the answers are cached, so the whole
    site costs a handful of these ever.
    """
    data = _wiki_get(WIKIDATA_API, {"action": "wbsearchentities", "search": name,
                                    "language": "en", "type": "item", "limit": 5})
    for hit in data.get("search", []):
        codes = _country_codes([hit["id"]]).get(hit["id"], {})
        if codes.get("country_code"):
            return codes["country_code"]
    return None


def _page_html(title: str) -> str:
    """Fetch full page HTML for text extraction (amateur record, titles)."""
    try:
        resp = requests.get(
            WIKIPEDIA_API,
            params={
                "action": "query",
                "titles": title,
                "prop": "extracts",
                "exintro": 0,
                "explaintext": 1,
                "redirects": 1,
                "format": "json",
                "formatversion": 2,
            },
            headers={"User-Agent": WIKI_UA},
            timeout=30
        )
        resp.raise_for_status()
        pages = resp.json().get("query", {}).get("pages", [])
        if pages and not pages[0].get("missing"):
            return pages[0].get("extract", "")
    except requests.RequestException:
        pass
    return ""


def _extract_amateur_record(text: str) -> dict | None:
    """Extract amateur W-L-D record from Wikipedia text."""
    match = AMATEUR_RECORD_PATTERN.search(text)
    if match:
        record_str = match.group("record")
        parts = re.split(r"[-–]", record_str)
        if len(parts) >= 2:
            try:
                wins, losses = int(parts[0]), int(parts[1])
                d = int(parts[2]) if len(parts) > 2 else 0
                if wins + losses + d >= 3:
                    return {"wins": wins, "losses": losses, "draws": d}
            except ValueError:
                pass
    return None


def _extract_other_org_titles(text: str) -> list[str]:
    """Extract championship titles from other organizations."""
    titles = []
    for match in TITLE_PATTERN.finditer(text):
        org = match.group("org")
        if org and org not in [t.split(":")[0] for t in titles]:
            titles.append(f"{org} champion")
    return titles[:5]  # limit to 5 titles


def wiki_records(names: list[str]) -> dict[str, dict]:
    """Article link, description, backup photo, citizenship, amateur record, and titles."""
    pages = _pages(names)
    for name in names:                      # second chance for the misses
        if name in pages:
            continue
        time.sleep(WIKI_SEARCH_DELAY)       # searches are not batchable
        title = _search_title(name)
        if title and title in (hit := _pages([title])):
            pages[name] = hit[title]

    qid_of = {name: page.get("pageprops", {}).get("wikibase_item")
              for name, page in pages.items()}
    people = _entities([q for q in qid_of.values() if q], "claims")
    country_of = {qid: (_claim_ids(entity, "P27") or [None])[0]
                  for qid, entity in people.items()}
    codes = _country_codes([c for c in country_of.values() if c])

    # Amateur record / titles from the full Wikipedia page.
    full_text_cache = {}
    for name, page in pages.items():
        if "title" in page:
            full_text_cache[name] = _page_html(page["title"])

    out = {}
    for name, page in pages.items():
        file_name = page.get("pageprops", {}).get("page_image_free")
        full_text = full_text_cache.get(name, "")
        out[name] = {
            "wiki_page": "https://en.wikipedia.org/wiki/"
                         + page["title"].replace(" ", "_"),
            "description": page.get("pageprops", {}).get("wikibase-shortdesc"),
            "wiki_image": page.get("thumbnail", {}).get("source"),
            "wiki_image_credit": (COMMONS_FILE + file_name.replace(" ", "_")
                                  if file_name else None),
            "amateur_record": _extract_amateur_record(full_text),
            "other_org_titles": _extract_other_org_titles(full_text),
            **codes.get(country_of.get(qid_of.get(name) or "") or "", {}),
        }
    return out


# --------------------------------------------------------------------------
# Sherdog — backup portraits for debutants with no ufc.com page
# --------------------------------------------------------------------------

def _absolute_url(src: str, base: str) -> str:
    if src.startswith("//"):
        return "https:" + src
    if src.startswith("/"):
        return base.rstrip("/") + src
    return src


def _larger_sherdog_crop(url: str) -> str:
    """Ask for a 400x600 crop instead of the 200x300 thumbnail on the page."""
    return re.sub(r"/image_crop/\d+/\d+/", "/image_crop/400/600/", url)


def sherdog_photo_from_html(html: str, name: str, page_url: str) -> dict | None:
    """Portrait URL from a Sherdog fighter page, or None if it isn't them."""
    from bs4 import BeautifulSoup

    img = BeautifulSoup(html, "lxml").select_one("img.profile-image.photo")
    if img is None:
        return None
    alt = (img.get("alt") or "").strip()
    if not alt or not _same_person(alt, name):
        return None
    src = img.get("src") or img.get("data-src")
    if not src:
        return None
    url = _real_photo(_larger_sherdog_crop(_absolute_url(src, SHERDOG_HOST)))
    if not url:
        return None
    return {"image": url, "image_source": "sherdog", "image_credit": page_url}


def _sherdog_index() -> dict[str, dict]:
    """Already-resolved fighter URLs from `octagon fetch-sherdog`. No network."""
    from octagon.config import load_config, resolve_path
    from octagon.scraping import sherdog

    return sherdog.load_cache(resolve_path(load_config()["data"]["sherdog_cache"]))


def _sherdog_photo(name: str, fighter_url: str,
                   session: requests.Session) -> dict | None:
    try:
        resp = session.get(fighter_url, timeout=30)
        resp.raise_for_status()
    except requests.RequestException:
        return None
    return sherdog_photo_from_html(resp.text, name, fighter_url)


# --------------------------------------------------------------------------
# Portrait files
# --------------------------------------------------------------------------

def _image_headers(url: str) -> dict[str, str]:
    """CDNs gate on Referer; send the host the bytes actually live on."""
    host = ("https://www.sherdog.com/" if "sherdog.com" in url.lower()
            else "https://www.ufc.com/")
    return {"User-Agent": BROWSER_UA, "Referer": host}


def download_image(url: str | None, name: str, image_dir: Path) -> str | None:
    """Copy one image next to the rest of the data; return its file name.

    Serving these ourselves keeps the site working offline and keeps us off
    someone else's CDN on every page view.
    """
    if not url:
        return None
    file_name = name + (".png" if ".png" in url.lower() else ".jpg")
    path = image_dir / file_name
    if path.exists():
        return file_name
    try:
        resp = requests.get(url, timeout=30, headers=_image_headers(url))
        resp.raise_for_status()
    except requests.RequestException:
        return None
    image_dir.mkdir(parents=True, exist_ok=True)
    path.write_bytes(resp.content)
    return file_name


def download_portraits(record: dict, image_dir: Path) -> dict[str, str | None]:
    """Local copies of both official images, keyed as the record stores them."""
    stem = slug(record["name"])
    return {"portrait": download_image(record.get("image_full"), stem, image_dir),
            "headshot": download_image(record.get("image"), stem + "-head",
                                       image_dir)}


# --------------------------------------------------------------------------
# Orchestration + cache
# --------------------------------------------------------------------------

def fetch(names: list[str], image_dir: Path, delay: float = 15.0,
          on_progress=None) -> dict[str, dict]:
    """Everything known about these fighters. All network access is here."""
    unique = sorted({n.strip() for n in names if n and n.strip()})
    # Wikipedia supplies flags and descriptions; ufc.com supplies everything
    # the page can't do without. Losing the former to a rate limit or an
    # outage should cost a flag, not the whole crawl.
    try:
        wiki = wiki_records(unique)
    except requests.RequestException as exc:
        print(f"  (Wikipedia lookup failed: {exc} — continuing without flags)")
        wiki = {}

    session = requests.Session()
    session.headers.update({"User-Agent": BROWSER_UA})
    sherdog_pages = _sherdog_index()

    media = {}
    for i, name in enumerate(unique):
        if i:
            time.sleep(delay)           # ufc.com robots.txt: crawl-delay 15
        record = _blank(name)
        record.update({k: v for k, v in wiki.get(name, {}).items()
                       if k in ("wiki_page", "description", "country",
                                "country_code")})
        profile = ufc_profile(name, session)
        if profile:
            record.update({k: v for k, v in profile.items() if v is not None})
        # Wikipedia's photo is the fallback whenever ufc.com left us without
        # one — which includes roster pages that exist but carry no portrait,
        # not just the fighters who have no page at all.
        if not record["image"] and wiki.get(name, {}).get("wiki_image"):
            record.update({"image": wiki[name]["wiki_image"],
                           "image_source": "wikipedia",
                           "image_credit": wiki[name]["wiki_image_credit"]})
        # Contender Series debutants: Sherdog usually has the face ufc.com
        # doesn't. Only a URL we already resolved for records is eligible.
        if not record["image"]:
            fighter_url = (sherdog_pages.get(normalize_name(name)) or {}).get(
                "sherdog_url")
            photo = (_sherdog_photo(name, fighter_url, session)
                     if fighter_url else None)
            if photo:
                record.update(photo)
                if not record.get("profile"):
                    record["profile"] = fighter_url

        # ufc.com's place of birth wins over Wikidata citizenship (it is
        # what UFC itself puts under the flag), but the ISO code the flag
        # needs still has to come from Wikidata.
        if profile and profile.get("country") and not _same_country(
                profile["country"], wiki.get(name, {}).get("country")):
            try:
                record["country_code"] = iso_for_country(profile["country"])
            except requests.RequestException:
                record["country_code"] = None

        record.update(download_portraits(record, image_dir))
        media[name] = record
        if on_progress:
            on_progress(record)
    return media


def _same_country(a: str | None, b: str | None) -> bool:
    return bool(a and b and a.strip().lower() == b.strip().lower())


def load_cache(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_cache(path: Path, cache: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, indent=1, ensure_ascii=False,
                               sort_keys=True), encoding="utf-8")


def refresh(names: list[str], path: Path, image_dir: Path, delay: float = 15.0,
            force: bool = False, on_progress=None) -> dict[str, dict]:
    """Top up the cache for these fighters and return their records.

    Keyed by the normalized name, so a card spelling drifting from ufcstats'
    ('Benoit' vs 'Benoît') costs neither a second lookup nor a second face.
    """
    cache = load_cache(path)
    wanted = {normalize_name(n): n for n in names if n and n.strip()}
    missing = [name for key, name in wanted.items() if force or key not in cache]
    for name, record in fetch(missing, image_dir, delay, on_progress).items():
        cache[normalize_name(name)] = record
        save_cache(path, cache)         # checkpoint: a 15s crawl gets interrupted
    return {name: cache.get(key, _blank(name)) for key, name in wanted.items()}


def lookup(names: list[str], path: Path) -> dict[str, dict]:
    """Read-only view of the cache — no network, for predict and the API."""
    cache = load_cache(path)
    return {name: cache.get(normalize_name(name), _blank(name))
            for name in names if name}

"""Media lookup must not attach the wrong fighter."""

import json

import pytest

from octagon.scraping import fighters


@pytest.mark.parametrize("name, expected", [
    ("Uroš Medić", "uros-medic"),          # accents fold to ufc.com's slug
    ("Jan Błachowicz", "jan-blachowicz"),  # ł does not NFKD-decompose
    ("Ľudovít Klein", "ludovit-klein"),
    ("Benoît Saint Denis", "benoit-saint-denis"),
    ("Jéssica Andrade", "jessica-andrade"),
])
def test_slug_matches_the_url_ufc_uses(name, expected):
    assert fighters.slug(name) == expected


def test_middle_names_get_a_second_slug_to_try():
    """Cards carry the legal name, ufc.com lists the fighting name."""
    assert fighters.slug_candidates("Nina Nikolija Milošević") == [
        "nina-nikolija-milosevic", "nina-milosevic"]
    assert fighters.slug_candidates("Hailey Cowan") == ["hailey-cowan"]


@pytest.mark.parametrize("found, asked", [
    ("Uroš Medić", "Uros Medic"),                    # accents only
    ("Zhang Weili", "Weili Zhang"),                  # word order
    ("Nina Milosevic", "Nina Nikolija Milošević"),   # dropped middle name
])
def test_accepts_the_same_person_spelled_differently(found, asked):
    assert fighters._same_person(found, asked)


@pytest.mark.parametrize("found, asked", [
    ("Cody Gibson", "Abdul Hussein"),      # what Wikipedia's search returns
    ("Search results", "Robert Valentin"), # what a dead ufc.com slug returns
    ("Michael Johnson", "Michael Page"),   # shared first name only
    ("", "Jan Błachowicz"),
])
def test_rejects_a_different_person(found, asked):
    """A monogram is better than confidently showing the wrong man."""
    assert not fighters._same_person(found, asked)


@pytest.mark.parametrize("url", [
    "https://ufc.com/images/styles/athlete_bio_full_body/s3/image/"
    "fighter_images/SHADOW_Fighter_fullLength_RED.png",
    "https://ufc.com/images/2019-04/SILHOUETTE.png?VersionId=abc",
])
def test_ufc_placeholder_silhouettes_count_as_no_photo(url):
    """A featureless shadow beside real portraits reads as a broken image."""
    assert fighters._real_photo(url) is None


def test_a_real_portrait_survives_the_placeholder_filter():
    url = "https://ufc.com/images/2025-12/BLACHOWICZ_JAN_12-06.png"
    assert fighters._real_photo(url) == url


def test_cache_is_keyed_so_spelling_drift_costs_no_second_lookup(tmp_path):
    """'Benoît' on the card and 'Benoit' in ufcstats are one fighter."""
    path = tmp_path / "media.json"
    record = {**fighters._blank("Benoît Saint Denis"), "record": "13-2-0"}
    fighters.save_cache(path, {fighters.normalize_name("Benoît Saint Denis"): record})

    found = fighters.lookup(["Benoit Saint Denis"], path)
    assert found["Benoit Saint Denis"]["record"] == "13-2-0"


def test_lookup_of_an_unknown_fighter_is_blank_not_missing(tmp_path):
    """Callers render a record either way; None would make every one branch."""
    blank = fighters.lookup(["Nobody At All"], tmp_path / "none.json")
    assert blank["Nobody At All"]["portrait"] is None
    assert blank["Nobody At All"]["name"] == "Nobody At All"


def test_saved_cache_is_readable_json(tmp_path):
    path = tmp_path / "media.json"
    fighters.save_cache(path, {"a b": fighters._blank("A B")})
    assert json.loads(path.read_text(encoding="utf-8"))["a b"]["name"] == "A B"


_SHERDOG_PROFILE = """
<html><body>
<img class="profile-image photo" itemprop="image" alt="Bella Mir"
     src="/image_crop/200/300/_images/fighter/20250727070809_Bella_Mir.JPG">
<img class="profile-image-mobile photo" alt="Bella Mir"
     src="/image_crop/200/300/_images/fighter/20250727070809_Bella_Mir.JPG">
</body></html>
"""


def test_sherdog_portrait_is_absolutized_and_upscaled():
    """Contender Series faces live on Sherdog, not ufc.com; hotlink the crop we host."""
    photo = fighters.sherdog_photo_from_html(
        _SHERDOG_PROFILE, "Bella Mir",
        "https://www.sherdog.com/fighter/Bella-Mir-376715")
    assert photo["image"] == (
        "https://www.sherdog.com/image_crop/400/600/_images/fighter/"
        "20250727070809_Bella_Mir.JPG")
    assert photo["image_source"] == "sherdog"
    assert photo["image_credit"].endswith("Bella-Mir-376715")


def test_sherdog_portrait_rejects_the_wrong_face():
    """Same name-guard as ufc.com: a teammate's thumbnail must not become the card photo."""
    html = _SHERDOG_PROFILE.replace('alt="Bella Mir"', 'alt="Alex Apodaca"', 1)
    assert fighters.sherdog_photo_from_html(
        html, "Bella Mir", "https://www.sherdog.com/fighter/Bella-Mir-376715") is None


def test_sherdog_portrait_rejects_missing_alt():
    """No alt means we cannot confirm the crop is this fighter."""
    html = _SHERDOG_PROFILE.replace('alt="Bella Mir"', "", 1)
    assert fighters.sherdog_photo_from_html(
        html, "Bella Mir", "https://www.sherdog.com/fighter/Bella-Mir-376715") is None


def test_sherdog_default_silhouette_counts_as_no_photo():
    html = """
    <img class="profile-image photo" alt="Somebody"
         src="/img/default_200x300.jpg">
    """
    assert fighters.sherdog_photo_from_html(
        html, "Somebody", "https://www.sherdog.com/fighter/Somebody-1") is None


def test_image_download_headers_match_the_host():
    """Sherdog's CDN 403s a ufc.com Referer; ufc.com wants one of its own."""
    assert "sherdog.com" in fighters._image_headers(
        "https://www.sherdog.com/image_crop/400/600/_images/fighter/x.JPG")["Referer"]
    assert "ufc.com" in fighters._image_headers(
        "https://ufc.com/images/2025-12/BLACHOWICZ_JAN.png")["Referer"]

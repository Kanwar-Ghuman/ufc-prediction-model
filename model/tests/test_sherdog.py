"""Sherdog regional-record lookup: finding the right fighter, or nobody.

Nothing here touches the network — the search response is stubbed. What is
worth testing is the name resolution, because a debutant whose Sherdog page
we fail to find is a fighter the model sees as having no career at all, and
one we match to the wrong page is worse than that.
"""

import pytest

from octagon.scraping import sherdog


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


class _FakeSession:
    """Records the query it was asked for, replies with fixed hits."""

    def __init__(self, hits):
        self._hits = hits
        self.queries = []

    def get(self, url, params=None, timeout=None):
        self.queries.append(params["q"])
        return _FakeResponse({"collection": self._hits})


def _hit(first, last, fighter_id):
    return {"source": "Fighter", "firstname": first, "lastname": last,
            "url": f"/fighter/{first}-{last}-{fighter_id}"}


def test_accents_are_folded_out_of_the_search_query():
    """Sherdog's fightfinder returns nothing for 'Błachowicz'."""
    session = _FakeSession([_hit("Jan", "Blachowicz", 25821)])
    sherdog._search_sherdog("Jan Błachowicz", session)
    assert session.queries == ["Jan Blachowicz"]


def test_alias_finds_the_fighter_sherdog_files_under_a_formal_name():
    """The UFC bills 'Vlasto Čepo'; Sherdog has him as 'Vlastislav Cepo'."""
    session = _FakeSession([_hit("Vlastislav", "Cepo", 330615)])
    url = sherdog._search_sherdog("Vlasto Čepo", session)
    assert session.queries == ["Vlastislav Cepo"]
    assert url == "https://www.sherdog.com/fighter/Vlastislav-Cepo-330615"


def _nick_hit(first, last, nickname, fighter_id):
    return {"source": "Fighter", "firstname": first, "lastname": last,
            "nickname": nickname,
            "url": f"/fighter/{first}-{last}-{fighter_id}"}


def test_a_ring_name_billed_as_a_surname_still_matches():
    """The UFC cards 'Jose Montanha'; Sherdog files 'Jose Luiz', nick 'Montanha'."""
    session = _FakeSession([_nick_hit("Jose", "Luiz", "Montanha", 398299)])
    url = sherdog._search_sherdog("Jose Montanha", session)
    assert url == "https://www.sherdog.com/fighter/Jose-Luiz-398299"


def test_the_full_legal_plus_ring_name_matches_too():
    """Wikipedia writes him out as 'Jose Luiz Montanha' — all three tokens."""
    session = _FakeSession([_nick_hit("Jose", "Luiz", "Montanha", 398299)])
    url = sherdog._search_sherdog("Jose Luiz Montanha", session)
    assert url == "https://www.sherdog.com/fighter/Jose-Luiz-398299"


def test_a_nickname_alone_is_not_enough_to_match():
    """Plenty of fighters are 'The Spider'; a bare nickname must not pair them."""
    session = _FakeSession([_nick_hit("Anderson", "Silva", "Spider", 1356)])
    assert sherdog._search_sherdog("Rodrigo Spider", session) is None


def test_a_shared_surname_alone_does_not_match():
    """Without the alias, 'Vlasto' and 'Vlastislav' must stay separate people."""
    session = _FakeSession([_hit("Vlastislav", "Cepo", 330615)])
    assert sherdog._search_sherdog("Marko Cepo", session) is None


@pytest.mark.parametrize("hits", [
    [],                                             # nobody by that name
    [{"source": "Event", "firstname": "", "lastname": ""}],  # non-fighter hit
])
def test_no_fighter_hit_is_a_miss_not_a_guess(hits):
    assert sherdog._search_sherdog("Bogdan Grad", _FakeSession(hits)) is None


EVENT_HTML = """
<html><body>
  <a href="/fighter/Uros-Medic-272505">Uros Medic</a>
  <a href="/fighter/Daniel-Rodriguez-145945">Daniel Rodriguez</a>
  <a href="/fighter/Vlastislav-Cepo-330615">Vlastislav Cepo</a>
  <a href="/events/UFC-Fight-Night-283-112723">the event itself</a>
</body></html>
"""


class _FakePageSession:
    def __init__(self, html):
        self._html = html

    def get(self, url, timeout=None):
        return type("R", (), {"text": self._html,
                              "raise_for_status": lambda self: None})()


def test_event_page_maps_fighters_to_their_own_pages():
    urls = sherdog.event_fighter_urls("http://e", _FakePageSession(EVENT_HTML))
    assert urls["medic uros"] == "https://www.sherdog.com/fighter/Uros-Medic-272505"
    assert urls["daniel rodriguez"] == \
        "https://www.sherdog.com/fighter/Daniel-Rodriguez-145945"
    assert "the event itself" not in str(urls)


def test_an_unreadable_event_page_falls_back_to_search_not_an_error():
    class _Dead:
        def get(self, url, timeout=None):
            raise sherdog.requests.RequestException("404")

    assert sherdog.event_fighter_urls("http://e", _Dead()) == {}


@pytest.mark.parametrize("cached_url, expected", [
    # The Daniel Rodriguez who lost once in 2003 is a different man.
    ("https://www.sherdog.com/fighter/Daniel-Rodriguez-34954", True),
    ("https://www.sherdog.com/fighter/Daniel-Rodriguez-145945", False),
])
def test_a_cached_record_the_event_page_contradicts_is_refetched(cached_url, expected):
    known = sherdog.event_fighter_urls("http://e", _FakePageSession(EVENT_HTML))
    record = {"sherdog_url": cached_url}
    assert sherdog._disagrees(record, known, "Daniel Rodriguez") is expected


def test_disagreement_check_understands_aliases():
    """Čepo is cached under the card's name but linked under Sherdog's."""
    known = sherdog.event_fighter_urls("http://e", _FakePageSession(EVENT_HTML))
    right = {"sherdog_url": "https://www.sherdog.com/fighter/Vlastislav-Cepo-330615"}
    assert sherdog._disagrees(right, known, "Vlasto Čepo") is False
    assert sherdog._disagrees({"sherdog_url": None}, known, "Vlasto Čepo") is True


def test_a_fighter_the_event_page_does_not_list_is_left_alone():
    """No authoritative URL means no opinion — don't churn the cache."""
    known = sherdog.event_fighter_urls("http://e", _FakePageSession(EVENT_HTML))
    assert sherdog._disagrees({"sherdog_url": None}, known, "Bogdan Grad") is False


def test_aliases_are_keyed_the_way_they_are_looked_up():
    """A key that normalize_name never produces is a silently dead entry."""
    from octagon.db.parsing import normalize_name

    for key in sherdog.SHERDOG_ALIASES:
        assert normalize_name(key) == key

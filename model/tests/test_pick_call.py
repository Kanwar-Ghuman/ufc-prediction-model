"""pick_call: no-call in the dead zone, decisive outside it."""

from octagon.predict import pick_call


def test_close_fight_is_no_call():
    assert pick_call(0.51, "A", "B", 0.42, 0.58).startswith("no call")
    assert pick_call(0.49, "A", "B", 0.42, 0.58).startswith("no call")
    assert "lean B" in pick_call(0.49, "A", "B", 0.42, 0.58)


def test_clear_favorite_is_a_pick():
    assert pick_call(0.70, "A", "B", 0.42, 0.58) == "pick: A (70%)"
    assert pick_call(0.30, "A", "B", 0.42, 0.58) == "pick: B (70%)"


def test_band_edge_is_no_call_inclusive():
    assert pick_call(0.42, "A", "B", 0.42, 0.58).startswith("no call")
    assert pick_call(0.58, "A", "B", 0.42, 0.58).startswith("no call")
    assert pick_call(0.581, "A", "B", 0.42, 0.58).startswith("pick:")

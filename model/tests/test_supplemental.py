from pathlib import Path

from octagon.db.schema import connect, init_db
from octagon.db.supplemental import load_supplemental
from octagon.features.build import build_feature_rows, load_bouts
from tests.test_features import canonical, make_bout


def test_official_supplement_is_idempotent_and_has_no_invented_stats(tmp_path):
    conn = connect(tmp_path / "test.db")
    init_db(conn)
    path = Path(__file__).parents[1] / "supplements/fights.yaml"
    assert load_supplemental(conn, path) == 1
    assert load_supplemental(conn, path) == 0
    bouts = load_bouts(conn)
    assert len(bouts) == 1
    assert bouts[0].duration_s == 70
    assert bouts[0].stats1 is None and bouts[0].stats2 is None
    before = make_bout(100, "2026-05-01", "Rongzhu", "Alice", winner="upcoming")
    after = make_bout(101, "2026-06-01", "Rongzhu", "Alice", winner="upcoming")
    rows = build_feature_rows([before, bouts[0], after], {})
    assert canonical(rows, 100)["f1_n_fights"] == 0
    assert canonical(rows, 101)["f1_n_fights"] == 1
    assert canonical(rows, 101)["f1_slpm_l3"] is None
    # If canonical data supplies the reversed bout, do not duplicate it.
    conn.execute("UPDATE fights SET fighter1='Victor Martinez', fighter2='Rongzhu', source='greco'")
    assert load_supplemental(conn, path) == 0
    conn.close()

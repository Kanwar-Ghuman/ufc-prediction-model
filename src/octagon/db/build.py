"""Build data/ufc.db from scratch out of the raw sources.

The database is a derived artifact: raw CSVs in, one SQLite file out.
Rebuilding from zero every time (rather than patching in place) keeps the
pipeline honest — there is no state that "remembers" old bugs.
"""

from pathlib import Path

from octagon.db.bootstrap import load_bootstrap_odds
from octagon.db.greco import load_greco
from octagon.db.schema import connect, init_db


def build_db(db_path: Path, greco_dir: Path, bootstrap_dir: Path) -> dict[str, int]:
    if db_path.exists():
        db_path.unlink()

    conn = connect(db_path)
    init_db(conn)
    counts = load_greco(conn, greco_dir)
    counts |= load_bootstrap_odds(conn, bootstrap_dir)
    conn.close()
    return counts

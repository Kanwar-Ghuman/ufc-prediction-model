"""Rebuild data/ufc.db from the raw CSVs. Always from scratch."""

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

"""Source-linked official results omitted by the canonical CSV feed.

No strike or grappling counts are inferred. Canonical results take precedence
when the feed later includes the bout, and reloading is idempotent.
"""

from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

from octagon.db.parsing import normalize_name


def load_supplemental(conn, path: Path) -> int:
    if not path.exists():
        return 0
    records = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    inserted = 0
    with conn:
        for record in records:
            day = date.fromisoformat(str(record["date"])).isoformat()
            source = record["source_url"]
            if urlparse(source).hostname not in {"ufc.com", "www.ufc.com"}:
                raise ValueError("Supplemental results require an official UFC source")
            if record["winner"] not in {"fighter1", "fighter2", "draw", "nc"}:
                raise ValueError("Invalid supplemental outcome")
            names = {normalize_name(record["fighter1"]), normalize_name(record["fighter2"])}
            existing = conn.execute(
                "SELECT fighter1, fighter2 FROM fights WHERE date = ?", (day,)).fetchall()
            if any({normalize_name(row[0]), normalize_name(row[1])} == names for row in existing):
                continue
            event_uid = f"supplement:{record['event']}:{day}"
            conn.execute(
                "INSERT OR IGNORE INTO events(uid, name, date, source) VALUES (?, ?, ?, ?)",
                (event_uid, record["event"], day, source))
            event_id = conn.execute(
                "SELECT event_id FROM events WHERE uid = ?", (event_uid,)).fetchone()[0]
            end_round, end_time = int(record["end_round"]), int(record["end_time_s"])
            scheduled = int(record["scheduled_rounds"])
            if not (1 <= end_round <= scheduled <= 5 and 0 <= end_time <= 300):
                raise ValueError("Invalid supplemental round or duration")
            conn.execute(
                """INSERT INTO fights
                (uid, event_id, date, weight_class, title_fight, scheduled_rounds,
                 fighter1, fighter2, winner, method, end_round, end_time_s, duration_s, source)
                VALUES (?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (f"supplement:{record['id']}", event_id, day, record["weight_class"],
                 scheduled, record["fighter1"], record["fighter2"], record["winner"],
                 record["method"], end_round, end_time, (end_round - 1) * 300 + end_time, source))
            inserted += 1
    return inserted

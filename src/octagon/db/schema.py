"""SQLite schema for data/ufc.db (v2 — Greco scrape as canonical source).

Design notes (read this before touching the schema):

* Canonical fight/event/fighter data comes from the Greco1899 ufcstats
  scrape (1994 -> 2026). The bootstrap dataset contributes only its
  closing odds (2014 -> 2023), matched onto fights by name + date.

* ``fights.winner`` preserves the source's fighter ordering. On ufcstats
  fight-details pages the winner is listed first only ~63% of the time, so
  ordering is less leaky than the bootstrap's winner-first convention — but
  the modeling dataset still randomizes corners (PRD 5.5). Never "fix"
  ordering here; the database stores raw truth.

* ``fight_stats`` holds one row per fighter per fight — whole-fight totals
  aggregated from ufcstats' round-by-round table. These are OUTPUTS of the
  fight: they only ever enter a model as historical rolling aggregates.

* Fighters carry a stable ufcstats ID (``uid``). Fights, however, reference
  fighters by NAME because the source's results table has no fighter links.
  A handful of UFC fighters share a name — the feature builder treats those
  names' tale-of-the-tape as unknown rather than guessing.
"""

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    event_id   INTEGER PRIMARY KEY,
    uid        TEXT UNIQUE,            -- ufcstats hex id from the event URL
    name       TEXT NOT NULL,
    date       TEXT NOT NULL,          -- ISO yyyy-mm-dd
    location   TEXT,
    source     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fights (
    fight_id         INTEGER PRIMARY KEY,
    uid              TEXT UNIQUE,      -- ufcstats hex id from the fight URL
    event_id         INTEGER NOT NULL REFERENCES events(event_id),
    date             TEXT NOT NULL,    -- denormalized for chronological queries
    weight_class     TEXT,
    title_fight      INTEGER NOT NULL DEFAULT 0,
    scheduled_rounds INTEGER,
    fighter1         TEXT NOT NULL,    -- source ordering preserved; see docstring
    fighter2         TEXT NOT NULL,
    winner           TEXT NOT NULL CHECK (winner IN ('fighter1', 'fighter2', 'draw', 'nc')),
    method           TEXT,             -- 'KO/TKO', 'SUB', 'U-DEC', 'S-DEC', 'M-DEC', 'DQ', ...
    method_detail    TEXT,
    end_round        INTEGER,
    end_time_s       INTEGER,          -- seconds into the final round
    duration_s       INTEGER,          -- total fight length in seconds
    source           TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fight_stats (
    fight_id       INTEGER NOT NULL REFERENCES fights(fight_id),
    fighter        TEXT NOT NULL,
    corner         TEXT NOT NULL CHECK (corner IN ('fighter1', 'fighter2')),
    knockdowns     INTEGER,
    sig_landed     INTEGER,
    sig_attempted  INTEGER,
    total_landed   INTEGER,            -- all strikes, not just significant
    total_attempted INTEGER,
    td_landed      INTEGER,
    td_attempted   INTEGER,
    sub_attempts   INTEGER,
    reversals      INTEGER,
    ctrl_seconds   INTEGER,            -- control time (NULL for old fights)
    -- Where the landed significant strikes went (style profile):
    head_landed    INTEGER,
    body_landed    INTEGER,
    leg_landed     INTEGER,
    -- ... and from where they were thrown:
    distance_landed INTEGER,
    clinch_landed  INTEGER,
    ground_landed  INTEGER,
    PRIMARY KEY (fight_id, corner)
);

CREATE TABLE IF NOT EXISTS fighters (
    fighter_id INTEGER PRIMARY KEY,
    uid        TEXT UNIQUE NOT NULL,   -- ufcstats hex id (stable, unlike names)
    name       TEXT NOT NULL,
    nickname   TEXT,
    height_cm  REAL,
    reach_cm   REAL,
    weight_kg  REAL,                   -- listed (division) weight, not walk-around
    stance     TEXT,
    dob        TEXT,                   -- ISO yyyy-mm-dd
    source     TEXT NOT NULL
);

-- Decimal odds aligned to the fight's fighter1/fighter2 orientation.
CREATE TABLE IF NOT EXISTS odds (
    odds_id       INTEGER PRIMARY KEY,
    fight_id      INTEGER NOT NULL REFERENCES fights(fight_id),
    fighter1_odds REAL NOT NULL,       -- decimal odds (e.g. 1.67)
    fighter2_odds REAL NOT NULL,
    source        TEXT NOT NULL,       -- 'betmma' for bootstrap closing odds
    UNIQUE (fight_id, source)
);

CREATE INDEX IF NOT EXISTS idx_fights_date ON fights(date);
CREATE INDEX IF NOT EXISTS idx_fight_stats_fighter ON fight_stats(fighter);
CREATE INDEX IF NOT EXISTS idx_fighters_name ON fighters(name);
"""


def connect(db_path: Path | str) -> sqlite3.Connection:
    """Open the SQLite DB with foreign keys enforced and dict-like rows."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Create all tables/indexes if they don't already exist."""
    conn.executescript(SCHEMA)
    conn.commit()

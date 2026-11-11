import sqlite3
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / 'instance' / 'retail.db'


@contextmanager
def connect(path=DEFAULT_DB):
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS purchases (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL CHECK(age BETWEEN 0 AND 120),
    gender TEXT NOT NULL,
    item TEXT NOT NULL,
    category TEXT NOT NULL,
    amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0),
    location TEXT NOT NULL,
    size TEXT NOT NULL,
    color TEXT NOT NULL,
    season TEXT NOT NULL,
    rating REAL NOT NULL CHECK(rating BETWEEN 0 AND 5),
    subscribed INTEGER NOT NULL CHECK(subscribed IN (0,1)),
    payment TEXT NOT NULL,
    shipping TEXT NOT NULL,
    discounted INTEGER NOT NULL CHECK(discounted IN (0,1)),
    promo INTEGER NOT NULL CHECK(promo IN (0,1)),
    previous_purchases INTEGER NOT NULL CHECK(previous_purchases >= 0),
    preferred_payment TEXT NOT NULL,
    frequency TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_category_season ON purchases(category, season);
CREATE TABLE IF NOT EXISTS etl_runs (
    id INTEGER PRIMARY KEY,
    loaded_at TEXT NOT NULL,
    source_name TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    row_count INTEGER NOT NULL,
    duration_ms INTEGER NOT NULL
);
"""

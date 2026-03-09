"""
Database module — stores scraped data in SQLite.

STEPS TO ADAPT:
  1. Edit the CREATE TABLE in init_db() to match YOUR data fields
  2. Update insert_record() parameter names to match your columns
  3. Update search_records() to search the columns that matter to you
  4. Update the UNIQUE INDEX to define what counts as a duplicate
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from config import DB_PATH


# ── Connection Helper ────────────────────────────────────────────────────

@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Yield a database connection that auto-commits/rolls back."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ── Schema ───────────────────────────────────────────────────────────────
# ✏️  CUSTOMIZE: change the table name and columns below to fit your data.

TABLE_NAME = "records"

def init_db() -> None:
    """Create the data table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                source        TEXT    NOT NULL,
                field_1       TEXT    NOT NULL,
                field_2       TEXT,
                field_3       TEXT,
                url           TEXT,
                extra         TEXT,
                date_scraped  TEXT    NOT NULL
            )
        """)
        # ✏️  CUSTOMIZE: define which combination of columns makes a record unique
        conn.execute(f"""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_records_unique
            ON {TABLE_NAME} (source, field_1, field_2, url)
        """)


# ── Insert ───────────────────────────────────────────────────────────────

def insert_record(record: dict) -> bool:
    """
    Insert a single record. Returns True if inserted, False if duplicate.

    Expected keys should match YOUR column names above, e.g.:
        source, field_1, field_2, field_3, url, extra
    """
    record.setdefault("date_scraped", datetime.now().isoformat())
    with get_connection() as conn:
        try:
            conn.execute(f"""
                INSERT INTO {TABLE_NAME}
                    (source, field_1, field_2, field_3, url, extra, date_scraped)
                VALUES
                    (:source, :field_1, :field_2, :field_3, :url, :extra, :date_scraped)
            """, record)
            return True
        except sqlite3.IntegrityError:
            return False  # duplicate


def insert_records(records: list[dict]) -> tuple[int, int]:
    """Insert multiple records. Returns (inserted_count, duplicate_count)."""
    inserted = 0
    duplicates = 0
    for record in records:
        if insert_record(record):
            inserted += 1
        else:
            duplicates += 1
    return inserted, duplicates


# ── Query ────────────────────────────────────────────────────────────────

def get_all_records() -> list[dict]:
    """Retrieve every record from the database."""
    with get_connection() as conn:
        rows = conn.execute(f"SELECT * FROM {TABLE_NAME} ORDER BY date_scraped DESC").fetchall()
        return [dict(row) for row in rows]


def get_record_count() -> int:
    """Return total number of stored records."""
    with get_connection() as conn:
        return conn.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]


def search_records(keyword: str) -> list[dict]:
    """
    Search records by keyword.
    ✏️  CUSTOMIZE: change the WHERE clause to search your relevant columns.
    """
    pattern = f"%{keyword}%"
    with get_connection() as conn:
        rows = conn.execute(f"""
            SELECT * FROM {TABLE_NAME}
            WHERE field_1 LIKE ?
               OR field_2 LIKE ?
               OR extra   LIKE ?
            ORDER BY date_scraped DESC
        """, (pattern, pattern, pattern)).fetchall()
        return [dict(row) for row in rows]

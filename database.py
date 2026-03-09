"""Database module — stores scraped job listings in SQLite."""

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from config import DB_PATH


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


def init_db() -> None:
    """Create the jobs table if it doesn't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                source        TEXT    NOT NULL,
                title         TEXT    NOT NULL,
                company       TEXT,
                location      TEXT,
                url           TEXT,
                tags          TEXT,
                salary        TEXT,
                description   TEXT,
                date_posted   TEXT,
                date_scraped  TEXT    NOT NULL
            )
        """)
        # Index for quick duplicate checks
        conn.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_jobs_unique
            ON jobs (source, title, company, url)
        """)


def insert_job(job: dict) -> bool:
    """
    Insert a single job record. Returns True if inserted, False if duplicate.

    Expected keys: source, title, company, location, url,
                   tags, salary, description, date_posted
    """
    job.setdefault("date_scraped", datetime.now().isoformat())
    with get_connection() as conn:
        try:
            conn.execute("""
                INSERT INTO jobs
                    (source, title, company, location, url,
                     tags, salary, description, date_posted, date_scraped)
                VALUES
                    (:source, :title, :company, :location, :url,
                     :tags, :salary, :description, :date_posted, :date_scraped)
            """, job)
            return True
        except sqlite3.IntegrityError:
            return False  # duplicate


def insert_jobs(jobs: list[dict]) -> tuple[int, int]:
    """Insert multiple jobs. Returns (inserted_count, duplicate_count)."""
    inserted = 0
    duplicates = 0
    for job in jobs:
        if insert_job(job):
            inserted += 1
        else:
            duplicates += 1
    return inserted, duplicates


def get_all_jobs() -> list[dict]:
    """Retrieve every job from the database."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM jobs ORDER BY date_scraped DESC").fetchall()
        return [dict(row) for row in rows]


def get_job_count() -> int:
    """Return total number of stored jobs."""
    with get_connection() as conn:
        return conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]


def search_jobs(keyword: str) -> list[dict]:
    """Search jobs by keyword in title, company, or tags."""
    pattern = f"%{keyword}%"
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT * FROM jobs
            WHERE title   LIKE ?
               OR company LIKE ?
               OR tags    LIKE ?
            ORDER BY date_scraped DESC
        """, (pattern, pattern, pattern)).fetchall()
        return [dict(row) for row in rows]

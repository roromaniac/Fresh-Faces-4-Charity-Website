"""Local SQLite visit log.

This file talks to a normal SQLite file on disk. It does not use Reflex
database models (rx.Model / sqlmodel).
"""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

# visits.db lives in the project folder. *.db is already gitignored.
DB_PATH = Path(__file__).resolve().parent.parent / "data" /"visits.db"

# SQLite connections are not always safe to share across threads, so we
# take a lock around each read or write.
_LOCK = Lock()


def _connect() -> sqlite3.Connection:
    """Connect to the visits.db SQLite database, ensuring the file and parent directory exist."""
    # Ensure the parent directory for the DB file exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    # timeout lets one request wait briefly if another is writing
    connection = sqlite3.connect(DB_PATH, timeout=5)
    # MEMORY journal avoids .db-wal / .db-shm files. Granian watches those and
    # would restart the app on every visit if we used WAL.
    connection.execute("PRAGMA journal_mode=MEMORY")
    # Ensure table exists (idempotent)
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            session_id TEXT NOT NULL DEFAULT '',
            visited_at TEXT NOT NULL
        )
        """
    )
    return connection


def init_db() -> None:
    """Create the visits table the first time we need it."""
    with _LOCK:
        connection = _connect()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    page TEXT NOT NULL,
                    session_id TEXT NOT NULL DEFAULT '',
                    visited_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_visits_session ON visits (session_id)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_visits_page ON visits (page)"
            )
            connection.commit()
        finally:
            connection.close()


def log_visit(page: str, session_id: str = "") -> None:
    """Save one page visit: which page, which browser session, and when."""
    init_db()
    visited_at = datetime.now(timezone.utc).isoformat()
    with _LOCK:
        connection = _connect()
        try:
            connection.execute(
                "INSERT INTO visits (page, session_id, visited_at) VALUES (?, ?, ?)",
                (page, session_id, visited_at),
            )
            connection.commit()
        finally:
            connection.close()


def count_visitors() -> int:
    """Count unique browser sessions. That is "how many people came by"."""
    init_db()
    with _LOCK:
        connection = _connect()
        try:
            unique = connection.execute(
                "SELECT COUNT(DISTINCT session_id) FROM visits WHERE session_id <> ''"
            ).fetchone()
            unique_count = int(unique[0]) if unique else 0
            if unique_count > 0:
                return unique_count
            # Fallback if older rows have no session id yet
            total = connection.execute("SELECT COUNT(*) FROM visits").fetchone()
            return int(total[0]) if total else 0
        finally:
            connection.close()

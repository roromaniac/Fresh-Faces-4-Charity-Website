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

# Counted once at startup, then bumped when a new browser session arrives.
# Page loads read this number instead of counting the whole table again.
_visitor_total: int | None = None


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


def _count_unlocked(connection: sqlite3.Connection) -> int:
    """Count unique browser sessions on a connection the caller already holds."""
    unique = connection.execute(
        "SELECT COUNT(DISTINCT session_id) FROM visits WHERE session_id <> ''"
    ).fetchone()
    unique_count = int(unique[0]) if unique else 0
    if unique_count > 0:
        return unique_count
    # Fallback if older rows have no session id yet
    total = connection.execute("SELECT COUNT(*) FROM visits").fetchone()
    return int(total[0]) if total else 0


def count_visitors() -> int:
    """Count unique browser sessions. That is "how many people came by"."""
    with _LOCK:
        connection = _connect()
        try:
            return _count_unlocked(connection)
        finally:
            connection.close()


def seed_visitor_total() -> int:
    """Count past visitors once, so later page loads can reuse that number."""
    global _visitor_total
    with _LOCK:
        if _visitor_total is not None:
            return _visitor_total
        connection = _connect()
        try:
            _visitor_total = _count_unlocked(connection)
            return _visitor_total
        finally:
            connection.close()


def record_page_view(page: str, session_id: str = "") -> int:
    """Save one page view and return the shared visitor total.

    A brand-new session adds 1. A return visit keeps the saved total.
    """
    global _visitor_total
    visited_at = datetime.now(timezone.utc).isoformat()
    with _LOCK:
        connection = _connect()
        try:
            if _visitor_total is None:
                _visitor_total = _count_unlocked(connection)
            is_new = False
            if session_id:
                existing = connection.execute(
                    "SELECT 1 FROM visits WHERE session_id = ? LIMIT 1",
                    (session_id,),
                ).fetchone()
                is_new = existing is None
            connection.execute(
                "INSERT INTO visits (page, session_id, visited_at) VALUES (?, ?, ?)",
                (page, session_id, visited_at),
            )
            connection.commit()
            if is_new:
                _visitor_total += 1
            return _visitor_total
        finally:
            connection.close()

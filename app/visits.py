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
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "visits.db"

# Two locks so a slow disk write never blocks the number we show.
# Take _count_lock first if you ever need both, so they cannot deadlock.
_count_lock = Lock()
_db_lock = Lock()

# One connection for the whole process. Reopening the file on every page
# view is slow on the host's disk.
_connection: sqlite3.Connection | None = None

# Counted once at startup, then bumped by 1 on every page view.
# Page loads read this number instead of counting the whole table again.
_visitor_total: int | None = None
_known_sessions: set[str] | None = None


def _database() -> sqlite3.Connection:
    """Open visits.db once and reuse it. Caller must hold _db_lock."""
    global _connection
    if _connection is not None:
        return _connection

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=5, check_same_thread=False)
    # MEMORY journal avoids .db-wal / .db-shm files. Granian watches those and
    # would restart the app on every visit if we used WAL.
    connection.execute("PRAGMA journal_mode=MEMORY").fetchone()
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
    _connection = connection
    return connection


def _load_known_sessions() -> None:
    """Read the saved visit count once. Caller must hold _count_lock.

    Every row is one visit. Counting only distinct browsers hides later
    page views, so the number on the poster barely moves.
    """
    global _visitor_total, _known_sessions
    with _db_lock:
        connection = _database()
        counted = connection.execute("SELECT COUNT(*) FROM visits").fetchone()
        total = int(counted[0]) if counted else 0
    # Empty set means "already loaded", not "no visitors".
    _known_sessions = set()
    _visitor_total = total


def init_db() -> None:
    """Create the visits table the first time we need it."""
    with _db_lock:
        _database()


def cached_visitor_total() -> int | None:
    """Visitor total already in memory, or None if startup has not counted yet."""
    return _visitor_total


def seed_visitor_total() -> int:
    """Load past visitors once, so later page loads can reuse that number."""
    with _count_lock:
        if _known_sessions is None:
            _load_known_sessions()
        return _visitor_total or 0


def resync_visitor_total() -> int:
    """Recount the visits saved in the database and fix the shared number.

    The page number is only "+1 in memory", so it can drift if rows were
    deleted or a save failed. The slow database count runs WITHOUT the
    count lock, so page views keep working while it runs.
    """
    global _visitor_total, _known_sessions
    # Startup has not loaded anything yet, so there is nothing to fix.
    if _known_sessions is None:
        return seed_visitor_total()

    # Step 1: count rows (slow part). Only the database lock is held.
    with _db_lock:
        connection = _database()
        counted = connection.execute("SELECT COUNT(*) FROM visits").fetchone()
        total = int(counted[0]) if counted else 0

    # Step 2: swap in the number (instant). A visit counted in the split
    # second before its row is saved may be off by 1 until the next recount.
    with _count_lock:
        _visitor_total = total
    return total


def count_visitors() -> int:
    """How many visits are saved. Uses the saved total after startup."""
    return seed_visitor_total()


def remember_visitor(session_id: str = "") -> int:
    """Add one visit and return the shared total.

    This does not write to disk, so the page can show the number immediately.
    The same browser counts again on a later page view. Callers still pass
    session_id so the saved row can name that browser.
    """
    global _visitor_total, _known_sessions
    with _count_lock:
        if _known_sessions is None:
            _load_known_sessions()
        total = (_visitor_total or 0) + 1
        _visitor_total = total
        return total


def save_page_view(page: str, session_id: str = "") -> None:
    """Append one page visit to the database."""
    visited_at = datetime.now(timezone.utc).isoformat()
    with _db_lock:
        connection = _database()
        connection.execute(
            "INSERT INTO visits (page, session_id, visited_at) VALUES (?, ?, ?)",
            (page, session_id, visited_at),
        )
        connection.commit()


def log_visit(page: str, session_id: str = "") -> None:
    """Save one page visit: which page, which browser session, and when."""
    remember_visitor(session_id)
    save_page_view(page, session_id)


def record_page_view(page: str, session_id: str = "") -> int:
    """Save one page view and return the shared visitor total.

    Each page view adds 1, including a return visit.
    """
    total = remember_visitor(session_id)
    save_page_view(page, session_id)
    return total

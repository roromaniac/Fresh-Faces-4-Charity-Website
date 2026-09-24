import csv
import sqlite3
import os
import re
import tempfile
from contextlib import contextmanager

CSV_FILE = os.path.join("data", "FF4_Eligibility.csv")
DB_FILE = os.path.join("data", "eligibility.db")
SQL_SCRIPT = os.path.join("data", "eligibility.sql")
TABLE_NAME = "FF4 Eligibility"  # matches the table in .sql

# Other processes (the website, a second server worker) read this to find the
# finished database. The temp folder is writable even when the app folder is not.
_PATH_FILE = os.path.join(tempfile.gettempdir(), "ff4_eligibility_path.txt")
_LOCK_FILE = os.path.join(tempfile.gettempdir(), "ff4_eligibility.lock")

def is_int_field(col):
    """Determines if a column should be an INTEGER field by column header conventions."""
    # All columns except for names are placings (should be integers)
    col_lower = col.lower()
    if "placing" in col_lower:
        return True
    if col_lower in ("player", "discord name", "twitch name"):
        return False
    # Ensure any future columns default to TEXT, be conservative
    return False

def coerce_row_types(row, columns):
    """Cast int-looking values to actual int type fields, leave others alone."""
    new_row = []
    for value, col in zip(row, columns):
        if is_int_field(col):
            try:
                # Treat blank as None (NULL), else int
                new_row.append(None if value.strip() == "" else int(value))
            except Exception:
                new_row.append(None)
        else:
            new_row.append(value)
    return new_row

def eligibility_db_path() -> str:
    """Path of the database the website should read."""
    try:
        with open(_PATH_FILE, encoding="utf-8") as handle:
            saved = handle.read().strip()
    except OSError:
        saved = ""
    if saved and os.path.exists(saved):
        return saved
    return DB_FILE


@contextmanager
def _rebuild_lock():
    """Only one process may rebuild the database at a time."""
    handle = open(_LOCK_FILE, "a+")
    try:
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        if os.name == "nt":
            import msvcrt

            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
        handle.close()


def _has_eligibility_columns(db_path: str) -> bool:
    """True when the lookup columns exist. A half-written database does not."""
    try:
        conn = sqlite3.connect(db_path, timeout=5)
    except sqlite3.Error:
        return False
    try:
        rows = conn.execute(f'PRAGMA table_info("{TABLE_NAME}")').fetchall()
    except sqlite3.Error:
        return False
    finally:
        conn.close()
    names = {row[1] for row in rows}
    return "eligible" in names and "reason" in names


def _is_current(db_path: str) -> bool:
    """Skip a rebuild when this file is already newer than the CSV and complete."""
    if not os.path.exists(db_path) or not _has_eligibility_columns(db_path):
        return False
    try:
        return os.path.getmtime(db_path) >= os.path.getmtime(CSV_FILE)
    except OSError:
        return False


def _write_database(db_path: str) -> None:
    """Create a new database file. The journal stays in memory, so no sidecar file is needed."""
    parent = os.path.dirname(db_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path, timeout=30)
    try:
        # DELETE/WAL journals need extra files next to the database. On the
        # deployed machine those files cannot be created, and the write fails.
        conn.execute("PRAGMA journal_mode=MEMORY")
        cur = conn.cursor()

        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            columns = next(reader)

        col_defs = []
        for col in columns:
            if is_int_field(col):
                col_defs.append(f'"{col}" INTEGER')
            else:
                col_defs.append(f'"{col}" TEXT')
        cur.execute(f'CREATE TABLE "{TABLE_NAME}" ({", ".join(col_defs)});')

        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            to_insert = [coerce_row_types(row, columns) for row in reader]
        qmarks = ", ".join(["?"] * len(columns))
        cur.executemany(
            f'INSERT INTO "{TABLE_NAME}" VALUES ({qmarks})',
            to_insert,
        )
        print(f"✅ Imported {len(to_insert)} rows from {CSV_FILE} into {db_path} [{TABLE_NAME}]")

        with open(SQL_SCRIPT, encoding="utf-8") as s:
            sql_script = s.read()
        # SQLite here does not accept "ADD COLUMN IF NOT EXISTS".
        sql_script = re.sub(r"ADD COLUMN IF NOT EXISTS", "ADD COLUMN", sql_script)
        cur.executescript(sql_script)
        print(f"✅ Ran eligibility update script ({SQL_SCRIPT})")
        conn.commit()
    finally:
        conn.close()


def _remember_path(db_path: str) -> None:
    with open(_PATH_FILE, "w", encoding="utf-8") as handle:
        handle.write(db_path)


def main():
    """Import the eligibility CSV into SQLite, then apply eligibility.sql.

    One process builds the file. The others wait, then reuse it. The live
    database is only replaced after the new file is complete, so a failed
    build cannot leave a table missing the eligible column.
    """
    with _rebuild_lock():
        current = eligibility_db_path()
        if _is_current(current):
            return

        # Build away from the live file. A crash here does not delete the old one.
        fd, temporary = tempfile.mkstemp(prefix="ff4_eligibility_", suffix=".db")
        os.close(fd)
        try:
            _write_database(temporary)
            if not _has_eligibility_columns(temporary):
                raise RuntimeError("Eligibility database was built without eligible/reason columns.")

            destination = DB_FILE
            try:
                os.makedirs(os.path.dirname(DB_FILE) or ".", exist_ok=True)
                os.replace(temporary, DB_FILE)
                temporary = ""
            except OSError:
                # The app folder is not writable (deployed host). Keep the temp copy.
                destination = os.path.join(tempfile.gettempdir(), "ff4_eligibility.db")
                os.replace(temporary, destination)
                temporary = ""
            _remember_path(destination)
            print(f"✅ Eligibility database ready at {destination}")
        finally:
            if temporary and os.path.exists(temporary):
                os.remove(temporary)

if __name__ == "__main__":
    main()
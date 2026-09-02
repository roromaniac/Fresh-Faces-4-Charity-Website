import csv
import sqlite3
import os
import re

CSV_FILE = os.path.join("data", "FF4_Eligibility.csv")
DB_FILE = os.path.join("data", "eligibility.db")
SQL_SCRIPT = os.path.join("data", "eligibility.sql")
TABLE_NAME = "FF4 Eligibility"  # matches the table in .sql

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

def main():
    # Connect to the SQLite DB
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # 1. Optional: drop table if exists (for full re-import)
    cur.execute(f'DROP TABLE IF EXISTS "{TABLE_NAME}"')

    # Read the CSV header for column names
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        columns = next(reader)

    # Build the CREATE TABLE statement, coercing all *placing* fields to INTEGER, names to TEXT
    col_defs = []
    for col in columns:
        if is_int_field(col):
            col_defs.append(f'"{col}" INTEGER')
        else:
            col_defs.append(f'"{col}" TEXT')
    col_defs_str = ', '.join(col_defs)
    cur.execute(f'CREATE TABLE "{TABLE_NAME}" ({col_defs_str});')

    # Import all rows at once, ensuring all eligible fields are written as ints
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        to_insert = [coerce_row_types(row, columns) for row in reader]
    qmarks = ", ".join(["?"] * len(columns))
    cur.executemany(
        f'INSERT INTO "{TABLE_NAME}" VALUES ({qmarks})',
        to_insert,
    )
    print(f"✅ Imported {len(to_insert)} rows from {CSV_FILE} into {DB_FILE} [{TABLE_NAME}]")

    # 3. Execute the eligibility.sql script to set/update eligibility logic
    with open(SQL_SCRIPT, encoding="utf-8") as s:
        sql_script = s.read()
    # Patch: replace non-standard "ADD COLUMN IF NOT EXISTS" with just "ADD COLUMN"
    # SQLite supports "IF NOT EXISTS" for CREATE TABLE, but not for ALTER TABLE ADD COLUMN syntax until version 3.35+.
    # For max compatibility, remove the "IF NOT EXISTS".
    sql_script = re.sub(r'ADD COLUMN IF NOT EXISTS', 'ADD COLUMN', sql_script)
    cur.executescript(sql_script)
    print(f"✅ Ran eligibility update script ({SQL_SCRIPT})")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
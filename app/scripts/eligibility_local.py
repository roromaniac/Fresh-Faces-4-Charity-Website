import csv
import sqlite3
import os

try:
    from app.scripts.eligibility import eligibility_db_path
except ImportError:
    # Running this file directly puts its folder, not the project, on the path.
    from eligibility import eligibility_db_path

TABLE_NAME = "FF4 Eligibility"
OUT_CSV = os.path.join("data", "FF4_Eligibility_CALCULATED.csv")

def export_calculated_csv():
    """Export the full calculated eligibility table to a CSV."""
    db_file = eligibility_db_path()
    if not os.path.exists(db_file):
        raise FileNotFoundError(
            f"Eligibility DB not found at {db_file}. Please run the main eligibility script first."
        )
    # Connect to the eligibility.db
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    # Query table columns (reflecting all calculated columns as well)
    cur.execute(f'PRAGMA table_info("{TABLE_NAME}");')
    columns = [row[1] for row in cur.fetchall()]

    # Query all results
    cur.execute(f'SELECT * FROM "{TABLE_NAME}";')
    rows = cur.fetchall()

    # Write to output CSV (always overwrite)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"✅ Exported calculated eligibility table from {db_file} to {OUT_CSV} ({len(rows)} rows)")

if __name__ == "__main__":
    export_calculated_csv()
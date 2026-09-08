import sqlite3
import os

# Always resolve DB path relative to this file's location
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales_crm.db")


def create_database():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table with full schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT    NOT NULL,
        email       TEXT    NOT NULL,
        company     TEXT    NOT NULL,
        budget      REAL    NOT NULL,
        requirement TEXT    NOT NULL,
        score       INTEGER NOT NULL,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Migration: add created_at column if it doesn't exist (for older DBs)
    cursor.execute("PRAGMA table_info(leads)")
    columns = [row[1] for row in cursor.fetchall()]

    if "created_at" not in columns:
        # SQLite does not allow non-constant defaults in ALTER TABLE,
        # so existing rows get NULL; new rows use the trigger/app default
        cursor.execute(
            "ALTER TABLE leads ADD COLUMN created_at DATETIME"
        )

    conn.commit()
    conn.close()

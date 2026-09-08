import sqlite3
import pandas as pd
import os

# Always resolve DB path relative to this file's location
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sales_crm.db")


def save_lead(name, email, company, budget, requirement, score):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO leads (name, email, company, budget, requirement, score)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, email, company, budget, requirement, score)
    )

    conn.commit()
    conn.close()


def get_all_leads():

    conn = sqlite3.connect(DB_PATH)

    try:
        df = pd.read_sql_query(
            "SELECT id, name, email, company, budget, requirement, score, created_at FROM leads ORDER BY id DESC",
            conn
        )
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()

    return df


def delete_lead(lead_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))

    conn.commit()
    conn.close()

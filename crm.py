import sqlite3
import pandas as pd

DB_NAME = "sales_crm.db"

def save_lead(
    name,
    email,
    company,
    budget,
    requirement,
    score
):
    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO leads
        (
            name,
            email,
            company,
            budget,
            requirement,
            score
        )
        VALUES (?,?,?,?,?,?)
        """,
        (
            name,
            email,
            company,
            budget,
            requirement,
            score
        )
    )

    conn.commit()
    conn.close()


def get_all_leads():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM leads",
        conn
    )

    conn.close()

    return df
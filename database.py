import sqlite3

def create_database():

    conn = sqlite3.connect("sales_crm.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leads(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT,

        email TEXT,

        company TEXT,

        budget TEXT,

        requirement TEXT,

        score INTEGER
    )
    """)

    conn.commit()
    conn.close()
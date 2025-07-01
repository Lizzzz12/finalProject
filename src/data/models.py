# -------------------- src/data/models.py --------------------
import sqlite3
import os

def create_tables():
    os.makedirs("data_output", exist_ok=True)
    conn = sqlite3.connect("data_output/db.sqlite")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT
        )
    ''')
    conn.commit()
    conn.close()

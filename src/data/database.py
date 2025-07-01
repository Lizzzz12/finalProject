import sqlite3
import os

# Dynamically get the path to the project root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DB_PATH = os.path.join(BASE_DIR, 'data_output', 'db.sqlite')

def insert_item(title, price):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO items (title, price) VALUES (?, ?)", (title, price))
    conn.commit()
    conn.close()

def count_items():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    total = cur.fetchone()[0]
    conn.close()
    return total

def get_all_items():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, title, price FROM items")
    rows = cur.fetchall()
    conn.close()
    return rows

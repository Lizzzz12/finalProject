import sqlite3

def insert_item(title):
    conn = sqlite3.connect("data_output/db.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO items (title) VALUES (?)", (title,))
    conn.commit()
    conn.close()

def count_items():
    import sqlite3
    conn = sqlite3.connect("data_output/db.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    total = cur.fetchone()[0]
    conn.close()
    return total

def get_all_items():
    conn = sqlite3.connect("data_output/db.sqlite")
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM items")
    rows = cur.fetchall()
    conn.close()
    return rows

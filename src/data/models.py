<<<<<<< HEAD
import sqlite3
import os

def create_tables():
    os.makedirs("data_output", exist_ok=True)
    conn = sqlite3.connect("data_output/db.sqlite")
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT
        )
    ''')
    conn.commit()
    conn.close()
=======
# src/data/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProductData:
    title: str
    price: str
    url: str
    source: str  # e.g., 'Amazon', 'eBay'
    timestamp: datetime
>>>>>>> f0ba75326657d2188e7194689ed6a139e5d23b19

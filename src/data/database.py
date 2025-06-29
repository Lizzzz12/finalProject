# src/data/database.py
import sqlite3
from datetime import datetime
from src.data.models import ProductData
from src.utils.logger import logger


DB_PATH = "data_output/products.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            url TEXT,
            source TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()
    logger.info("Database table ensured.")

def save_product(product: ProductData):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (title, price, url, source, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (product.title, product.price, product.url, product.source, product.timestamp.isoformat()))
    conn.commit()
    conn.close()
    logger.info(f"Product saved: {product.title}")

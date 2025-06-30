# test_database.py
import sqlite3
from src.data.database import DatabaseManager
import pytest


@pytest.fixture
def db_manager():
    manager = DatabaseManager()
    yield manager
    manager.close()


def test_database_creation(db_manager):
    """Test if database and tables are created properly"""
    cursor = db_manager.connection.cursor()

    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    assert 'products' in tables
    assert 'price_history' in tables


def test_add_product(db_manager):
    """Test adding a product to the database"""
    test_product = {
        'product_id': 'TEST123',
        'name': 'Test Product',
        'description': 'Test Description',
        'category': 'Test Category',
        'source_website': 'Test Site',
        'url': 'http://test.com/product'
    }

    product_id = db_manager.add_product(test_product)
    assert product_id is not None

    # Verify the product was added
    cursor = db_manager.connection.cursor()
    cursor.execute("SELECT name FROM products WHERE product_id = 'TEST123'")
    result = cursor.fetchone()
    assert result[0] == 'Test Product'


def test_add_price_record(db_manager):
    """Test adding price history"""
    db_manager.add_price_record('TEST123', 99.99)

    cursor = db_manager.connection.cursor()
    cursor.execute("SELECT price FROM price_history WHERE product_id = 'TEST123'")
    result = cursor.fetchone()
    assert result[0] == 99.99
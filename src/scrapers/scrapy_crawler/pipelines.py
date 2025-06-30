# src/scrapers/scrapy_crawler/pipelines.py

from src.data.database import create_table, save_product
from src.utils.logger import logger

def save_product_to_db(product):
    try:
        create_table()
        save_product(product)
    except Exception as e:
        logger.error(f"Failed to save product: {e}")

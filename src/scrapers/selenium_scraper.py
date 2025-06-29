# src/scrapers/selenium_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timezone
import time

from src.data.models import ProductData
from src.data.database import create_table, save_product
from src.utils.logger import logger

def scrape_ebay_search(query="laptop", max_items=5):
    logger.info(f"Starting eBay scrape for query: {query}")

    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    url = f"https://www.ebay.com/sch/i.html?_nkw={query}"
    driver.get(url)

    time.sleep(3)  # allow JS to load

    items = driver.find_elements(By.CSS_SELECTOR, ".s-item")
    logger.info(f"Found {len(items)} items")

    results = []

    for item in items[:max_items]:
        try:
            title_tag = item.find_element(By.CSS_SELECTOR, ".s-item__title")
            price_tag = item.find_element(By.CSS_SELECTOR, ".s-item__price")
            link_tag = item.find_element(By.CSS_SELECTOR, ".s-item__link")

            title = title_tag.text.strip()
            price = price_tag.text.strip().replace("US", "").replace("$", "").strip()
            url = link_tag.get_attribute("href")

            results.append(ProductData(
                title=title,
                price=price,
                url=url,
                source="eBay",
                timestamp=datetime.now(timezone.utc)
            ))

        except Exception as e:
            logger.warning(f"Skipping item due to error: {e}")

    driver.quit()
    return results

if __name__ == "__main__":
    create_table()
    products = scrape_ebay_search(query="headphones", max_items=5)
    for product in products:
        save_product(product)

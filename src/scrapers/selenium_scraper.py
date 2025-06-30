<<<<<<< HEAD
# Updated Selenium eBay Scraper with Pagination (up to 10 pages)
=======
# src/scrapers/selenium_scraper.py
>>>>>>> f0ba75326657d2188e7194689ed6a139e5d23b19

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
<<<<<<< HEAD
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from .base_scraper import BaseScraper
from src.data.database import insert_item
from src.utils.logger import logger

class SeleniumScraper(BaseScraper):
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def run(self):
        base_url = "https://www.ebay.com/sch/i.html?_nkw=laptop&_pgn={}"
        total_inserted = 0

        for page in range(1, 51):  # Pages 1 to 10
            url = base_url.format(page)
            self.driver.get(url)
            logger.info(f"Fetching eBay page {page} - {url}")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "s-item"))
                )
            except Exception as e:
                logger.error(f"Page {page} load failed: {e}")
                continue

            items = self.driver.find_elements(By.CLASS_NAME, "s-item")
            results = []

            for item in items:
                try:
                    title_element = item.find_element(By.CLASS_NAME, "s-item__title")
                    title = title_element.text.strip()
                    if title and "Shop on eBay" not in title:
                        results.append(title)
                except Exception:
                    continue

            logger.info(f"Page {page}: Extracted {len(results)} items")

            for title in results:
                insert_item(title)
                total_inserted += 1

        logger.info(f"Total items inserted from eBay: {total_inserted}")
        self.driver.quit()
=======
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
>>>>>>> f0ba75326657d2188e7194689ed6a139e5d23b19

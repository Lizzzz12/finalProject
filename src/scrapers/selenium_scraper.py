# -------------------- src/scrapers/selenium_scraper.py (eBay) --------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.scrapers.base_scraper import BaseScraper
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

        for page in range(1, 5):
            url = base_url.format(page)
            self.driver.get(url)
            logger.info(f"Fetching eBay page {page}: {url}")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "s-item"))
                )
            except Exception as e:
                logger.error(f"Page {page} load failed: {e}")
                continue

            items = self.driver.find_elements(By.CLASS_NAME, "s-item")
            for item in items:
                try:
                    title_el = item.find_element(By.CLASS_NAME, "s-item__title")
                    price_el = item.find_element(By.CLASS_NAME, "s-item__price")

                    title = title_el.text.strip()
                    price = price_el.text.strip() if price_el else "N/A"

                    if title and "Shop on eBay" not in title:
                        print(f"[DEBUG] INSERTING → TITLE: {title} | PRICE: {price}")
                        insert_item(title, price)
                        total_inserted += 1
                except Exception:
                    continue

        logger.info(f"Total eBay items inserted: {total_inserted}")
        self.driver.quit()

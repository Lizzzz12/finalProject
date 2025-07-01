# -------------------- src/scrapers/newegg_selenium.py --------------------
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.data.database import insert_item
from src.utils.logger import logger
from src.scrapers.base_scraper import BaseScraper

class NeweggSeleniumScraper(BaseScraper):
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def run(self):
        base_url = "https://www.newegg.com/p/pl?d=laptop&page={}"
        total_inserted = 0

        for page in range(1, 5):
            url = base_url.format(page)
            self.driver.get(url)
            logger.info(f"Fetching Newegg page {page}: {url}")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "item-cell"))
                )
                items = self.driver.find_elements(By.CLASS_NAME, "item-cell")
                for item in items:
                    try:
                        title_el = item.find_element(By.CLASS_NAME, "item-title")
                        price_el = item.find_element(By.CLASS_NAME, "price-current")

                        title = title_el.text.strip()
                        price = price_el.text.strip().split("\n")[0] if price_el else "N/A"

                        if title:
                            print(f"[DEBUG] INSERTING → TITLE: {title} | PRICE: {price}")

                            insert_item(title, price)
                            total_inserted += 1
                    except Exception:
                        continue
            except Exception as e:
                logger.warning(f"Failed to load Newegg page {page}: {e}")

        logger.info(f"Newegg Selenium: Total inserted = {total_inserted}")
        self.driver.quit()

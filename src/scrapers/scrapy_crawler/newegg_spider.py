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

        for page in range(1, 51):  # Scrape pages 1–5
            url = base_url.format(page)
            self.driver.get(url)
            logger.info(f"Fetching Newegg page {page}: {url}")

            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "item-title"))
                )
            except Exception as e:
                logger.warning(f"Page {page} failed to load items: {e}")
                continue

            titles = self.driver.find_elements(By.CLASS_NAME, "item-title")
            logger.info(f"Page {page}: Found {len(titles)} titles")

            for title_el in titles:
                title = title_el.text.strip()
                if title:
                    insert_item(title)
                    total_inserted += 1
                    print("Inserted:", title)

        logger.info(f"Newegg Selenium: Total inserted = {total_inserted}")
        self.driver.quit()

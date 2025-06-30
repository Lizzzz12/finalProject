import requests
from bs4 import BeautifulSoup
from src.data.database import insert_item
from src.utils.logger import logger
from .base_scraper import BaseScraper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}


class AmazonScraper(BaseScraper):
    def run(self):
        url = "https://www.amazon.com/s?k=laptop"
        logger.info(f"Fetching Amazon URL: {url}")

        try:
            response = requests.get(url, headers=HEADERS)
            soup = BeautifulSoup(response.content, "html.parser")

            product_blocks = soup.select("div.s-main-slot div[data-component-type='s-search-result']")
            count = 0

            for block in product_blocks:
                title_tag = block.select_one("h2 span")
                if title_tag:
                    title = title_tag.get_text(strip=True)
                    if title:
                        insert_item(title)
                        logger.info(f"Amazon scraped: {title}")
                        count += 1

            print(f"Inserted {count} Amazon records")
        except Exception as e:
            logger.error(f"Amazon scraper failed: {e}")

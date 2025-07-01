# -------------------- src/scrapers/amazon_scraper.py --------------------
import requests
from bs4 import BeautifulSoup
from src.data.database import insert_item
from src.utils.logger import logger
from src.scrapers.base_scraper import BaseScraper

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:112.0) Gecko/20100101 Firefox/112.0",
    "Accept-Language": "en-US,en;q=0.9",
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
                price_whole = block.select_one("span.a-price-whole")
                price_frac = block.select_one("span.a-price-fraction")

                if title_tag:
                    title = title_tag.get_text(strip=True)
                    if price_whole and price_frac:
                        price = f"${price_whole.text}.{price_frac.text}"
                    else:
                        price = "N/A"
                    if title:
                        print(f"[DEBUG] INSERTING → TITLE: {title} | PRICE: {price}")

                        insert_item(title, price)
                        count += 1
            logger.info(f"Amazon inserted {count} titles")
        except Exception as e:
            logger.error(f"Amazon scraper failed: {e}")
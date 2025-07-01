import requests
from bs4 import BeautifulSoup
from src.scrapers.base_scraper import BaseScraper
from src.data.database import insert_item
from src.utils.logger import logger

class StaticScraper(BaseScraper):
    def run(self):
        url = "https://www.walmart.com/brand/laroche-posay/10046134?athAsset=eyJhdGhjcGlkIjoiNGE3NGZmN2UtZDY5Yi00NmFlLTgxYjUtZWZhMDViNDIwMDMwIiwiYWV3ciI6IkNUUiJ9&athena=true"
        html = self.fetch(url)
        return self.parse(html)

    def fetch(self, url):
        logger.info(f"Fetching URL: {url}")
        response = requests.get(url)
        return response.text

    def parse(self, content):
        soup = BeautifulSoup(content, "html.parser")
        titles = [book.h3.a["title"] for book in soup.select("article.product_pod")]
        return titles

    def save_to_db(self, title):
        insert_item(title, "N/A")  # 👈 add default price

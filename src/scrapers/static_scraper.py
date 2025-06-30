import requests
from bs4 import BeautifulSoup
from .base_scraper import BaseScraper
from src.data.database import insert_item
from src.utils.logger import logger


class StaticScraper(BaseScraper):
    def run(self):
        url = "https://www.amazon.com/Skytech-Gaming-PC-Desktop-Windows/dp/B0BXCJVKHF/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.860dbf94-9f09-4ada-8615-32eb5ada253a&dib=eyJ2IjoiMSJ9.5G4LxoP3-ZdomJxxTmtyBgfZKp6gPrEBXUHlrwGRq6LYLkPJ_dEHBfM9ktwhlnqKRwFfiNuN6ETd7A4BWat6XHJ-qQK78vlPn3MRIDy1XnkjylJeopr4TINkinuOOYfavwmWWNd-3zfJD2P3pr2vreAmVXsmA1__FUSO-zyUIro1qBXnAVUxncF9OyYES2AD7WlJtyAIgWiJ5u_1aXdCU2dULJFV7dEI_igaoWyRuKjKMz45gBNg-g4mLAxZINdQnjwknJGO-qbt-Se140gb1gbJYiWkm48_pfQQdfe_Y1M.oAZjrAGhkGK-rPtzEL6q8rxSWB_QtMTgwd4GDPRtnV0&dib_tag=se&keywords=gaming&pd_rd_r=64fe5caf-6880-4fce-9187-1e17d7992da3&pd_rd_w=qpJW4&pd_rd_wg=YR9Mb&qid=1751292492&sr=8-1"
        html = self.fetch(url)
        return self.parse(html)

    def fetch(self, url):
        logger.info(f"Fetching URL: {url}")
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse(self, content):
        soup = BeautifulSoup(content, "html.parser")
        titles = [book.h3.a["title"] for book in soup.select("article.product_pod")]
        return titles

    def save_to_db(self, title):
        insert_item(title)

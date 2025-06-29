# amazon_spider.py
import scrapy
from src.scrapers.scrapy_crawler.items import ProductItem
from src.utils.config import get_site_config

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    cfg  = get_site_config("amazon")
    start_urls = [cfg["product_url"].format(asin="B08N5WRWNW")]

    def parse(self, response):
        item = ProductItem()
        item["site"]  = "amazon"
        item["url"]   = response.url
        item["name"]  = response.css(self.cfg["title_selector"]).get().strip()
        item["price"] = response.css(self.cfg["price_selector"]).get().strip()
        yield item

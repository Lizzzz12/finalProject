# src/scrapers/scrapy_crawler/spiders/aliexpress_spider.py

import scrapy
from src.scrapers.scrapy_crawler.items import ProductItem
from src.utils.config import get_site_config

class AliExpressSpider(scrapy.Spider):
    name = "aliexpress"
    cfg  = get_site_config("aliexpress")
    # e.g. cfg["product_url"] might be "https://www.aliexpress.com/item/{item_id}.html"
    start_urls = [cfg["product_url"].format(item_id="1005002686561234")]

    def parse(self, response):
        item = ProductItem()
        item["site"]  = "aliexpress"
        item["url"]   = response.url

        # Use the selectors you defined in config/scrappers.yaml
        title_sel = self.cfg.get("title_selector", "h1.product-title-text")
        price_sel = self.cfg.get("price_selector", "span.product-price-value")

        # Extract & clean
        name_tag  = response.css(title_sel).get()
        price_tag = response.css(price_sel).get()

        item["name"]  = name_tag.strip()  if name_tag  else None
        item["price"] = price_tag.strip() if price_tag else None

        yield item

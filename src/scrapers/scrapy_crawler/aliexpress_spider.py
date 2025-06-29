# src/scrapers/scrapy_crawler/aliexpress_spider.py

import scrapy
from datetime import datetime, timezone
from src.data.models import ProductData
from src.scrapers.scrapy_crawler.pipelines import save_product_to_db

class AliExpressSpider(scrapy.Spider):
    name = "aliexpress"
    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "PLAYWRIGHT_LAUNCH_OPTIONS": {"headless": True},
        "LOG_LEVEL": "INFO"
    }

    def start_requests(self):
        yield scrapy.Request(
            url="https://www.aliexpress.com/wholesale?SearchText=headphones",
            callback=self.parse,
            meta={"playwright": True}
        )

    def parse(self, response):
        self.logger.info("✅ Page loaded successfully")

        # Dump HTML for verification (optional)
        with open("aliexpress_debug_final.html", "w", encoding="utf-8") as f:
            f.write(response.text)

        items = response.css("div.multi--container--1UZxx")
        self.logger.info(f"📦 Found {len(items)} items")

        for item in items[:5]:
            try:
                title = item.css("h1.multi--titleText--nXeOv3X::text").get()
                price = item.css("div.multi--price-sale--U-S0jtj span::text").get()
                url = item.css("a::attr(href)").get()

                if title and price and url:
                    product = ProductData(
                        title=title.strip(),
                        price=price.strip().replace("$", ""),
                        url=response.urljoin(url),
                        source="AliExpress",
                        timestamp=datetime.now(timezone.utc)
                    )
                    save_product_to_db(product)
                    self.logger.info(f"✅ Saved: {product.title} - {product.price}")
                else:
                    self.logger.warning("⚠️ Missing data; skipping product.")

            except Exception as e:
                self.logger.warning(f"❌ Error parsing product: {e}")

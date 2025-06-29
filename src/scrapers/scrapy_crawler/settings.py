# src/scrapers/scrapy_crawler/settings.py

BOT_NAME = "scrapy_crawler"

SPIDER_MODULES = ["src.scrapers.scrapy_crawler.spiders"]
NEWSPIDER_MODULE = "src.scrapers.scrapy_crawler.spiders"

# Be polite
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 1            # 1 second delay between requests
CONCURRENT_REQUESTS = 4       # tweak as needed

# Pipelines
ITEM_PIPELINES = {
    "src.scrapers.scrapy_crawler.pipelines.JsonWriterPipeline": 300,
}

# Export encoding
FEED_EXPORT_ENCODING = "utf-8"

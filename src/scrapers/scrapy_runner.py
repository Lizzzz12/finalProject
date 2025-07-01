from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from src.scrapers.scrapy_crawler.quotes_spider import QuotesSpider

def run_scrapy_spider():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "data_output/raw/quotes.json": {"format": "json"},
        },
        "LOG_ENABLED": False,
    })

    process.crawl(QuotesSpider)
    process.start()

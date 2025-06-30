import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from typing import Dict, Any

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    def __init__(self, urls=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls or [
            'https://www.amazon.com/s?k=laptop'
        ]

    def parse(self, response):
        for product in response.css('div.s-result-item'):
            yield {
                'product_name': product.css('h2 a span::text').get(),
                'price': product.css('span.a-price-whole::text').get(),
                'currency': 'USD',
                'source': 'amazon',
                'url': response.urljoin(product.css('h2 a::attr(href)').get())
            }

        next_page = response.css('a.s-pagination-next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

def run_spider(urls=None):
    process = CrawlerProcess(get_project_settings())
    process.crawl(AmazonSpider, urls=urls)
    process.start()
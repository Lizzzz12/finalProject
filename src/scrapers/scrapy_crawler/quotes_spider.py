import scrapy
from src.data.database import insert_item

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css("div.quote"):
            title = quote.css("span.text::text").get().strip()
            insert_item(title, "N/A")

        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

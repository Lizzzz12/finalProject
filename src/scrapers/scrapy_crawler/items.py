# items.py
import scrapy

class ProductItem(scrapy.Item):
    site  = scrapy.Field()
    url   = scrapy.Field()
    name  = scrapy.Field()
    price = scrapy.Field()

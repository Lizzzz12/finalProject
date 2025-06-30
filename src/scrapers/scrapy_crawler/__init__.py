"""
Scrapy-based web crawler implementation.

Contains:
- spider.py: Amazon product spider implementation
"""

from .spider import AmazonSpider, run_spider

__all__ = ['AmazonSpider', 'run_spider']
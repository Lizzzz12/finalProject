"""
Web scraping components for the price monitoring system.

Includes:
- base_scraper.py: Abstract base class for all scrapers
- static_scraper.py: BeautifulSoup-based scrapers
- selenium_scraper.py: Browser automation scrapers
- scrapy_crawler/: Scrapy-based spider implementation
"""

from .base_scraper import BaseScraper
from .static_scraper import StaticScraper
from .selenium_scraper import SeleniumScraper

__all__ = ['BaseScraper', 'StaticScraper', 'SeleniumScraper']
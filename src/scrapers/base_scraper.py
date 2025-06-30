<<<<<<< HEAD
class BaseScraper:
    def fetch(self, url):
        raise NotImplementedError

    def parse(self, content):
        raise NotImplementedError
=======
# # src/scrapers/base_scraper.py - Member 1's work
# """
# Base scraper class providing common functionality for all scrapers
# """
# import requests
# from bs4 import BeautifulSoup
# from selenium import webdriver
# from urllib.parse import urlparse
# import time
# import random
# from typing import Optional, Dict, List
# import logging
#
#
# class BaseScraper:
#     """Base class for all scrapers implementing common functionality"""
#
#     def __init__(self, config: dict):
#         """Initialize with configuration"""
#         self.config = config
#         self.logger = logging.getLogger(__name__)
#         self.headers = {
#             'User-Agent': self._get_random_user_agent(),
#             'Accept-Language': 'en-US,en;q=0.5'
#         }
#         self.session = requests.Session()
#         self.session.headers.update(self.headers)
#
#     def _get_random_user_agent(self) -> str:
#         """Return a random user agent from configuration"""
#         return random.choice(self.config['user_agents'])
#
#     def _delay_request(self):
#         """Implement polite delay between requests"""
#         delay = random.uniform(*self.config['request_delay_range'])
#         time.sleep(delay)
#
#     def _get_page_static(self, url: str) -> Optional[BeautifulSoup]:
#         """Fetch page content using requests and BeautifulSoup"""
#         try:
#             self._delay_request()
#             response = self.session.get(url)
#             response.raise_for_status()
#             return BeautifulSoup(response.text, 'html.parser')
#         except Exception as e:
#             self.logger.error(f"Error fetching {url}: {str(e)}")
#             return None
#
#     def _get_page_dynamic(self, url: str) -> Optional[webdriver.Chrome]:
#         """Fetch page content using Selenium for dynamic content"""
#         try:
#             options = webdriver.ChromeOptions()
#             options.add_argument('--headless')
#             options.add_argument(f'user-agent={self._get_random_user_agent()}')
#             driver = webdriver.Chrome(options=options)
#             driver.get(url)
#             return driver
#         except Exception as e:
#             self.logger.error(f"Error with Selenium on {url}: {str(e)}")
#             return None
#
#     def scrape(self, url: str) -> Dict:
#         """Base scrape method to be implemented by child classes"""
#         raise NotImplementedError("Subclasses must implement this method")
>>>>>>> f0ba75326657d2188e7194689ed6a139e5d23b19

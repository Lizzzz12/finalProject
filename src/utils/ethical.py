# final-project/src/utils/ethical.py
import requests
from urllib.parse import urlparse
import time
import logging


class EthicalScraper:
    """Handles ethical scraping compliance"""

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.last_request_time = 0

    def check_robots_txt(self, url):
        """Check robots.txt for scraping permissions"""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        try:
            response = requests.get(robots_url, timeout=5)
            if response.status_code == 200:
                return self._parse_robots_txt(response.text)
            return True  # Assume allowed if no robots.txt
        except Exception:
            return True  # Assume allowed if can't check

    def _parse_robots_txt(self, content):
        """Parse robots.txt content"""
        # Simplified parsing - in reality would need full parser
        return "User-agent: *\nDisallow: /" not in content

    def enforce_delay(self):
        """Enforce delay between requests"""
        elapsed = time.time() - self.last_request_time
        required_delay = self.config.get('min_delay', 1)

        if elapsed < required_delay:
            delay = required_delay - elapsed
            time.sleep(delay)

        self.last_request_time = time.time()

    def validate_scraping(self, url):
        """Validate if scraping is allowed"""
        if not self.check_robots_txt(url):
            self.logger.warning(f"Scraping may be disallowed by robots.txt for {url}")
            return False

        self.enforce_delay()
        return True
import pytest
from src.scrapers.amazon_scraper import AmazonScraper
from unittest.mock import patch


@pytest.fixture
def scraper():
    return AmazonScraper(config={'min_delay': 0, 'max_delay': 0})


def test_extract_product_id(scraper):
    test_urls = [
        ('https://www.amazon.com/dp/B08N5KWB9H', 'B08N5KWB9H'),
        ('https://www.amazon.com/gp/product/B08N5KWB9H', 'B08N5KWB9H'),
        ('invalid_url', None)
    ]

    for url, expected in test_urls:
        assert scraper._extract_product_id(url) == expected
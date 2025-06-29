# src/scrapers/static_scraper.py

import requests
from bs4 import BeautifulSoup
import random
from datetime import datetime, timezone
from src.utils.logger import logger
from src.data.models import ProductData
from src.data.database import create_table, save_product

HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
]

def get_amazon_price(url):
    headers = random.choice(HEADERS_LIST)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            logger.warning(f"Failed request for {url}: {response.status_code}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')

        # Dump raw HTML for inspection
        with open("amazon_debug.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        # Extract title
        title_tag = soup.find(id='productTitle')
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        # Try to extract combined price (whole + fraction)
        whole = soup.find('span', {'class': 'a-price-whole'})
        fraction = soup.find('span', {'class': 'a-price-fraction'})
        if whole and fraction:
            whole_clean = whole.get_text(strip=True).replace('.', '')
            fraction_clean = fraction.get_text(strip=True)
            price_text = f"{whole_clean}.{fraction_clean}"
        else:
            # Fallback options
            price = (
                soup.find('span', {'class': 'a-offscreen'}) or
                soup.find('span', {'id': 'priceblock_ourprice'}) or
                soup.find('span', {'id': 'priceblock_dealprice'}) or
                soup.find('span', {'class': 'a-price'})
            )
            price_text = price.get_text(strip=True).replace("..", ".") if price else "N/A"

        return {
            'title': title,
            'price': price_text,
            'url': url
        }

    except Exception as e:
        logger.error(f"Error scraping Amazon URL {url}: {e}")
        return None

if __name__ == "__main__":
    test_url = "https://www.amazon.com/dp/B0BVZ7LS9N"  # Replace with any valid Amazon product URL
    create_table()
    result = get_amazon_price(test_url)
    if result:
        logger.info(f"Scraped: {result}")
        product = ProductData(
            title=result['title'],
            price=result['price'],
            url=result['url'],
            source="Amazon",
            timestamp=datetime.now(timezone.utc)
        )
        save_product(product)

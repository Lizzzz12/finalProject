# src/scrapers/static_scraper.py

import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def fetch_static(url: str, timeout: int = 10, max_retries: int = 3) -> str:
    """
    Download the raw HTML of `url`.
    - Rotate user-agent each try.
    - Retry up to `max_retries` on network errors.
    Returns the page HTML as a string.
    """
    ua = UserAgent()
    for attempt in range(1, max_retries + 1):
        try:
            headers = {"User-Agent": ua.random}
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"[fetch_static] attempt {attempt} failed: {e}")
            time.sleep(1 * attempt)  # simple backoff
    raise RuntimeError(f"fetch_static: all {max_retries} attempts failed for {url}")

def parse_product_page_amazon(html: str) -> dict:
    """
    Given an Amazon product page HTML, extract:
      - name: product title
      - price: current price as string (e.g. "$19.99")
    TODO: adjust the CSS selectors if Amazon changes its markup.
    """
    soup = BeautifulSoup(html, "lxml")

    # 1) Find the product title
    title_tag = soup.select_one("#productTitle")
    name = title_tag.get_text(strip=True) if title_tag else None

    # 2) Find the price
    price_tag = soup.select_one(".a-price .a-offscreen")
    price = price_tag.get_text(strip=True) if price_tag else None

    return {
        "name": name,
        "price": price,
    }

def parse_product_page_ebay(html: str) -> dict:
    """
    Given an eBay product page HTML, extract name & price.
    TODO: replace selectors with the ones you discover via browser devtools.
    """
    soup = BeautifulSoup(html, "lxml")

    name_tag = soup.select_one("#itemTitle")
    name = name_tag.get_text(strip=True).replace("Details about  \xa0", "") if name_tag else None

    price_tag = soup.select_one("span#prcIsum, span#mm-saleDscPrc")
    price = price_tag.get_text(strip=True) if price_tag else None

    return {
        "name": name,
        "price": price,
    }

# Example usage (you can remove or move this into a test module later):
if __name__ == "__main__":
    url = "https://www.amazon.com/dp/B08N5WRWNW"
    html = fetch_static(url)
    data = parse_product_page_amazon(html)
    print("Amazon product:", data)

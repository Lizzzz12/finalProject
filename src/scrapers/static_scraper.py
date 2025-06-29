# src/scrapers/static_scraper.py

import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

def fetch_static(url: str, timeout: int = 10, max_retries: int = 3) -> str:
    """
    Download the raw HTML of `url`.
    - Rotate user-agent each try.
    - Retry on failures up to max_retries.
    Returns page HTML as text.
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
            time.sleep(1 * attempt)
    raise RuntimeError(f"fetch_static: all {max_retries} attempts failed for {url}")

def parse_product_page_amazon(html: str) -> dict:
    """
    Parse Amazon product HTML for:
      - name (from #productTitle)
      - price (from .a-price .a-offscreen)
    """
    soup = BeautifulSoup(html, "lxml")

    # Title
    title_tag = soup.select_one("#productTitle")
    name = title_tag.get_text(strip=True) if title_tag else None

    # Price
    price_tag = soup.select_one(".a-price .a-offscreen")
    price = price_tag.get_text(strip=True) if price_tag else None

    return {"site": "amazon", "name": name, "price": price}


def parse_product_page_ebay(html: str) -> dict:
    """
    Parse eBay product HTML for:
      - name (from #itemTitle)
      - price (from #prcIsum or #mm-saleDscPrc)
    """
    soup = BeautifulSoup(html, "lxml")

    # Title (strip the "Details about  " prefix)
    name_tag = soup.select_one("#itemTitle")
    raw = name_tag.get_text(strip=True) if name_tag else ""
    name = raw.replace("Details about", "").strip() or None

    # Price
    price_tag = soup.select_one("span#prcIsum, span#mm-saleDscPrc")
    price = price_tag.get_text(strip=True) if price_tag else None

    return {"site": "ebay", "name": name, "price": price}


def parse_product_page_aliexpress(html: str) -> dict:
    """
    Parse AliExpress product HTML for:
      - name (example selector: h1.product-title-text)
      - price (example selector: span.product-price-value)
    YOU WILL NEED TO INSPECT YOUR aliexpress_debug.html AND ADJUST THESE!
    """
    soup = BeautifulSoup(html, "lxml")

    # TODO: open aliexpress_debug.html in your browser, find the right CSS selectors
    name_tag = soup.select_one("h1.product-title-text")
    name = name_tag.get_text(strip=True) if name_tag else None

    price_tag = soup.select_one("span.product-price-value")
    price = price_tag.get_text(strip=True) if price_tag else None

    return {"site": "aliexpress", "name": name, "price": price}


if __name__ == "__main__":
    # Path to your debug HTML files
    base = os.path.abspath(os.path.dirname(__file__) + "/../../")
    tests = [
        ("amazon_debug.html", parse_product_page_amazon),
        ("aliexpress_debug.html", parse_product_page_aliexpress),
    ]

    for filename, parser in tests:
        path = os.path.join(base, filename)
        print(f"\n=== Testing {filename} ===")
        try:
            html = open(path, encoding="utf-8").read()
            result = parser(html)
            print(result)
        except FileNotFoundError:
            print(f"❌ {filename} not found at {path}")
        except Exception as e:
            print(f"❌ Error parsing {filename}: {e}")

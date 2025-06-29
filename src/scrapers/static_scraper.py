# src/scrapers/static_scraper.py

import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os

def fetch_static(url: str, timeout: int = 10, max_retries: int = 3) -> str:
    ua = UserAgent()
    for attempt in range(1, max_retries + 1):
        try:
            headers = {"User-Agent": ua.random}
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"[fetch_static] attempt {attempt} failed: {e}")
            time.sleep(attempt)
    raise RuntimeError(f"fetch_static: failed after {max_retries} tries for {url}")

def parse_product_page_amazon(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # Title
    title_tag = soup.select_one("#productTitle")
    name = title_tag.get_text(strip=True) if title_tag else None

    # Price fallbacks
    price_tag = (
        soup.select_one("#priceblock_ourprice")
        or soup.select_one("#priceblock_dealprice")
        or soup.select_one("#price_inside_buybox")
        or soup.select_one(".a-price .a-offscreen")
    )
    price = price_tag.get_text(strip=True) if price_tag else None

    return {"site": "amazon", "name": name, "price": price}

def parse_product_page_aliexpress(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")

    # 🔧 **Step 1: open aliexpress_debug.html in your browser, inspect these elements,**
    # then replace the selectors below with the **actual** ones you see.
    name_tag  = soup.select_one("REPLACE_WITH_TITLE_SELECTOR")
    price_tag = soup.select_one("REPLACE_WITH_PRICE_SELECTOR")

    name  = name_tag.get_text(strip=True) if name_tag else None
    price = price_tag.get_text(strip=True) if price_tag else None

    return {"site": "aliexpress", "name": name, "price": price}

if __name__ == "__main__":
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    tests = [
        ("amazon_debug.html",     parse_product_page_amazon),
        ("aliexpress_debug.html", parse_product_page_aliexpress),
    ]

    for filename, parser in tests:
        path = os.path.join(base, filename)
        print(f"\n=== Testing {filename} ===")
        try:
            html = open(path, encoding="utf-8").read()
            print(parser(html))
        except FileNotFoundError:
            print(f"❌ {filename} not found at {path}")
        except Exception as e:
            print(f"❌ Error parsing {filename}: {e}")

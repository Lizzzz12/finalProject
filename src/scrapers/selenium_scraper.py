# src/scrapers/selenium_scraper.py

import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def fetch_dynamic(
    url: str,
    headless: bool = True,
    wait_time: int = 3,
    do_scroll: bool = False
) -> str:
    opts = Options()
    if headless:
        opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    try:
        driver.get(url)
        time.sleep(wait_time)
        if do_scroll:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_time)
        return driver.page_source
    finally:
        driver.quit()

def parse_product_page_dynamic(html: str) -> dict:
    soup = BeautifulSoup(html, "lxml")
    title_tag = soup.select_one("#productTitle")
    name = title_tag.get_text(strip=True) if title_tag else None

    price_tag = (
        soup.select_one("#priceblock_ourprice")
        or soup.select_one("#priceblock_dealprice")
        or soup.select_one("#price_inside_buybox")
        or soup.select_one(".a-price .a-offscreen")
    )
    price = price_tag.get_text(strip=True) if price_tag else None

    return {"site": "dynamic", "name": name, "price": price}

if __name__ == "__main__":
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

    # Offline test against your saved HTML
    debug_file = os.path.join(base, "amazon_debug.html")
    if os.path.exists(debug_file):
        html = open(debug_file, encoding="utf-8").read()
        print("\n=== Offline dynamic parse ===")
        print(parse_product_page_dynamic(html))
    else:
        print(f"❌ {debug_file} not found")

    # **Live** fetch test (optional—may get blocked by Amazon)
    url = "https://www.amazon.com/dp/B08N5WRWNW"
    print("\n=== Live dynamic fetch ===")
    html_live = fetch_dynamic(url, headless=True, wait_time=5)
    print(parse_product_page_dynamic(html_live))

# -------------------- Final Main Script with Reporting, Record Count, and Cleaning --------------------

from src.scrapers.static_scraper import StaticScraper
from src.scrapers.selenium_scraper import SeleniumScraper
from src.scrapers.amazon_scraper import AmazonScraper
from src.scrapers.scrapy_crawler.newegg_spider import NeweggSeleniumScraper
from src.data.models import create_tables
from src.utils.logger import logger
from src.data.database import count_items, get_all_items
import pandas as pd

import os

if __name__ == "__main__":
    logger.info("Creating database tables...")
    create_tables()

    logger.info("Running static scraper...")
    static_scraper = StaticScraper()
    static_data = static_scraper.run()
    for title in static_data:
        static_scraper.save_to_db(title)

    logger.info("Running Selenium eBay scraper...")
    ebay_scraper = SeleniumScraper()
    ebay_scraper.run()

    logger.info("Running Amazon scraper...")
    amazon_scraper = AmazonScraper()
    amazon_scraper.run()

    logger.info("Running Newegg Selenium scraper...")
    newegg_scraper = NeweggSeleniumScraper()
    newegg_scraper.run()

    # -------------------- Clean and Report --------------------
    logger.info("Cleaning data and generating report...")
    items = get_all_items()
    df = pd.DataFrame(items, columns=["id", "title"])
    df.drop_duplicates(subset="title", inplace=True)
    df = df[df["title"].str.strip().astype(bool)]  # remove blank titles

    cleaned_count = len(df)
    df.to_csv("data_output/reports/item_summary.csv", index=False)

    print(f"\n✅ Final Report")
    print(f"Unique, cleaned items: {cleaned_count}")
    print("Saved: data_output/reports/item_summary.csv")
    logger.info(f"Final cleaned item count: {cleaned_count}")
# 3520
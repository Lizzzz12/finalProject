# -------------------- main.py (FINAL VERSION) --------------------
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from src.scrapers.static_scraper import StaticScraper
from src.scrapers.selenium_scraper import SeleniumScraper
from src.scrapers.amazon_scraper import AmazonScraper
from src.scrapers.scrapy_crawler.newegg_spider import NeweggSeleniumScraper
from src.scrapers.scrapy_runner import run_scrapy_spider
from src.data.models import create_tables
from src.utils.logger import logger
from src.data.database import count_items, get_all_items


def run_all_scrapers():
    logger.info("Creating database tables...")
    create_tables()

    logger.info("Running Amazon scraper...")
    amazon_scraper = AmazonScraper()
    amazon_scraper.run()

    logger.info("Running eBay scraper...")
    ebay_scraper = SeleniumScraper()
    ebay_scraper.run()

    logger.info("Running Newegg scraper...")
    newegg_scraper = NeweggSeleniumScraper()
    newegg_scraper.run()

    logger.info("Running Scrapy spider (QuotesToScrape)...")
    run_scrapy_spider()


def generate_report(sort_by=None):
    logger.info("Generating final report...")

    items = get_all_items()
    df = pd.DataFrame(items, columns=["id", "title", "price"])

    # Clean data
    df.drop_duplicates(subset="title", inplace=True)
    df = df[df["title"].str.strip().astype(bool)]

    # Optional: sort by price
    if sort_by == "price":
        df["clean_price"] = df["price"].str.replace("$", "").str.replace(",", "")
        df["clean_price"] = pd.to_numeric(df["clean_price"], errors="coerce")
        df = df.sort_values(by="clean_price", ascending=False)

    # Create reports directory
    os.makedirs("data_output/reports", exist_ok=True)

    # Save CSV
    csv_path = "data_output/reports/item_summary.csv"
    df.to_csv(csv_path, index=False)

    # Save JSON
    json_path = "data_output/raw/item_summary.json"
    df.to_json(json_path, orient="records", indent=2)

    # Generate price chart (top 10)
    clean_df = df[df["price"] != "N/A"].copy()
    clean_df["price_val"] = clean_df["price"].str.replace("$", "").str.replace(",", "")
    clean_df["price_val"] = pd.to_numeric(clean_df["price_val"], errors="coerce")
    top_prices = clean_df.nlargest(10, "price_val")

    plt.figure(figsize=(10, 6))
    plt.barh(top_prices["title"], top_prices["price_val"])
    plt.xlabel("Price ($)")
    plt.title("Top 10 Most Expensive Items")
    plt.tight_layout()
    plt.savefig("data_output/reports/top_10_prices.png")

    print("\n✅ Final Report")
    print(f"Total cleaned, unique items: {len(df)}")
    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")
    logger.info(f"Final cleaned item count: {len(df)}")


def main():
    parser = argparse.ArgumentParser(description="Data Scraping Final Project")
    parser.add_argument("--scrape", action="store_true", help="Run all scrapers")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--sort", choices=["price"], help="Sort report by column")

    args = parser.parse_args()

    if args.scrape:
        run_all_scrapers()
    if args.report:
        generate_report(sort_by=args.sort)
    if not args.scrape and not args.report:
        parser.print_help()


if __name__ == "__main__":
    main()

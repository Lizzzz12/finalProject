# final-project/src/cli/commands.py
import click
from typing import List
from concurrent.futures import ThreadPoolExecutor
from ..scrapers import AmazonScraper, EbayScraper
from ..data.database import DatabaseManager
from ..data.processors import DataProcessor
from ..analysis.trends import PriceAnalyzer
from ..analysis.reports import ReportGenerator
import logging


@click.group()
def cli():
    """E-Commerce Price Monitoring System CLI"""
    pass


@cli.command()
@click.argument('search_term')
@click.option('--limit', default=5, help='Maximum results per platform')
def search(search_term: str, limit: int):
    """Search for products across all platforms"""
    logger = logging.getLogger(__name__)
    db = DatabaseManager()
    processor = DataProcessor()

    scrapers = [
        AmazonScraper(config={'min_delay': 1, 'max_delay': 3}),
        EbayScraper(config={'min_delay': 1, 'max_delay': 3})
    ]

    def search_with_scraper(scraper):
        try:
            results = scraper.search_products(search_term, limit)
            for product in results:
                cleaned = processor.clean_product_data(product.__dict__)
                db.add_product(cleaned)
                db.add_price_record(cleaned['product_id'], cleaned['price'], cleaned['currency'])
            return results
        except Exception as e:
            logger.error(f"Error with {scraper.source_website}: {e}")
            return []

    with ThreadPoolExecutor() as executor:
        all_results = list(executor.map(search_with_scraper, scrapers))

    # Display results
    for i, scraper_results in enumerate(all_results):
        click.echo(f"\nResults from {scrapers[i].source_website}:")
        for result in scraper_results:
            click.echo(f"- {result.name} @ {result.price} {result.currency} (ID: {result.product_id})")


@cli.command()
@click.argument('product_id')
def track(product_id: str):
    """Track price history for a product"""
    db = DatabaseManager()
    analyzer = PriceAnalyzer(db)
    report_gen = ReportGenerator()

    # Get product info
    product = db.get_product(product_id)
    if not product:
        click.echo(f"Product {product_id} not found in database")
        return

    # Get price history
    price_history = analyzer.get_price_history_dataframe(product_id)
    if price_history.empty:
        click.echo("No price history available for this product")
        return

    # Generate report
    report_path = report_gen.generate_product_report(product, price_history)
    if report_path:
        click.echo(f"Report generated: {report_path}")
    else:
        click.echo("Failed to generate report")


@cli.command()
@click.argument('product_url')
def add(product_url: str):
    """Add a new product to track by URL"""
    db = DatabaseManager()
    processor = DataProcessor()

    # Determine which scraper to use based on URL
    if 'amazon.com' in product_url:
        scraper = AmazonScraper(config={'min_delay': 1, 'max_delay': 3})
    elif 'ebay.com' in product_url:
        scraper = EbayScraper(config={'min_delay': 1, 'max_delay': 3})
    else:
        click.echo("Unsupported website. Currently supports Amazon and eBay.")
        return

    # Scrape product data
    product_data = scraper.scrape_product(product_url)
    if not product_data:
        click.echo("Failed to scrape product information")
        return

    # Clean and store data
    cleaned = processor.clean_product_data(product_data.__dict__)
    db.add_product(cleaned)
    db.add_price_record(cleaned['product_id'], cleaned['price'], cleaned['currency'])

    click.echo(f"Added product: {cleaned['name']} (ID: {cleaned['product_id']})")
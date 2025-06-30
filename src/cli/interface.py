import click
from ..data.database import DatabaseManager
from ..analysis.trends import PriceAnalyzer


@click.group()
def main_menu():
    """E-Commerce Price Monitoring System CLI"""
    pass


@main_menu.command()
@click.argument('search_term')
def search(search_term):
    """Search for products across all platforms"""
    click.echo(f"Searching for: {search_term}")
    # Implementation here


@main_menu.command()
@click.argument('product_id')
def track(product_id):
    """Track price history for a product"""
    db = DatabaseManager()
    analyzer = PriceAnalyzer(db)
    analysis = analyzer.analyze_price_trends(product_id)

    if analysis:
        click.echo(f"Price analysis for {analysis['product_name']}:")
        click.echo(f"Current price: {analysis['current_price']} {analysis['currency']}")
        click.echo(f"30-day change: {analysis['price_change_30d']:.2f}%")
    else:
        click.echo("Product not found")
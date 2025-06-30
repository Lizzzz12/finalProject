# final-project/src/data/processors.py
import re
from datetime import datetime
from typing import Dict, Any
import logging


class DataProcessor:
    """Handles data cleaning and transformation"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def clean_product_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and standardize scraped product data"""
        try:
            cleaned = {
                'product_id': self._clean_text(raw_data.get('product_id', '')),
                'name': self._clean_text(raw_data.get('name', '')),
                'price': self._clean_price(raw_data.get('price', 0)),
                'currency': self._clean_currency(raw_data.get('currency', 'USD')),
                'url': raw_data.get('url', '').strip(),
                'description': self._clean_text(raw_data.get('description', '')),
                'category': self._clean_text(raw_data.get('category', '')),
                'availability': self._clean_availability(raw_data.get('availability', '')),
                'source_website': raw_data.get('source_website', ''),
                'timestamp': datetime.now().isoformat()
            }
            return cleaned
        except Exception as e:
            self.logger.error(f"Error cleaning product data: {e}")
            return {}

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if not text:
            return ''

        # Remove extra whitespace and special characters
        text = re.sub(r'\s+', ' ', text).strip()
        text = re.sub(r'[^\w\s\-.,;:!?()\'"$%&@#]', '', text)
        return text

    def _clean_price(self, price) -> float:
        """Convert price to standardized float"""
        try:
            if isinstance(price, str):
                # Remove currency symbols and thousands separators
                price = re.sub(r'[^\d.]', '', price)
            return float(price)
        except (ValueError, TypeError):
            return 0.0

    def _clean_currency(self, currency: str) -> str:
        """Standardize currency format"""
        currency = currency.upper() if currency else 'USD'
        if len(currency) > 3:
            # Extract currency symbol if present in text
            match = re.search(r'([$€£¥]|\bUSD\b|\bEUR\b|\bGBP\b|\bJPY\b)', currency)
            if match:
                symbol = match.group(1)
                if symbol == '$':
                    return 'USD'
                elif symbol == '€':
                    return 'EUR'
                elif symbol == '£':
                    return 'GBP'
                elif symbol == '¥':
                    return 'JPY'
                return symbol
            return 'USD'
        return currency if currency in {'USD', 'EUR', 'GBP', 'JPY'} else 'USD'

    def _clean_availability(self, availability: str) -> str:
        """Standardize availability status"""
        if not availability:
            return 'Unknown'

        availability = availability.lower()
        if 'stock' in availability:
            return 'In Stock'
        elif 'out' in availability and 'stock' in availability:
            return 'Out of Stock'
        elif 'pre-order' in availability:
            return 'Pre-Order'
        elif 'backorder' in availability:
            return 'Backordered'
        elif 'available' in availability:
            return 'Available'
        elif 'unavailable' in availability:
            return 'Unavailable'
        return availability.capitalize()
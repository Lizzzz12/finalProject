# src/data/models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ProductData:
    title: str
    price: str
    url: str
    source: str  # e.g., 'Amazon', 'eBay'
    timestamp: datetime

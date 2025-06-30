"""
Command-line interface package.

Contains:
- interface.py: Main CLI application
- commands.py: Additional command implementations
"""

from .interface import main
from .commands import scrapy

__all__ = ['main', 'scrapy']
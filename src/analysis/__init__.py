"""
Data analysis and reporting components.

Includes:
- statistics.py: Price analysis calculations
- trends.py: Visualization generation
- reports.py: HTML report generation
"""

from .statistics import PriceAnalyzer
from .trends import TrendAnalyzer
from .reports import ReportGenerator

__all__ = ['PriceAnalyzer', 'TrendAnalyzer', 'ReportGenerator']
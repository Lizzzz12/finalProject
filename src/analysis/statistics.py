import pandas as pd
from typing import List, Dict, Any
from datetime import datetime, timedelta


class PriceAnalyzer:
    @staticmethod
    def calculate_price_stats(products: List[Dict[str, Any]]) -> Dict[str, Any]:
        df = pd.DataFrame(products)
        if df.empty:
            return {}

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        stats = {
            'current_price': df['price'].iloc[-1],
            'average_price': df['price'].mean(),
            'min_price': df['price'].min(),
            'max_price': df['price'].max(),
            'price_change_7d': PriceAnalyzer._calculate_price_change(df, days=7),
            'price_change_30d': PriceAnalyzer._calculate_price_change(df, days=30),
            'total_observations': len(df)
        }

        return stats

    @staticmethod
    def _calculate_price_change(df: pd.DataFrame, days: int) -> float:
        cutoff = datetime.now() - timedelta(days=days)
        recent = df[df['timestamp'] >= cutoff]
        if len(recent) < 2:
            return 0.0

        old_avg = recent['price'].iloc[:len(recent) // 2].mean()
        new_avg = recent['price'].iloc[len(recent) // 2:].mean()

        if old_avg == 0:
            return 0.0

        return ((new_avg - old_avg) / old_avg) * 100
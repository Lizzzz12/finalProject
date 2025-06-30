import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from io import BytesIO
import base64


class TrendAnalyzer:
    @staticmethod
    def generate_price_trend_chart(products: List[Dict[str, Any]], product_name: str):
        df = pd.DataFrame(products)
        if df.empty:
            return None

        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')

        plt.figure(figsize=(10, 6))
        plt.plot(df['timestamp'], df['price'], marker='o')
        plt.title(f'Price Trend: {product_name}')
        plt.xlabel('Date')
        plt.ylabel('Price ($)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()

        return base64.b64encode(buffer.read()).decode('utf-8')
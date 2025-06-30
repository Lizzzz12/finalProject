# final-project/src/analysis/reports.py
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Environment, FileSystemLoader
import os
from pathlib import Path
from typing import Dict, List
import logging


class ReportGenerator:
    """Generates HTML reports with visualizations"""

    def __init__(self, output_dir: str = None):
        self.logger = logging.getLogger(__name__)
        self.output_dir = output_dir or os.path.join(Path(__file__).parent.parent.parent, 'data_output/reports')
        os.makedirs(self.output_dir, exist_ok=True)

        # Set up Jinja2 template environment
        template_dir = os.path.join(Path(__file__).parent.parent.parent, 'docs/templates')
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate_product_report(self, product_data: Dict, price_history: pd.DataFrame) -> str:
        """Generate a comprehensive product report"""
        try:
            # Create visualizations
            chart_path = self._create_price_chart(price_history, product_data['product_id'])

            # Prepare data for template
            context = {
                'product': product_data,
                'stats': self._calculate_stats(price_history),
                'chart_path': os.path.basename(chart_path),
                'price_history': price_history.to_dict('records'),
                'generated_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')
            }

            # Render HTML template
            template = self.env.get_template('product_report.html')
            html_content = template.render(context)

            # Save report
            report_path = os.path.join(self.output_dir, f"product_{product_data['product_id']}.html")
            with open(report_path, 'w') as f:
                f.write(html_content)

            return report_path
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            return None

    def _create_price_chart(self, df: pd.DataFrame, product_id: str) -> str:
        """Create price trend visualization"""
        plt.figure(figsize=(10, 6))
        sns.set_style("whitegrid")

        # Plot price history
        ax = sns.lineplot(x='timestamp', y='price', data=df, marker='o')

        # Format plot
        ax.set_title(f"Price History for Product {product_id}")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot
        chart_path = os.path.join(self.output_dir, f"price_chart_{product_id}.png")
        plt.savefig(chart_path)
        plt.close()

        return chart_path

    def _calculate_stats(self, df: pd.DataFrame) -> Dict:
        """Calculate statistics for the report"""
        if df.empty:
            return {}

        return {
            'current_price': df['price'].iloc[-1],
            'min_price': df['price'].min(),
            'max_price': df['price'].max(),
            'avg_price': df['price'].mean(),
            'price_change': df['price'].iloc[-1] - df['price'].iloc[0],
            'price_change_pct': ((df['price'].iloc[-1] - df['price'].iloc[0]) / df['price'].iloc[0]) * 100,
            'days_tracked': len(df),
            'first_date': df['timestamp'].iloc[0].strftime('%Y-%m-%d'),
            'last_date': df['timestamp'].iloc[-1].strftime('%Y-%m-%d')
        }
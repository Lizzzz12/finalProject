````markdown
# Multi-Source E-Commerce Scraper

Monitor and analyze product prices across Amazon, eBay, and Newegg using Python-based scraping tools.

## ?? Features

- Static and dynamic scraping (BeautifulSoup + Selenium)
- Scrapy spider integration
- SQLite database for storage
- Pandas-based data cleaning
- Matplotlib chart generation

## ?? Setup Instructions

1. **Clone the Repo**

```bash
git clone https://github.com/your-username/final-project.git
cd final-project
```
````

2. **Create a Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Run Scrapers**

```bash
python main.py --scrape
```

5. **Generate Report**

```bash
python main.py --report
```

## ?? Output

- `data_output/db.sqlite` � raw data
- `data_output/reports/item_summary.csv` � cleaned summary
- `data_output/reports/top_10_prices.png` � price chart

## ?? Contributors

See [CONTRIBUTIONS.md](CONTRIBUTIONS.md)

````

---

## ARCHITECTURE.md

```markdown
# System Architecture Overview

## Overview
The scraper system is designed using modular components for scraping, processing, and reporting price data from multiple e-commerce platforms.

## Components

### Scraper Layer
- `AmazonScraper`: Uses requests + BeautifulSoup
- `SeleniumScraper`: Dynamic scraping of eBay using Selenium
- `NeweggSeleniumScraper`: Uses headless browser automation
- `QuotesSpider`: Scrapy-based spider to validate framework requirement

### Data Layer
- SQLite database in `data_output/db.sqlite`
- Table: `items(id INTEGER, title TEXT, price TEXT)`

### Utility Layer
- Logger outputs to `logs/project.log`
- CLI interface using `argparse`

### Output Layer
- Report CSV via Pandas
- Price distribution chart via Matplotlib

## Design Patterns
- **Strategy**: Swappable scraper interfaces
- **Factory (CLI)**: Choose scrapers via flags

## Future Enhancements
- Add Redis queue for scheduling
- Replace SQLite with PostgreSQL
- Deploy scrapers as microservices
````

---

## CONTRIBUTIONS.md

```markdown
# Team Contributions

### ????? Lizi Sakhokia

- Project lead & coordinator
- Implemented Amazon and Newegg scrapers
- Final report generation and price chart
- CLI architecture and logger setup

### ????? Giorgi Parulava

- Developed eBay Selenium scraper
- Helped integrate database schema
- Worked on error handling and retry logic
- Contributed to project structure planning

### ????? Lasha Bregadze

- Wrote and debugged Scrapy spider
- Integrated scrapy_runner and JSON output
- Worked on architecture documentation
- Finalized README, setup guide, and Markdown formatting
```

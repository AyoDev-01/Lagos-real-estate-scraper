
# Lagos Real Estate Scraper - Save 5 Hours/Week

Automated scraper that collects property listings from PrivateProperty.ng

## Problem it solves
Real estate agents spend 5+ hours manually copying listings. This bot does it in 3 minutes.

## Features
- Scrapes 500+ listings with pagination
- Cleans price data ( ₦50M -> 50000000 )
- Anti-blocking with random delays
- Exports to CSV ready for Excel
- Timestamp for tracking

## Tech Stack
Python, Requests, BeautifulSoup, Pandas

## How to run
```bash
pip install -r requirements.txt
python scraper.py
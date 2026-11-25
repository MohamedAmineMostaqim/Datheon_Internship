# Task 1 - Web Scraper (`src/scraper.py`)

## Goal
Extract structured data from a multi-page website with BeautifulSoup and export 100+ records to CSV/JSON.

## Data source
https://books.toscrape.com - a website built for scraping practice. 50 pages x 20 books = **1000 records**.

## Fields extracted
| Field | Example | Where it comes from |
|---|---|---|
| title | A Light in the Attic | `<a title="...">` |
| price | £51.77 | `<p class="price_color">` |
| rating | Three | `<p class="star-rating Three">` |
| availability | In stock | `<p class="availability">` |
| url | https://books.toscrape.com/... | `<a href="...">` |
| page | 1 | loop counter (metadata) |
| scraped_at | 2026-10-22 09:00:00 | time of scraping (metadata) |

## How it works (step by step)
1. `run()` loops from page 1 to 50 (**pagination loop**).
2. `fetch_page(url)` downloads the page with `requests`, with a **User-Agent header** (looks like a normal browser).
3. If it fails (network error, bad status), it **retries 3 times** (`try/except` + `retries`), waiting 2 seconds between tries. If all fail it returns `None` and the page is skipped.
4. `parse_page(html)` uses BeautifulSoup to find every `<article class="product_pod">` and read the fields.
5. `save_files()` writes `data/raw/books_raw.csv` and `data/raw/books_raw.json`.
6. A `time.sleep(0.5)` between pages avoids overloading the server.

## Run
```
python -m src.scraper
```

## Output
`data/raw/books_raw.csv` and `data/raw/books_raw.json` (1000 records).

"""Task 1 - Web scraper.

Scrapes books from https://books.toscrape.com (a website made for practice)
and saves them to data/raw as CSV and JSON.
"""
import csv
import json
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

import config

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch_page(url, retries=3):
    """Download one page. Try up to `retries` times, return None if it fails."""
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()      # error if status is 404, 500...
            response.encoding = "utf-8"      # avoids a bad "£" symbol
            return response.text
        except requests.RequestException as error:
            print(f"  Attempt {attempt}/{retries} failed for {url}: {error}")
            time.sleep(2)
    return None


def parse_page(html, page_number):
    """Read the HTML of one page and return a list of books (dictionaries)."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.find_all("article", class_="product_pod"):
        link = article.h3.a
        books.append({
            "title": link["title"],
            "price": article.find("p", class_="price_color").text,          # e.g. "£51.77"
            "rating": article.find("p", class_="star-rating")["class"][1],  # e.g. "Three"
            "availability": article.find("p", class_="availability").text.strip(),
            "url": config.SITE_ROOT + link["href"],
            "page": page_number,
            "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })
    return books


def save_files(books):
    """Save the list of books to CSV and JSON."""
    config.RAW_DIR.mkdir(parents=True, exist_ok=True)

    with open(config.RAW_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=books[0].keys())
        writer.writeheader()
        writer.writerows(books)

    with open(config.RAW_JSON, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)


def run(total_pages=config.TOTAL_PAGES):
    """Scrape all pages and save the result. Returns a small stats dictionary."""
    all_books = []
    failed_pages = 0

    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}/{total_pages}...")
        html = fetch_page(config.PAGE_URL.format(page))
        if html is None:
            failed_pages += 1
            continue
        all_books.extend(parse_page(html, page))
        time.sleep(config.DELAY_SECONDS)

    if not all_books:
        raise RuntimeError("Scraper got no data. Check your internet connection.")

    save_files(all_books)
    print(f"Done: {len(all_books)} books saved in {config.RAW_DIR}")
    return {"records_scraped": len(all_books), "failed_pages": failed_pages}


if __name__ == "__main__":
    run()

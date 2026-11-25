"""Task 3 - Check that the data in PostgreSQL is correct.

Run from the project root:  python -m scripts.verify_db
"""
from sqlalchemy import create_engine, text

import config

QUERIES = {
    "Total rows": "SELECT COUNT(*) FROM books",
    "Distinct urls (must equal total rows)": "SELECT COUNT(DISTINCT url) FROM books",
    "Rows with NULL title or price (must be 0)":
        "SELECT COUNT(*) FROM books WHERE title IS NULL OR price_gbp IS NULL",
    "Min / Max / Avg price":
        "SELECT MIN(price_gbp), MAX(price_gbp), ROUND(AVG(price_gbp), 2) FROM books",
    "Books per rating":
        "SELECT rating, COUNT(*) FROM books GROUP BY rating ORDER BY rating",
    "5 most expensive books":
        "SELECT title, price_gbp FROM books ORDER BY price_gbp DESC LIMIT 5",
}

engine = create_engine(config.DATABASE_URL)
with engine.connect() as connection:
    for name, query in QUERIES.items():
        print(f"\n--- {name} ---")
        for row in connection.execute(text(query)):
            print(tuple(row))

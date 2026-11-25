"""Task 3 - Load the clean data into PostgreSQL (with upsert).

Upsert = insert the row if it is new, update it if it already exists.
"""
import pandas as pd
from sqlalchemy import create_engine, text

import config

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS books (
    url        VARCHAR(500) PRIMARY KEY,
    title      VARCHAR(500) NOT NULL,
    price_gbp  NUMERIC(8, 2) NOT NULL,
    rating     INTEGER,
    in_stock   BOOLEAN,
    page       INTEGER,
    scraped_at TIMESTAMP
)
"""

UPSERT = """
INSERT INTO books (url, title, price_gbp, rating, in_stock, page, scraped_at)
VALUES (:url, :title, :price_gbp, :rating, :in_stock, :page, :scraped_at)
ON CONFLICT (url) DO UPDATE SET
    title      = EXCLUDED.title,
    price_gbp  = EXCLUDED.price_gbp,
    rating     = EXCLUDED.rating,
    in_stock   = EXCLUDED.in_stock,
    page       = EXCLUDED.page,
    scraped_at = EXCLUDED.scraped_at
"""

COUNT = "SELECT COUNT(*) FROM books"


def run():
    df = pd.read_csv(config.CLEAN_CSV)
    records = df.to_dict(orient="records")   # list of dictionaries, one per row

    engine = create_engine(config.DATABASE_URL)

    # engine.begin() = one transaction: everything is saved, or nothing (on error)
    with engine.begin() as connection:
        connection.execute(text(CREATE_TABLE))
        before = connection.execute(text(COUNT)).scalar()
        connection.execute(text(UPSERT), records)
        after = connection.execute(text(COUNT)).scalar()

    inserted = after - before
    updated = len(records) - inserted
    print(f"Loaded {len(records)} rows: {inserted} inserted, {updated} updated.")
    return {"inserted": inserted, "updated": updated, "total_in_db": after}


if __name__ == "__main__":
    run()

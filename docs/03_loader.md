# Task 3 - PostgreSQL Loader with Upsert (`src/loader.py`)

## Goal
Load the clean data into PostgreSQL in a safe, repeatable (idempotent) way.

## Table `books`
| Column | Type | Notes |
|---|---|---|
| **url** | VARCHAR(500) | **PRIMARY KEY** |
| title | VARCHAR(500) | NOT NULL |
| price_gbp | NUMERIC(8,2) | NOT NULL |
| rating | INTEGER | |
| in_stock | BOOLEAN | |
| page | INTEGER | |
| scraped_at | TIMESTAMP | |

## How it works
1. Read `data/clean/books_clean.csv` with Pandas.
2. Connect to PostgreSQL with a **SQLAlchemy engine** (`DATABASE_URL` from `.env`).
3. `CREATE TABLE IF NOT EXISTS books (...)` **creates the table** if it doesn't exist.
4. Run an **upsert** statement (plain SQL, sent with `text()`):
   ```sql
   INSERT INTO books (...) VALUES (...)
   ON CONFLICT (url) DO UPDATE SET title = excluded.title, ...
   ```
   New book -> inserted. Existing book (same url) -> updated.
5. `engine.begin()` opens a **transaction**: if anything fails, everything is rolled back (no half-loaded data).
6. Counts rows before/after to report how many were inserted vs updated.

## Idempotency
Run the loader 2 times: the second time it **inserts 0** and **updates 1000**. The table still has 1000 rows (no duplicates).

## Run
```
python -m src.loader
python -m scripts.verify_db
```

## Verification script (`scripts/verify_db.py`)
Runs SQL queries to check the data: total rows, distinct URLs (must equal total), nulls (must be 0), min/max/avg price, books per rating, 5 most expensive books.


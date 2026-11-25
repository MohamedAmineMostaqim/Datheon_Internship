# Task 2 - Data Cleaning & Validation (`src/cleaner.py`)

## Goal
Turn the raw scraped file into clean, typed, production-ready data and produce a validation report.

## Input / Output
- Input: `data/raw/books_raw.csv`
- Output: `data/clean/books_clean.csv` and `logs/validation_report.txt`

## What the raw data looks like (the "mess")
- Price is text: `"£51.77"`
- Rating is a word: `"Three"`
- Availability is text: `"In stock"`
- Dates are text

## Cleaning steps (in order)
| # | Step | Pandas used |
|---|---|---|
| 1 | Null values: fill missing availability/rating, drop rows with no title/price/url | `.fillna()`, `.dropna()` |
| 2 | Remove extra spaces in titles | `.str.strip()` |
| 3 | **Normalize currency**: `"£51.77"` -> `51.77` | `.str.replace()`, `pd.to_numeric()` |
| 4 | Rating word -> number (`"Three"` -> `3`) | `.map()` |
| 5 | Availability -> `True/False` | `.str.contains()` |
| 6 | **Normalize dates** to real datetime | `pd.to_datetime()` |
| 7 | **Deduplicate** on `url` (same URL = same book) | `.drop_duplicates()` |
| 8 | **Enforce types** | `.astype()` |
| 9 | **Validation checks** (see below) | simple `if` checks |

## Final schema
| Column | Type |
|---|---|
| title | text |
| price_gbp | float |
| rating | integer (0-5) |
| in_stock | boolean |
| url | text (unique) |
| page | integer |
| scraped_at | datetime |

## Validation checks
- No null values left
- `price_gbp > 0`
- `rating` between 0 and 5
- URLs are unique

Types are enforced in step 8 with `.astype()` (it raises an error if a value can't be converted), and the final column types are printed in the report.

If one check fails, the script **stops with an error** and nothing is saved as clean data.

## Validation report
`logs/validation_report.txt` contains: date, rows read, nulls per column, rows removed, duplicates removed, final row count, PASSED/FAILED, column types.

## Run
```
python -m src.cleaner
```


"""Task 2 - Data cleaning.

Reads data/raw/books_raw.csv, cleans it with Pandas, checks the result,
saves data/clean/books_clean.csv and writes logs/validation_report.txt.
"""
from datetime import datetime

import pandas as pd

import config

RATING_NUMBERS = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
FINAL_COLUMNS = ["title", "price_gbp", "rating", "in_stock", "url", "page", "scraped_at"]


def run():
    report = []
    report.append("=== DATA VALIDATION REPORT ===")
    report.append(f"Date: {datetime.now():%Y-%m-%d %H:%M:%S}")

    # Read the raw file
    df = pd.read_csv(config.RAW_CSV)
    rows_in = len(df)
    report.append(f"Rows read: {rows_in}")
    report.append("Null values per column (before cleaning):")
    report.append(df.isnull().sum().to_string())

    # 1. Null values
    df["availability"] = df["availability"].fillna("Unknown")
    df["rating"] = df["rating"].fillna("Zero")
    df = df.dropna(subset=["title", "price", "url"])

    # 2. Remove extra spaces in titles
    df["title"] = df["title"].str.strip()

    # 3. Currency: "£51.77" -> 51.77
    df["price_gbp"] = df["price"].str.replace("£", "", regex=False)
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df = df.dropna(subset=["price_gbp"])

    # 4. Rating: "Three" -> 3
    df["rating"] = df["rating"].map(RATING_NUMBERS).fillna(0)

    # 5. Availability: "In stock" -> True, anything else -> False
    df["in_stock"] = df["availability"].str.contains("In stock")

    # 6. Dates: text -> real date
    df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")
    df = df.dropna(subset=["scraped_at"])
    rows_after_nulls = len(df)

    # 7. Remove duplicates (same url = same book)
    df = df.drop_duplicates(subset="url")
    duplicates_removed = rows_after_nulls - len(df)

    # 8. Keep final columns and force the types
    df = df[FINAL_COLUMNS]
    df = df.astype({"title": str, "price_gbp": float, "rating": int,
                    "in_stock": bool, "url": str, "page": int})

    # 9. Validation checks
    problems = []
    if df.isnull().any().any():
        problems.append("There are null values")
    if (df["price_gbp"] <= 0).any():
        problems.append("Some prices are 0 or negative")
    if (df["rating"] < 0).any() or (df["rating"] > 5).any():
        problems.append("Some ratings are not between 0 and 5")
    if df["url"].duplicated().any():
        problems.append("There are duplicate urls")

    report.append(f"Rows removed (missing values): {rows_in - rows_after_nulls}")
    report.append(f"Duplicates removed: {duplicates_removed}")
    report.append(f"Final rows: {len(df)}")
    if problems:
        report.append("Validation: FAILED - " + ", ".join(problems))
    else:
        report.append("Validation: PASSED")
    report.append("Column types:")
    report.append(df.dtypes.to_string())

    # 10. Save the report and the clean file
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    config.CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    config.VALIDATION_REPORT.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))

    if problems:
        raise ValueError("Validation failed, see logs/validation_report.txt")

    df.to_csv(config.CLEAN_CSV, index=False, encoding="utf-8")
    return {
        "rows_in": rows_in,
        "rows_removed_null": rows_in - rows_after_nulls,
        "duplicates_removed": duplicates_removed,
        "rows_out": len(df),
    }


if __name__ == "__main__":
    run()

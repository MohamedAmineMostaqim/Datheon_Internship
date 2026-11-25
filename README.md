# Datheon Internship - End-to-End ETL Pipeline

**Author:** Mohamed Amine Mostaqim

A beginner-friendly ETL project built during the Datheon internship. It scrapes data from a website, cleans it, loads it into PostgreSQL, and runs automatically every day with an email report.

## Pipeline overview

```
 books.toscrape.com
        |
        v
 [Task 1] Scraper (BeautifulSoup)  ->  data/raw/books_raw.csv / .json
        |
        v
 [Task 2] Cleaner (Pandas)         ->  data/clean/books_clean.csv + logs/validation_report.txt
        |
        v
 [Task 3] Loader (SQLAlchemy)      ->  PostgreSQL table "books" (upsert)
        |
        v
 [Task 4] Pipeline (schedule)      ->  logs/pipeline.log + email report
```

## The 4 tasks

| Task | What I built | Code | Documentation |
|---|---|---|---|
| 1 | Web scraper, 50 pages, 1000 records | `src/scraper.py` | [docs/01_scraper.md](docs/01_scraper.md) |
| 2 | Data cleaning + schema validation + report | `src/cleaner.py` | [docs/02_cleaner.md](docs/02_cleaner.md) |
| 3 | PostgreSQL loader with upsert + verification | `src/loader.py`, `scripts/verify_db.py` | [docs/03_loader.md](docs/03_loader.md) |
| 4 | Scheduled pipeline with logs and email alerts | `src/pipeline.py` | [docs/04_pipeline.md](docs/04_pipeline.md) |

Setup guide: [docs/00_setup.md](docs/00_setup.md)

## Tech stack
Python 3, requests, BeautifulSoup4, Pandas, SQLAlchemy, PostgreSQL, schedule, logging, smtplib.

## Project structure
```
Datheon_Internship/
├── README.md
├── requirements.txt
├── config.py            # all settings (paths, URLs, DB, email)
├── .env.example         # copy to .env and fill in
├── src/
│   ├── scraper.py       # Task 1
│   ├── cleaner.py       # Task 2
│   ├── loader.py        # Task 3
│   └── pipeline.py      # Task 4
├── scripts/
│   └── verify_db.py     # Task 3 verification queries
├── docs/                # one doc per task + setup
├── data/raw/            # scraped files
├── data/clean/          # cleaned file
└── logs/                # validation report + pipeline log
```

## Quick start
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env          # then edit .env
```
Create the database `datheon` in PostgreSQL (see [setup](docs/00_setup.md)), then run each task:
```
python -m src.scraper           # Task 1
python -m src.cleaner           # Task 2
python -m src.loader            # Task 3
python -m scripts.verify_db     # Task 3 check
python -m src.pipeline --now    # Task 4 (all steps + email)
python -m src.pipeline          # Task 4 scheduled daily
```

## Results
- 1000 records scraped (title, price, rating, availability, url, page, timestamp)
- Cleaned and validated with an automatic report
- Loaded into PostgreSQL with a primary key; re-running the loader creates no duplicates
- Automated daily run with logs and email summary/alert

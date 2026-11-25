# Task 4 - Scheduled ETL Pipeline with Alerting (`src/pipeline.py`)

## Goal
Run Extract -> Transform -> Load automatically on a schedule, log everything, and email a report.

## Flow
```
scraper.run()  ->  cleaner.run()  ->  loader.run()  ->  email report
   (Task 1)         (Task 2)          (Task 3)
```

## Components
| Need | Tool used |
|---|---|
| Scheduling | `schedule` module (`schedule.every().day.at("09:00")`) |
| Logs | `logging` module -> `logs/pipeline.log` (and `print` on screen) |
| Email | `smtplib` (Gmail SMTP, port 587, TLS) |

## How it works
1. `run_pipeline()` calls the three steps one after the other.
2. Each step returns a small **stats dictionary**; they are combined into a summary message.
3. If everything works -> email **"[ETL] Pipeline SUCCESS"** with the summary.
4. If any step raises an error -> `logging.exception` writes the full error in the log file, and an email **"[ETL] Pipeline FAILED"** is sent (this is the **alert**).
5. Without `--now`, the script registers the job with `schedule` and loops forever (`run_pending()` every 30 seconds).

## Run
```
python -m src.pipeline --now     # run once immediately (good for testing)
python -m src.pipeline           # run every day at RUN_TIME from .env
```
The terminal must stay open for the scheduler to keep running.

## Alternative: Windows Task Scheduler (cron equivalent)
Create a task that runs daily: program `venv\Scripts\python.exe`, arguments `-m src.pipeline --now`, start in the project folder.

## Example email
```
ETL pipeline finished successfully.
Duration: 62.4 seconds
Scraped: 1000 records (0 failed pages)
Cleaning: 1000 rows kept, 0 removed (nulls), 0 duplicates removed
Database: 0 inserted, 1000 updated, 1000 total rows
```
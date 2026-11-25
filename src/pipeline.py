"""Task 4 - Full pipeline: scrape -> clean -> load -> email report.

Run from the project root:
    python -m src.pipeline --now    run once, right now
    python -m src.pipeline          run every day at RUN_TIME (see .env)
"""
import logging
import smtplib
import sys
import time
from datetime import datetime

import schedule

import config
from src import cleaner, loader, scraper

config.LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=config.PIPELINE_LOG,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8",
)


def log(message):
    """Write to the log file and show it on screen."""
    logging.info(message)
    print(message)


def send_email(subject, body):
    if not (config.EMAIL_SENDER and config.EMAIL_PASSWORD and config.EMAIL_RECEIVER):
        log("Email not configured in .env, skipping email.")
        return
    try:
        message = f"Subject: {subject}\n\n{body}"
        with smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.sendmail(config.EMAIL_SENDER, config.EMAIL_RECEIVER, message.encode("utf-8"))
        log("Email sent.")
    except Exception as error:
        logging.error(f"Could not send email: {error}")
        print(f"Could not send email: {error}")


def run_pipeline():
    start = time.time()
    log("===== Pipeline started =====")
    try:
        log("Step 1/3: scraping")
        scrape_stats = scraper.run()

        log("Step 2/3: cleaning")
        clean_stats = cleaner.run()

        log("Step 3/3: loading into PostgreSQL")
        load_stats = loader.run()

        summary = (
            f"ETL pipeline finished successfully.\n"
            f"Date: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"Duration: {round(time.time() - start, 1)} seconds\n\n"
            f"Scraped: {scrape_stats['records_scraped']} records "
            f"({scrape_stats['failed_pages']} failed pages)\n"
            f"Cleaning: {clean_stats['rows_out']} rows kept, "
            f"{clean_stats['rows_removed_null']} removed, "
            f"{clean_stats['duplicates_removed']} duplicates removed\n"
            f"Database: {load_stats['inserted']} inserted, "
            f"{load_stats['updated']} updated, "
            f"{load_stats['total_in_db']} total rows\n"
        )
        log(summary)
        send_email("[ETL] Pipeline SUCCESS", summary)

    except Exception as error:
        logging.exception("Pipeline FAILED")
        print(f"Pipeline FAILED: {error}")
        send_email("[ETL] Pipeline FAILED", f"The pipeline failed.\n\nError: {error}\n\nSee logs/pipeline.log")


if "--now" in sys.argv:
    run_pipeline()
else:
    schedule.every().day.at(config.RUN_TIME).do(run_pipeline)
    log(f"Scheduler started. Pipeline will run every day at {config.RUN_TIME}.")
    while True:
        schedule.run_pending()
        time.sleep(30)

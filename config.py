"""Central settings for the whole project (paths, URLs, database, email)."""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  

# ---------- Paths ----------
BASE_DIR = Path(__file__).parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "clean"
LOG_DIR = BASE_DIR / "logs"

RAW_CSV = RAW_DIR / "books_raw.csv"
RAW_JSON = RAW_DIR / "books_raw.json"
CLEAN_CSV = CLEAN_DIR / "books_clean.csv"
VALIDATION_REPORT = LOG_DIR / "validation_report.txt"
PIPELINE_LOG = LOG_DIR / "pipeline.log"

# ---------- Scraper ----------
SITE_ROOT = "https://books.toscrape.com/catalogue/"
PAGE_URL = SITE_ROOT + "page-{}.html"
TOTAL_PAGES = 50          
DELAY_SECONDS = 0.5       

# ---------- Database ----------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:password@localhost:5432/datheon",
)

# ---------- Email ----------
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")

# ---------- Scheduler ----------
RUN_TIME = os.getenv("RUN_TIME", "09:00")

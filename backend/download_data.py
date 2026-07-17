"""
download_data.py

Run this once before starting the server.

Usage:
    python download_data.py

If marketmind.db already exists, the script exits immediately.
Otherwise it downloads the Sephora dataset from Kaggle, converts it to SQLite,
then deletes the raw CSVs to save disk space.
"""

import sys
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "marketmind.db"

REVIEW_CSV_FILES = [
    "reviews_0-250.csv",
    "reviews_250-500.csv",
    "reviews_500-750.csv",
    "reviews_750-1250.csv",
    "reviews_1250-end.csv",
]

KAGGLE_DATASET = "nadyinky/sephora-products-and-skincare-reviews"


def db_exists():
    return DB_PATH.exists()


def missing_csvs():
    all_csvs = ["product_info.csv"] + REVIEW_CSV_FILES
    return [f for f in all_csvs if not (DATA_DIR / f).exists()]


def download_from_kaggle():
    """Download and unzip the Kaggle dataset into DATA_DIR."""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        print("ERROR: kaggle package not installed. Run: pip install kaggle")
        sys.exit(1)

    print("Authenticating with Kaggle...")
    api = KaggleApi()
    api.authenticate()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading '{KAGGLE_DATASET}'...")
    api.dataset_download_files(KAGGLE_DATASET, path=str(DATA_DIR), unzip=True)
    print("Download complete.")


def compute_sentiment(text):
    """Returns TextBlob polarity score for a single review string."""
    from textblob import TextBlob
    if not isinstance(text, str) or not text.strip():
        return 0.0
    return TextBlob(text).sentiment.polarity


def build_database():
    """Reads CSVs in chunks, computes sentiment, and writes to SQLite."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)

    # --- Products table ---
    product_csv = DATA_DIR / "product_info.csv"
    if product_csv.exists():
        print("Loading products...")
        for chunk in pd.read_csv(product_csv, chunksize=10_000, low_memory=False):
            chunk.to_sql("products", conn, if_exists="append", index=False)

        conn.execute(
            "CREATE INDEX IF NOT EXISTS idx_products_product_id ON products(product_id)"
        )
        print(f"  Products loaded.")

    # --- Reviews table ---
    for filename in REVIEW_CSV_FILES:
        csv_path = DATA_DIR / filename
        if not csv_path.exists():
            print(f"  Skipping {filename} (not found)")
            continue

        print(f"Processing {filename}...")
        for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=20_000, low_memory=False)):
            print(f"  Chunk {i + 1}: computing sentiment for {len(chunk)} rows...", end="\r")
            chunk["sentiment_polarity"] = chunk["review_text"].apply(compute_sentiment)
            chunk.to_sql("reviews", conn, if_exists="append", index=False)
        print()

    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_reviews_submission_time ON reviews(submission_time)"
    )

    conn.commit()
    conn.close()
    print(f"Database built: {DB_PATH}")


def delete_csvs():
    """Remove raw CSVs after the database is built."""
    all_csvs = ["product_info.csv"] + REVIEW_CSV_FILES
    for filename in all_csvs:
        path = DATA_DIR / filename
        if path.exists():
            path.unlink()
            print(f"Deleted {filename}")


def main():
    if db_exists():
        print("SQLite database already exists. Nothing to do.")
        return

    missing = missing_csvs()
    if missing:
        print(f"Missing CSVs: {missing}. Downloading from Kaggle...")
        download_from_kaggle()

        still_missing = missing_csvs()
        if still_missing:
            print(f"ERROR: Download completed but files are still missing: {still_missing}")
            sys.exit(1)

    print("Building SQLite database...")
    build_database()

    print("Verifying database integrity...")
    conn = sqlite3.connect(DB_PATH)
    result = conn.execute("PRAGMA integrity_check").fetchone()[0]
    conn.close()
    if result.lower() != "ok":
        print(f"ERROR: Database integrity check failed: {result}")
        sys.exit(1)
    print("Integrity check passed.")

    print("Cleaning up raw CSVs...")
    delete_csvs()

    print("\nSetup complete. You can now run:")
    print("  uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()

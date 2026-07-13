import os
import sys
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "marketmind.db"

REQUIRED_CSVS = [
    "product_info.csv",
    "reviews_0-250.csv",
    "reviews_250-500.csv",
    "reviews_500-750.csv",
    "reviews_750-1250.csv",
    "reviews_1250-end.csv",
]

def is_db_ready():
    if not DB_PATH.exists():
        return False
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        has_products = cursor.fetchone() is not None
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reviews'")
        has_reviews = cursor.fetchone() is not None
        conn.close()
        return has_products and has_reviews
    except sqlite3.Error:
        return False

def check_missing_csvs():
    missing = []
    for filename in REQUIRED_CSVS:
        if not (DATA_DIR / filename).exists():
            missing.append(filename)
    return missing

def download_dataset():
    missing_csvs = check_missing_csvs()
    if not missing_csvs:
        print("Required CSVs are already present. Skipping download.")
        return
        
    print(f"Missing CSVs: {missing_csvs}")
    print("Downloading Sephora dataset via Kaggle API...")
    
    if not os.environ.get("KAGGLE_USERNAME") or not os.environ.get("KAGGLE_KEY"):
        print("ERROR: Missing KAGGLE_USERNAME or KAGGLE_KEY environment variables.")
        print("Please set these to download the dataset automatically on deployment.")
        sys.exit(1)
        
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        dataset_id = "nadyinky/sephora-products-and-skincare-reviews"
        print(f"Fetching {dataset_id}...")
        api.dataset_download_files(dataset_id, path=str(DATA_DIR), unzip=True)
        
        print("Download and extraction complete.")
        
        still_missing = check_missing_csvs()
        if still_missing:
            print(f"ERROR: Download completed but files are still missing: {still_missing}")
            sys.exit(1)
    except Exception as e:
        print(f"ERROR downloading dataset: {e}")
        sys.exit(1)

def convert_csv_to_sqlite():
    print(f"Creating SQLite database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    
    # Process products
    product_csv = DATA_DIR / "product_info.csv"
    if product_csv.exists():
        print(f"Loading {product_csv.name} into SQLite...")
        for chunk in pd.read_csv(product_csv, chunksize=10000, low_memory=False):
            chunk.to_sql("products", conn, if_exists="append", index=False)
            
    # Process reviews
    review_files = [f for f in REQUIRED_CSVS if f.startswith("reviews_")]
    for r_file in review_files:
        csv_path = DATA_DIR / r_file
        if csv_path.exists():
            print(f"Loading {r_file} into SQLite...")
            for chunk in pd.read_csv(csv_path, chunksize=20000, low_memory=False):
                chunk.to_sql("reviews", conn, if_exists="append", index=False)
                
    print("Creating indexes on products and reviews...")
    cursor = conn.cursor()
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_product_id ON products(product_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_product_id ON reviews(product_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_reviews_submission_time ON reviews(submission_time)")
    
    print("Creating materialized products_with_reviews table...")
    cursor.execute("DROP TABLE IF EXISTS products_with_reviews")
    cursor.execute('''
        CREATE TABLE products_with_reviews AS 
        SELECT p.* FROM products p 
        WHERE p.product_id IN (SELECT DISTINCT product_id FROM reviews)
    ''')
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_products_with_reviews_product_id ON products_with_reviews(product_id)")
    
    conn.commit()
    conn.close()
    print("SQLite database conversion successful.")

def verify_database():
    print("Verifying database integrity and row counts...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check integrity
    cursor.execute("PRAGMA integrity_check")
    integrity = cursor.fetchone()[0]
    if integrity.lower() != "ok":
        raise Exception(f"Database integrity check failed: {integrity}")
        
    # Check row counts
    cursor.execute("SELECT COUNT(*) FROM products")
    products_count = cursor.fetchone()[0]
    if products_count < 8000:
        raise Exception(f"Products count too low: {products_count}")
        
    cursor.execute("SELECT COUNT(*) FROM reviews")
    reviews_count = cursor.fetchone()[0]
    if reviews_count < 1000000:
        raise Exception(f"Reviews count too low: {reviews_count}")
        
    cursor.execute("SELECT COUNT(DISTINCT product_id) FROM reviews")
    unique_products_count = cursor.fetchone()[0]
    if unique_products_count < 2000:
        raise Exception(f"Unique reviewed products count too low: {unique_products_count}")
        
    # Check indexes exist
    cursor.execute("PRAGMA index_list(products)")
    products_indexes = [row[1] for row in cursor.fetchall()]
    if "idx_products_product_id" not in products_indexes:
        raise Exception("Missing products index")
        
    cursor.execute("PRAGMA index_list(reviews)")
    reviews_indexes = [row[1] for row in cursor.fetchall()]
    if "idx_reviews_product_id" not in reviews_indexes or "idx_reviews_submission_time" not in reviews_indexes:
        raise Exception(f"Missing reviews indexes. Found: {reviews_indexes}")
        
    conn.close()
    print("Verification passed! Row counts, indexes, and integrity are ok.")

def cleanup_csvs():
    print("Cleaning up raw CSV files to save disk space...")
    for filename in REQUIRED_CSVS:
        file_path = DATA_DIR / filename
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"Deleted {filename}")
            except Exception as e:
                print(f"Warning: Failed to delete {filename}: {e}")

def main():
    if is_db_ready():
        print("SQLite database is already set up and ready. Skipping data preparation.")
        sys.exit(0)
        
    download_dataset()
    convert_csv_to_sqlite()
    verify_database() # <-- CRITICAL: verify before deleting!
    cleanup_csvs()
    
    print("Backend data preparation is 100% complete.")

if __name__ == "__main__":
    main()

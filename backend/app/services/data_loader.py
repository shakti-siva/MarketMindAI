import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data"
DB_PATH = DATA_PATH / "marketmind.db"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = dict_factory
    return conn

def get_products():
    """Returns all products as a list of dicts."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, product_name, brand_name, rating, reviews, ingredients, price_usd, primary_category, highlights FROM products_with_reviews ORDER BY CAST(reviews AS INTEGER) DESC")
        return cursor.fetchall()
    finally:
        conn.close()

def get_product_details(product_id: str):
    """Returns details for a single product."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, product_name, brand_name, rating, reviews, ingredients, price_usd, primary_category, highlights FROM products WHERE product_id = ?", (str(product_id),))
        return cursor.fetchone()
    finally:
        conn.close()

def get_product_reviews(product_id: str):
    """Returns all reviews for a specific product as a generator."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT review_text, rating, submission_time, author_id, product_name, brand_name, sentiment_polarity FROM reviews WHERE product_id = ?", (str(product_id),))
        while True:
            chunk = cursor.fetchmany(1000)
            if not chunk:
                break
            for row in chunk:
                yield row
    finally:
        conn.close()

def get_recent_reviews_sample(limit: int = 10000):
    """Returns a sample of the most recent reviews across all products as a generator."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT review_text, rating, submission_time, author_id, product_name, brand_name, sentiment_polarity FROM reviews ORDER BY submission_time DESC LIMIT ?", (limit,))
        while True:
            chunk = cursor.fetchmany(1000)
            if not chunk:
                break
            for row in chunk:
                yield row
    finally:
        conn.close()

def get_total_reviews_count():
    """Returns the total number of reviews in the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM reviews")
        result = cursor.fetchone()
        return result['count'] if result else 0
    finally:
        conn.close()

def get_product_review_count(product_id: str):
    """Returns the total number of reviews for a specific product."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM reviews WHERE product_id = ?", (str(product_id),))
        result = cursor.fetchone()
        return result['count'] if result else 0
    finally:
        conn.close()
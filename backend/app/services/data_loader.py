"""
data_loader.py

All SQLite query helpers for the MarketMind AI backend.

Real Sephora dataset column reference
--------------------------------------
products : product_id, product_name, brand_name, price_usd, rating,
           reviews (count), loves_count, primary_category, highlights,
           secondary_category, tertiary_category, ingredients, ...

reviews  : product_id, product_name, brand_name, author_id, rating,
           submission_time, review_text, review_title, sentiment_polarity,
           is_recommended, skin_tone, skin_type, eye_color, hair_color, ...
"""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "marketmind.db"


def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = dict_factory
    return conn


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------

def get_products():
    """
    Returns all products ordered by review count descending.
    Selects the subset of columns needed by the frontend.
    """
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT product_id, product_name, brand_name, rating,
                   reviews, loves_count, price_usd,
                   primary_category, highlights, ingredients
            FROM   products
            ORDER  BY CAST(reviews AS INTEGER) DESC
            """
        ).fetchall()
    finally:
        conn.close()


def get_product_details(product_id: str):
    """Returns a single product row, or None if not found."""
    conn = get_connection()
    try:
        return conn.execute(
            """
            SELECT product_id, product_name, brand_name, rating,
                   reviews, loves_count, price_usd,
                   primary_category, highlights, ingredients
            FROM   products
            WHERE  product_id = ?
            """,
            (str(product_id),),
        ).fetchone()
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------------

def get_product_reviews(product_id: str):
    """
    Yields all review rows for the given product, fetching in chunks
    of 1 000 to avoid materialising millions of rows at once.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT review_text, rating, submission_time, author_id,
                   product_name, brand_name, sentiment_polarity
            FROM   reviews
            WHERE  product_id = ?
            """,
            (str(product_id),),
        )
        while True:
            chunk = cursor.fetchmany(1000)
            if not chunk:
                break
            yield from chunk
    finally:
        conn.close()


def get_recent_reviews_sample(limit: int = 10_000):
    """
    Yields up to `limit` of the most recent reviews across all products,
    useful for building the global sentiment dashboard without loading
    the full 1.1 M row table.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT review_text, rating, submission_time, author_id,
                   product_name, brand_name, sentiment_polarity
            FROM   reviews
            ORDER  BY submission_time DESC
            LIMIT  ?
            """,
            (limit,),
        )
        while True:
            chunk = cursor.fetchmany(1000)
            if not chunk:
                break
            yield from chunk
    finally:
        conn.close()


def get_total_reviews_count() -> int:
    """Returns the total number of reviews in the database."""
    conn = get_connection()
    try:
        row = conn.execute("SELECT COUNT(*) AS count FROM reviews").fetchone()
        return row["count"] if row else 0
    finally:
        conn.close()


def get_product_review_count(product_id: str) -> int:
    """Returns the number of reviews for a specific product."""
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT COUNT(*) AS count FROM reviews WHERE product_id = ?",
            (str(product_id),),
        ).fetchone()
        return row["count"] if row else 0
    finally:
        conn.close()
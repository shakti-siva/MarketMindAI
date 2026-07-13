import pandas as pd
from functools import lru_cache
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = BASE_DIR / "data"

@lru_cache(maxsize=1)
def load_products():
    products = pd.read_csv(
        DATA_PATH / "product_info.csv",
        low_memory=False
    )
    return products

@lru_cache(maxsize=1)
def load_reviews():
    review_files = [
        DATA_PATH / "reviews_0-250.csv",
        DATA_PATH / "reviews_250-500.csv",
        DATA_PATH / "reviews_500-750.csv",
        DATA_PATH / "reviews_750-1250.csv",
        DATA_PATH / "reviews_1250-end.csv",
    ]

    review_dfs = []
    for file in review_files:
        if file.exists():
            df = pd.read_csv(file, low_memory=False)
            review_dfs.append(df)

    if not review_dfs:
        return pd.DataFrame()

    reviews = pd.concat(review_dfs, ignore_index=True)
    return reviews

@lru_cache(maxsize=1)
def load_all_data():
    products = load_products()
    reviews = load_reviews()

    return {
        "products": products,
        "reviews": reviews,
    }
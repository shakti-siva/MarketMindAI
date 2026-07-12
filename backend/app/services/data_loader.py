import pandas as pd
from functools import lru_cache

DATA_PATH = "data"


@lru_cache(maxsize=1)
def load_products():
    products = pd.read_csv(
        f"{DATA_PATH}/product_info.csv",
        low_memory=False
    )

    return products


@lru_cache(maxsize=1)
def load_reviews():
    review_files = [
        f"{DATA_PATH}/reviews_0_250.csv",
    ]

    review_dfs = []

    for file in review_files:
        df = pd.read_csv(
            file,
            low_memory=False
        )
        review_dfs.append(df)

    reviews = pd.concat(
        review_dfs,
        ignore_index=True
    )

    return reviews


@lru_cache(maxsize=1)
def load_all_data():

    products = load_products()

    reviews = load_reviews()

    return {
        "products": products,
        "reviews": reviews
    }
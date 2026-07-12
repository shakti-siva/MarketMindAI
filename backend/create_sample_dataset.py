import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")

review_files = [
    "reviews_0-250.csv",
    "reviews_250-500.csv",
    "reviews_500-750.csv",
    "reviews_750-1250.csv",
    "reviews_1250-end.csv",
]

dfs = []

for file in review_files:
    print(f"Loading {file}...")
    dfs.append(pd.read_csv(DATA_DIR / file, low_memory=False))

print("Combining...")
reviews = pd.concat(dfs, ignore_index=True)

print(f"Original reviews: {len(reviews):,}")

# Random sample
sample = reviews.sample(n=10000, random_state=42)

print(f"Sample reviews: {len(sample):,}")

sample.to_csv(DATA_DIR / "reviews_sample.csv", index=False)

print("✅ Created reviews_sample.csv")
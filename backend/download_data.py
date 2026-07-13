import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

REQUIRED_FILES = [
    "product_info.csv",
    "reviews_0-250.csv",
    "reviews_250-500.csv",
    "reviews_500-750.csv",
    "reviews_750-1250.csv",
    "reviews_1250-end.csv",
]

def check_missing_files():
    missing = []
    for filename in REQUIRED_FILES:
        if not (DATA_DIR / filename).exists():
            missing.append(filename)
    return missing

def main():
    missing_files = check_missing_files()
    
    if not missing_files:
        print("All required Kaggle datasets are present. Skipping download.")
        sys.exit(0)
        
    print(f"Missing files: {missing_files}")
    print("Downloading Sephora dataset via Kaggle API...")
    
    # Ensure environment variables are set before trying to authenticate
    if not os.environ.get("KAGGLE_USERNAME") or not os.environ.get("KAGGLE_KEY"):
        print("ERROR: Missing KAGGLE_USERNAME or KAGGLE_KEY environment variables.")
        print("Please set these to download the dataset automatically on deployment.")
        sys.exit(1)
        
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        # Download and unzip the dataset directly to the data directory
        dataset_id = "nadyinky/sephora-products-and-skincare-reviews"
        print(f"Fetching {dataset_id}...")
        api.dataset_download_files(dataset_id, path=str(DATA_DIR), unzip=True)
        
        print("Download and extraction complete.")
        
        # Verify again
        still_missing = check_missing_files()
        if still_missing:
            print(f"ERROR: Download completed but files are still missing: {still_missing}")
            sys.exit(1)
            
        print("Data verification successful. All files are ready.")
        
    except Exception as e:
        print(f"ERROR downloading dataset: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

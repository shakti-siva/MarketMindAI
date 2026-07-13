import pandas as pd
from textblob import TextBlob
from functools import lru_cache
from .data_loader import load_all_data


def analyze_sentiment(polarity):
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"


def get_sentiment_polarities(reviews):
    return reviews["review_text"].fillna("").apply(
        lambda x: TextBlob(str(x)).sentiment.polarity
    )


def get_customer_voice_dashboard(sample_size=10000):
    data = load_all_data()
    reviews_raw = data["reviews"]

    if reviews_raw.empty:
        return {}

    reviews = reviews_raw.dropna(subset=["review_text"]).copy()

    if len(reviews) > sample_size:
        reviews = reviews.sample(sample_size, random_state=42)

    polarities = get_sentiment_polarities(reviews)
    reviews["sentiment"] = polarities.apply(analyze_sentiment)

    sentiment_counts = reviews["sentiment"].value_counts().to_dict()
    total = len(reviews)

    reviews_text = reviews["review_text"].fillna("").str.lower()

    complaint_keywords = {
        "Packaging Issue": ["leak", "pump", "broken", "spill", "packaging", "dispense", "waste"],
        "Skin Irritation": ["broke me out", "acne", "burn", "red", "blotchy", "breakout", "irritat", "bump", "itch"],
        "Texture / Feel": ["greasy", "oily", "residue", "pill", "flake", "heavy", "sticky", "clog"],
        "Scent / Odor": ["smell", "scent", "fragrance", "odor", "stink", "perfume"],
    }

    complaint_counts = {}
    top_complaint = {"name": None, "count": 0}
    for complaint_type, keywords in complaint_keywords.items():
        mask = reviews_text.apply(lambda text: any(kw in text for kw in keywords))
        matches = reviews[mask & (polarities < 0.0)]
        count = int(matches.shape[0])
        samples = []
        for _, row in matches.head(3).iterrows():
            samples.append({
                "text": row.get("review_text", ""),
                "rating": int(row.get("rating", 1)) if pd.notna(row.get("rating")) else 1,
                "date": row.get("submission_time", "N/A"),
                "author": row.get("author_id", "Anonymous")
            })
        complaint_counts[complaint_type] = {
            "count": count,
            "percentage": round((count / total) * 100, 1) if total > 0 else 0,
            "samples": samples
        }
        if count > top_complaint["count"]:
            top_complaint = {"name": complaint_type, "count": count}

    praise_keywords = {
        "Hydration": ["hydrat", "moist", "plump", "dry skin", "watery"],
        "Glow / Brightening": ["glow", "bright", "radiant", "luminous", "dullness"],
        "Acne / Clearing": ["acne", "clear", "pimple", "spot", "blackhead"],
        "Anti-Aging": ["wrinkle", "fine line", "firm", "tight", "aging"],
    }

    praise_counts = {}
    top_praise = {"name": None, "count": 0}
    for praise_type, keywords in praise_keywords.items():
        mask = reviews_text.apply(lambda text: any(kw in text for kw in keywords))
        matches = reviews[mask & (polarities > 0.2)]
        count = int(matches.shape[0])
        samples = []
        for _, row in matches.head(3).iterrows():
            samples.append({
                "text": row.get("review_text", ""),
                "rating": int(row.get("rating", 5)) if pd.notna(row.get("rating")) else 5,
                "date": row.get("submission_time", "N/A"),
                "author": row.get("author_id", "Anonymous")
            })
        praise_counts[praise_type] = {
            "count": count,
            "percentage": round((count / total) * 100, 1) if total > 0 else 0,
            "samples": samples
        }
        if count > top_praise["count"]:
            top_praise = {"name": praise_type, "count": count}

    return {
        "total_reviews_available": int(len(reviews_raw)),
        "reviews_analyzed": int(total),
        "sentiment_distribution": {
            "positive": int(sentiment_counts.get("positive", 0)),
            "neutral": int(sentiment_counts.get("neutral", 0)),
            "negative": int(sentiment_counts.get("negative", 0)),
        },
        "sentiment_percentages": {
            "positive": round((sentiment_counts.get("positive", 0) / total) * 100, 1) if total > 0 else 0,
            "neutral": round((sentiment_counts.get("neutral", 0) / total) * 100, 1) if total > 0 else 0,
            "negative": round((sentiment_counts.get("negative", 0) / total) * 100, 1) if total > 0 else 0,
        },
        "complaints": complaint_counts,
        "praises": praise_counts,
        "top_complaint": top_complaint["name"],
        "top_praise": top_praise["name"],
    }


def get_product_customer_voice(product_id: str):
    data = load_all_data()
    reviews_raw = data["reviews"]
    matches = reviews_raw[reviews_raw["product_id"].astype(str) == str(product_id)]

    # Filter reviews for this product
    reviews = reviews_raw[
        reviews_raw["product_id"].astype(str).str.strip() == str(product_id).strip()
    ].copy()

    if reviews.empty:
        return None

    # Remove empty reviews
    reviews = reviews.dropna(subset=["review_text"]).copy()

    polarities = get_sentiment_polarities(reviews)
    reviews["sentiment"] = polarities.apply(analyze_sentiment)

    sentiment_counts = reviews["sentiment"].value_counts().to_dict()
    total = len(reviews)

    reviews_text = reviews["review_text"].fillna("").str.lower()

    complaint_keywords = {
        "packaging_leak": [
            "leak", "spill", "pump", "bottle", "dispenser"
        ],
        "skin_irritation": [
            "broke me out", "breakout", "acne",
            "bump", "rash", "burn", "redness", "itch"
        ],
        "greasy_residue": [
            "greasy", "oily", "heavy", "shiny", "thick"
        ],
        "makeup_pilling": [
            "pill", "pilling", "flake", "peel", "makeup", "foundation"
        ],
    }

    complaints = {}
    top_complaint = {"name": None, "count": 0}

    ratings = pd.to_numeric(reviews["rating"], errors="coerce")

    for key, keywords in complaint_keywords.items():
        mask = reviews_text.apply(
            lambda text: any(word in text for word in keywords)
        )

        matches = reviews[
            mask & ((polarities < -0.05) | (ratings <= 2))
        ]

        count = len(matches)

        samples = []
        for _, row in matches.head(3).iterrows():
            samples.append({
                "text": row.get("review_text", ""),
                "rating": int(row["rating"]) if pd.notna(row["rating"]) else 1,
                "date": row.get("submission_time", "N/A"),
                "author": row.get("author_id", "Anonymous"),
            })

        complaints[key] = {
            "count": count,
            "percentage": round(count / total * 100, 1) if total else 0,
            "samples": samples,
        }

        if count > top_complaint["count"]:
            top_complaint = {"name": key, "count": count}

    praise_keywords = {
        "intense_hydration": [
            "hydrate", "hydrating", "moist",
            "moisture", "plump", "dewy", "soft"
        ],
        "fast_absorption": [
            "absorb", "absorbs", "absorbed",
            "lightweight", "quick", "fast"
        ],
        "clearing_effects": [
            "clear", "cleared", "acne",
            "pimple", "soothe", "soothing", "redness"
        ],
    }

    praises = {}
    top_praise = {"name": None, "count": 0}

    for key, keywords in praise_keywords.items():
        mask = reviews_text.apply(
            lambda text: any(word in text for word in keywords)
        )

        matches = reviews[
            mask & (polarities > 0.2)
        ]

        count = len(matches)

        samples = []
        for _, row in matches.head(3).iterrows():
            samples.append({
                "text": row.get("review_text", ""),
                "rating": int(row["rating"]) if pd.notna(row["rating"]) else 5,
                "date": row.get("submission_time", "N/A"),
                "author": row.get("author_id", "Anonymous"),
            })

        praises[key] = {
            "count": count,
            "percentage": round(count / total * 100, 1) if total else 0,
            "samples": samples,
        }

        if count > top_praise["count"]:
            top_praise = {"name": key, "count": count}

    product_name = None
    brand_name = None

    if "product_name" in reviews.columns:
        product_name = reviews["product_name"].iloc[0]

    if "brand_name" in reviews.columns:
        brand_name = reviews["brand_name"].iloc[0]

    return {
        "product_id": product_id,
        "product_name": product_name,
        "brand_name": brand_name,
        "total_reviews_available": len(reviews_raw),
        "total_reviews": total,

        "sentiment_percentages": {
            "positive": round(
                sentiment_counts.get("positive", 0) / total * 100, 1
            ) if total else 0,

            "neutral": round(
                sentiment_counts.get("neutral", 0) / total * 100, 1
            ) if total else 0,

            "negative": round(
                sentiment_counts.get("negative", 0) / total * 100, 1
            ) if total else 0,
        },

        "complaints": complaints,
        "praises": praises,
        "top_complaint": top_complaint["name"],
        "top_praise": top_praise["name"],
    } 
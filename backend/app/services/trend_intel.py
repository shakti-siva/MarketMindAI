import json
import os
from datetime import datetime, timedelta
from pytrends.request import TrendReq

CACHE_FILE = "data/trend_cache.json"
CACHE_HOURS = 24

TREND_KEYWORDS = {
    "peptides": {
        "name": "Peptides",
        "category": "Anti-Aging / Skin Firming",
        "summary": "Peptides are linked to firming, collagen support, and barrier-friendly anti-aging routines."
    },
    "vitamin c": {
        "name": "Vitamin C",
        "category": "Brightening / Antioxidant",
        "summary": "Vitamin C is associated with brightening, antioxidant protection, and hyperpigmentation care."
    },
    "retinol": {
        "name": "Retinol",
        "category": "Anti-Aging / Retinoids",
        "summary": "Retinol remains powerful but may face concerns around irritation and barrier damage."
    },
    "niacinamide": {
        "name": "Niacinamide",
        "category": "Oil Control / Pore Refining",
        "summary": "Niacinamide is used for oil control, pores, redness, and barrier support."
    },
    "ceramides": {
        "name": "Ceramides",
        "category": "Barrier Repair",
        "summary": "Ceramides are connected to barrier repair, hydration, and sensitive skin recovery."
    },
    "salicylic acid": {
        "name": "Salicylic Acid",
        "category": "Acne / Exfoliation",
        "summary": "Salicylic acid remains a core acne-care ingredient for oily and clogged skin."
    },
    "hyaluronic acid": {
        "name": "Hyaluronic Acid",
        "category": "Hydration / Plumping",
        "summary": "Hyaluronic acid is linked to hydration, plumping, and lightweight moisture routines."
    },
    "squalane": {
        "name": "Squalane",
        "category": "Hydration / Barrier Support",
        "summary": "Squalane is popular for lightweight, non-greasy hydration and barrier support."
    }
}

MOCK_TRENDS = {
    "peptides": {"momentum": 43.0},
    "vitamin c": {"momentum": 21.0},
    "retinol": {"momentum": -5.0},
    "niacinamide": {"momentum": 15.5},
    "ceramides": {"momentum": 32.2},
    "salicylic acid": {"momentum": 4.5},
    "hyaluronic acid": {"momentum": 10.0},
    "squalane": {"momentum": 18.0},
}


def is_cache_fresh():
    if not os.path.exists(CACHE_FILE):
        return False

    modified_time = datetime.fromtimestamp(os.path.getmtime(CACHE_FILE))
    return datetime.now() - modified_time < timedelta(hours=CACHE_HOURS)


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None

    with open(CACHE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_cache(data):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)

    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def calculate_momentum(series):
    values = [int(v) for v in series.tolist() if v is not None]

    if len(values) < 4:
        return 0.0

    midpoint = len(values) // 2
    old_avg = sum(values[:midpoint]) / max(1, len(values[:midpoint]))
    new_avg = sum(values[midpoint:]) / max(1, len(values[midpoint:]))

    if old_avg == 0:
        return 0.0

    return round(((new_avg - old_avg) / old_avg) * 100, 1)


def get_google_trends_data():
    pytrends = TrendReq(hl="en-US", tz=330)

    results = []
    keywords = list(TREND_KEYWORDS.keys())

    for i in range(0, len(keywords), 5):
        batch = keywords[i:i + 5]

        pytrends.build_payload(
            batch,
            cat=44,
            timeframe="today 12-m",
            geo="",
            gprop=""
        )

        data = pytrends.interest_over_time()

        if data.empty:
            continue

        for keyword in batch:
            if keyword not in data.columns:
                continue

            series = data[keyword]
            momentum = calculate_momentum(series)

            history = []
            monthly = series.resample("ME").mean()

            for date, value in monthly.items():
                history.append({
                    "month": date.strftime("%b %Y"),
                    "interest": int(round(value))
                })

            meta = TREND_KEYWORDS[keyword]

            results.append({
                "key": keyword,
                "name": meta["name"],
                "category": meta["category"],
                "momentum": momentum,
                "google_interest": int(series.tail(4).mean()),
                "reddit_mentions": 0,
                "reddit_growth": 0,
                "news_mentions": 0,
                "summary": meta["summary"],
                "history": history
            })

    return results


def get_fallback_trends():
    fallback = []

    for key, meta in TREND_KEYWORDS.items():
        momentum = MOCK_TRENDS.get(key, {}).get("momentum", 0.0)

        fallback.append({
            "key": key,
            "name": meta["name"],
            "category": meta["category"],
            "momentum": momentum,
            "google_interest": 0,
            "reddit_mentions": 0,
            "reddit_growth": 0,
            "news_mentions": 0,
            "summary": meta["summary"],
            "history": []
        })

    return sorted(fallback, key=lambda x: x["momentum"], reverse=True)


def get_trend_intelligence():
    if is_cache_fresh():
        cached = load_cache()
        if cached:
            return cached

    try:
        trends = get_google_trends_data()

        if trends:
            trends = sorted(trends, key=lambda x: x["momentum"], reverse=True)
            save_cache(trends)
            return trends

    except Exception as error:
        print("Google Trends failed:", error)

    cached = load_cache()
    if cached:
        print("Using old trend cache.")
        return cached

    print("Using fallback mock trends.")
    return get_fallback_trends()


def get_reddit_skincare_topics():
    return [
        {
            "topic": "Skin Barrier Recovery",
            "posts_count": 842,
            "sentiment_score": 0.72,
            "urgency_score": 95,
            "top_words": ["barrier", "slugging", "ceramides", "dryness", "heal", "soothing"],
            "description": "Skincare users are focused on repairing moisture barriers damaged by over-exfoliation."
        },
        {
            "topic": "Glass Skin Routine",
            "posts_count": 650,
            "sentiment_score": 0.85,
            "urgency_score": 82,
            "top_words": ["glow", "dewy", "hydration", "serum", "korean", "glass skin"],
            "description": "Consumers discuss layered hydration routines for a smooth, dewy skin finish."
        },
        {
            "topic": "SPF Pilling Under Makeup",
            "posts_count": 420,
            "sentiment_score": -0.38,
            "urgency_score": 88,
            "top_words": ["pilling", "sunscreen", "makeup", "foundation", "peeling", "silicone"],
            "description": "Users complain about sunscreen and skincare products pilling under makeup."
        },
        {
            "topic": "Gentle Retinol Alternatives",
            "posts_count": 380,
            "sentiment_score": 0.61,
            "urgency_score": 76,
            "top_words": ["bakuchiol", "peptides", "sensitive", "retinol", "gentle", "irritation"],
            "description": "Users are seeking anti-aging benefits without redness, burning, and purging."
        }
    ]
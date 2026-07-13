from textblob import TextBlob
from .data_loader import get_recent_reviews_sample, get_product_reviews, get_total_reviews_count

def analyze_sentiment(polarity):
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    return "neutral"

def get_sentiment_polarity(text):
    if not text:
        return 0.0
    return TextBlob(str(text)).sentiment.polarity

def process_reviews_analytics(reviews_list, total_available):
    if not reviews_list:
        return {}

    total = len(reviews_list)
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    
    complaint_keywords = {
        "packaging_leak": ["leak", "spill", "pump", "bottle", "dispenser", "broken", "packaging", "waste"],
        "skin_irritation": ["broke me out", "breakout", "acne", "bump", "rash", "burn", "redness", "itch", "irritat"],
        "greasy_residue": ["greasy", "oily", "heavy", "shiny", "thick", "residue", "pill", "flake"],
        "scent_odor": ["smell", "scent", "fragrance", "odor", "stink", "perfume"],
    }

    praise_keywords = {
        "intense_hydration": ["hydrate", "hydrating", "moist", "moisture", "plump", "dewy", "soft", "watery"],
        "glow_brightening": ["glow", "bright", "radiant", "luminous", "dullness"],
        "clearing_effects": ["clear", "cleared", "acne", "pimple", "soothe", "soothing", "spot", "blackhead"],
        "anti_aging": ["wrinkle", "fine line", "firm", "tight", "aging"],
    }

    complaint_stats = {k: {"count": 0, "samples": []} for k in complaint_keywords.keys()}
    praise_stats = {k: {"count": 0, "samples": []} for k in praise_keywords.keys()}
    
    for row in reviews_list:
        text = str(row.get("review_text") or "")
        if not text.strip():
            continue
            
        lower_text = text.lower()
        polarity = get_sentiment_polarity(text)
        sentiment = analyze_sentiment(polarity)
        sentiment_counts[sentiment] += 1
        
        try:
            rating_val = float(row.get("rating", 0))
        except (ValueError, TypeError):
            rating_val = 0
            
        # Check complaints
        if polarity < -0.05 or rating_val <= 2:
            for c_key, c_words in complaint_keywords.items():
                if any(w in lower_text for w in c_words):
                    complaint_stats[c_key]["count"] += 1
                    if len(complaint_stats[c_key]["samples"]) < 3:
                        complaint_stats[c_key]["samples"].append({
                            "text": text,
                            "rating": int(rating_val) if rating_val else 1,
                            "date": row.get("submission_time", "N/A"),
                            "author": row.get("author_id", "Anonymous")
                        })
                        
        # Check praises
        if polarity > 0.2 or rating_val >= 4:
            for p_key, p_words in praise_keywords.items():
                if any(w in lower_text for w in p_words):
                    praise_stats[p_key]["count"] += 1
                    if len(praise_stats[p_key]["samples"]) < 3:
                        praise_stats[p_key]["samples"].append({
                            "text": text,
                            "rating": int(rating_val) if rating_val else 5,
                            "date": row.get("submission_time", "N/A"),
                            "author": row.get("author_id", "Anonymous")
                        })
                        
    # Format complaints output
    complaints_out = {}
    top_complaint = {"name": None, "count": 0}
    for k, stat in complaint_stats.items():
        count = stat["count"]
        complaints_out[k] = {
            "count": count,
            "percentage": round(count / total * 100, 1) if total > 0 else 0,
            "samples": stat["samples"]
        }
        if count > top_complaint["count"]:
            top_complaint = {"name": k, "count": count}
            
    # Format praises output
    praises_out = {}
    top_praise = {"name": None, "count": 0}
    for k, stat in praise_stats.items():
        count = stat["count"]
        praises_out[k] = {
            "count": count,
            "percentage": round(count / total * 100, 1) if total > 0 else 0,
            "samples": stat["samples"]
        }
        if count > top_praise["count"]:
            top_praise = {"name": k, "count": count}
            
    return {
        "total_reviews_available": total_available,
        "reviews_analyzed": total,
        "sentiment_distribution": sentiment_counts,
        "sentiment_percentages": {
            "positive": round((sentiment_counts["positive"] / total) * 100, 1) if total > 0 else 0,
            "neutral": round((sentiment_counts["neutral"] / total) * 100, 1) if total > 0 else 0,
            "negative": round((sentiment_counts["negative"] / total) * 100, 1) if total > 0 else 0,
        },
        "complaints": complaints_out,
        "praises": praises_out,
        "top_complaint": top_complaint["name"],
        "top_praise": top_praise["name"],
    }

def get_customer_voice_dashboard(sample_size=10000):
    total_available = get_total_reviews_count()
    reviews_list = get_recent_reviews_sample(sample_size)
    return process_reviews_analytics(reviews_list, total_available)

def get_product_customer_voice(product_id: str):
    reviews_list = get_product_reviews(product_id)
    if not reviews_list:
        return None
        
    total_available = len(reviews_list)
    result = process_reviews_analytics(reviews_list, total_available)
    
    # Add product specifics
    result["product_id"] = product_id
    result["product_name"] = reviews_list[0].get("product_name") if reviews_list else None
    result["brand_name"] = reviews_list[0].get("brand_name") if reviews_list else None
    result["total_reviews"] = result["reviews_analyzed"]
    
    return result
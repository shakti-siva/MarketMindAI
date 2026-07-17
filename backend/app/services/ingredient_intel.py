from collections import defaultdict
from .data_loader import get_products

# Standard ingredient database with properties
SKINCARE_INGREDIENTS = {
    "niacinamide": {"benefits": ["Brightening", "Pore Minimizing", "Oil Control"], "category": "Vitamin B3"},
    "hyaluronic acid": {"benefits": ["Hydration", "Plumping"], "category": "Humectant"},
    "retinol": {"benefits": ["Anti-aging", "Cell Turnover"], "category": "Vitamin A"},
    "vitamin c": {"benefits": ["Brightening", "Antioxidant", "Collagen Production"], "category": "Antioxidant"},
    "salicylic acid": {"benefits": ["Acne Control", "Exfoliation"], "category": "BHA"},
    "glycolic acid": {"benefits": ["Exfoliation", "Texture Smoothing"], "category": "AHA"},
    "peptides": {"benefits": ["Firming", "Barrier Support"], "category": "Proteins"},
    "ceramides": {"benefits": ["Barrier Repair", "Moisture Retention"], "category": "Lipids"},
    "centella asiatica": {"benefits": ["Soothing", "Calming Redness"], "category": "Botanical"},
    "squalane": {"benefits": ["Moisturizing", "Emollient"], "category": "Oil/Lipid"},
    "lactic acid": {"benefits": ["Gentle Exfoliation", "Hydration"], "category": "AHA"},
    "azelaic acid": {"benefits": ["Redness Reduction", "Acne Control"], "category": "Dicarboxylic Acid"},
    "panthenol": {"benefits": ["Soothing", "Barrier Repair"], "category": "Vitamin B5"},
    "bakuchiol": {"benefits": ["Gentle Anti-aging", "Retinol Alternative"], "category": "Botanical"}
}

def clean_ingredient_name(name):
    return str(name).strip().lower()

def get_ingredient_analytics():
    """Compiles statistics and performance scores for all key skincare ingredients."""
    products = get_products()
    if not products:
        return []

    # Map product_id → rating and review count
    product_stats = {}
    for p in products:
        try:
            rating = float(p.get("rating") or 0)
            count = int(float(p.get("reviews") or 0))
        except (ValueError, TypeError):
            rating, count = 0.0, 0

        product_stats[p["product_id"]] = {
            "avg_rating": rating,
            "review_count": count,
        }

    ingredient_stats = defaultdict(lambda: {
        "product_count": 0,
        "total_reviews": 0,
        "sum_weighted_rating": 0.0
    })

    # Find products containing these ingredients
    for p in products:
        pid = p["product_id"]
        ing_list = str(p.get("ingredients") or "").lower()
        stats = product_stats.get(pid, {"avg_rating": 0, "review_count": 0})
        
        for ing_key in SKINCARE_INGREDIENTS.keys():
            if ing_key in ing_list:
                ingredient_stats[ing_key]["product_count"] += 1
                ingredient_stats[ing_key]["total_reviews"] += stats["review_count"]
                ingredient_stats[ing_key]["sum_weighted_rating"] += (stats["avg_rating"] * stats["review_count"])

    results = []
    
    for ing_key, props in SKINCARE_INGREDIENTS.items():
        stats = ingredient_stats[ing_key]
        if stats["product_count"] == 0:
            continue
            
        avg_rating = 0
        if stats["total_reviews"] > 0:
            avg_rating = stats["sum_weighted_rating"] / stats["total_reviews"]
            
        # Simplified success score formula
        # Baseline is avg rating (0-5) mapped to 0-100, plus a volume bonus
        rating_score = (avg_rating / 5.0) * 80
        volume_score = min(20, (stats["total_reviews"] / 100000) * 20)
        success_score = min(100, rating_score + volume_score)

        results.append({
            "key": ing_key,
            "name": ing_key.title(),
            "category": props["category"],
            "benefits": props["benefits"],
            "product_count": stats["product_count"],
            "average_rating": round(avg_rating, 2),
            "total_reviews": stats["total_reviews"],
            "success_score": round(success_score, 1)
        })

    # Sort by success score descending
    results.sort(key=lambda x: x["success_score"], reverse=True)
    return results

def check_pair_compatibility(ing1: str, ing2: str):
    """
    Evaluates the synergy between two specific ingredients.
    """
    i1 = clean_ingredient_name(ing1)
    i2 = clean_ingredient_name(ing2)
    
    # Conflict definitions
    conflicts = {
        ("retinol", "vitamin c"): {
            "status": "warning",
            "score": 45,
            "message": "Can cause significant irritation when used together. Best to use Vitamin C in AM and Retinol in PM.",
            "synergy_type": "pH Conflict"
        },
        ("retinol", "salicylic acid"): {
            "status": "danger",
            "score": 30,
            "message": "Both promote high cell turnover. Using together often leads to a compromised skin barrier and severe dryness.",
            "synergy_type": "Over-exfoliation"
        },
        ("glycolic acid", "salicylic acid"): {
            "status": "warning",
            "score": 40,
            "message": "Combining AHA and BHA can be too harsh for daily use unless formulated together at lower percentages.",
            "synergy_type": "Over-exfoliation"
        },
        ("glycolic acid", "retinol"): {
            "status": "danger",
            "score": 25,
            "message": "Extremely high risk of irritation. Do not layer these ingredients.",
            "synergy_type": "Severe Irritation"
        },
    }

    # Synergy definitions
    synergies = {
        ("ceramides", "retinol"): {
            "status": "excellent",
            "score": 95,
            "message": "Perfect pair. Ceramides restore the skin barrier that retinol tends to disrupt, reducing irritation.",
            "synergy_type": "Barrier Repair"
        },
        ("niacinamide", "retinol"): {
            "status": "excellent",
            "score": 90,
            "message": "Niacinamide calms the skin and stimulates ceramide production, making retinol much easier to tolerate.",
            "synergy_type": "Soothing & Efficacy"
        },
        ("vitamin c", "vitamin e"): {
            "status": "excellent",
            "score": 98,
            "message": "Classic antioxidant synergy. Vitamin E stabilizes Vitamin C and quadruples its photoprotective power.",
            "synergy_type": "Antioxidant Boost"
        },
        ("niacinamide", "salicylic acid"): {
            "status": "good",
            "score": 85,
            "message": "Great for acne. BHA clears pores while niacinamide reduces inflammation and regulates oil.",
            "synergy_type": "Acne Clearing"
        },
        ("ceramides", "hyaluronic acid"): {
            "status": "excellent",
            "score": 92,
            "message": "Ultimate hydration combo. HA draws in water while ceramides lock it in.",
            "synergy_type": "Moisture Lock"
        },
    }
    
    pair = tuple(sorted([i1, i2]))
    
    if pair in conflicts:
        return conflicts[pair]
    
    if pair in synergies:
        return synergies[pair]
        
    return {
        "status": "neutral",
        "score": 65,
        "message": "These ingredients can generally be used together without adverse reactions, though they do not have a documented synergistic effect.",
        "synergy_type": "Independent Action"
    }

import pandas as pd
from collections import defaultdict
from .data_loader import load_all_data

# Standard ingredient database with properties
INGREDIENT_METADATA = {
    "niacinamide": {
        "display_name": "Niacinamide",
        "category": "Vitamin B3 / Barrier Repair",
        "description": "Excellent for oil control, reducing redness, skin barrier repair, and fading hyperpigmentation."
    },
    "retinol": {
        "display_name": "Retinol",
        "category": "Vitamin A / Anti-Aging",
        "description": "Gold standard for cellular turnover, collagen boosting, acne reduction, and smoothing wrinkles."
    },
    "ceramides": {
        "display_name": "Ceramides",
        "category": "Lipids / Barrier Repair",
        "description": "Crucial fats that maintain the skin moisture barrier and prevent trans-epidermal water loss."
    },
    "hyaluronic acid": {
        "display_name": "Hyaluronic Acid",
        "category": "Humectant / Hydration",
        "description": "Attracts up to 1,000 times its weight in water to intensely hydrate and plump skin surface."
    },
    "vitamin c": {
        "display_name": "Vitamin C (Ascorbic Acid)",
        "category": "Antioxidant / Brightening",
        "description": "Fights free radicals, boosts collagen synthesis, and brightens dark spots and pigmentation."
    },
    "salicylic acid": {
        "display_name": "Salicylic Acid (BHA)",
        "category": "Exfoliant / Acne Control",
        "description": "Oil-soluble exfoliant that penetrates deep into pores to dissolve debris, sebum, and clear blackheads."
    },
    "glycolic acid": {
        "display_name": "Glycolic Acid (AHA)",
        "category": "Exfoliant / Resurfacing",
        "description": "Water-soluble exfoliant that sloughs away dead surface skin cells for smoother, brighter texture."
    },
    "peptides": {
        "display_name": "Peptides",
        "category": "Proteins / Firming",
        "description": "Short chain amino acids that signal skin cells to produce collagen and elastin for firmer skin."
    },
    "centella asiatica": {
        "display_name": "Centella Asiatica (Cica)",
        "category": "Botanical / Soothing",
        "description": "Rich in amino acids and active compounds to soothe inflammation, speed healing, and calm redness."
    },
    "squalane": {
        "display_name": "Squalane",
        "category": "Emollient / Hydration",
        "description": "A stable skin-identical oil that mimics natural sebum, providing light, non-comedogenic hydration."
    },
    "zinc pca": {
        "display_name": "Zinc PCA",
        "category": "Mineral / Oil Control",
        "description": "Regulates sebum production, limits acne bacteria growth, and works synergistically with Niacinamide."
    }
}

# Compatibility rules for common ingredient pairs
PAIR_COMPATIBILITY = {
    ("niacinamide", "zinc pca"): {
        "status": "Synergistic",
        "compatibility_index": 98,
        "description": "Highly synergistic! Excellent combination for oily and acne-prone skin. Regulates sebum production while reducing redness and blemishes."
    },
    ("retinol", "ceramides"): {
        "status": "Synergistic",
        "compatibility_index": 95,
        "description": "Highly recommended! Ceramides strengthen the skin barrier and significantly reduce the dryness and irritation caused by Retinol."
    },
    ("hyaluronic acid", "retinol"): {
        "status": "Compatible",
        "compatibility_index": 90,
        "description": "Great combination. Hyaluronic acid hydrates the skin, offsetting retinol's drying side effects. Apply HA first on damp skin, then follow with retinol."
    },
    ("vitamin c", "retinol"): {
        "status": "Precaution",
        "compatibility_index": 45,
        "description": "Use with caution. Using both in the same routine can cause irritation, redness, and peeling due to pH differences. Best practice is Vitamin C in AM and Retinol in PM."
    },
    ("glycolic acid", "retinol"): {
        "status": "Incompatible",
        "compatibility_index": 20,
        "description": "High risk of irritation! Combining strong AHA exfoliants with Retinol can severely compromise the skin moisture barrier. Avoid using in the same routine; rotate days."
    },
    ("salicylic acid", "retinol"): {
        "status": "Incompatible",
        "compatibility_index": 25,
        "description": "High risk of irritation! BHA and Retinol are both active treatments. Combining them can lead to extreme dryness, redness, and peeling. Do not layer them together."
    },
    ("niacinamide", "vitamin c"): {
        "status": "Compatible",
        "compatibility_index": 80,
        "description": "Generally safe. Older studies suggested they neutralize each other, but modern formulations allow both to be used safely. Can be layered, or split AM/PM."
    },
    ("hyaluronic acid", "centella asiatica"): {
        "status": "Synergistic",
        "compatibility_index": 96,
        "description": "Excellent calming combo. Centella reduces inflammation while Hyaluronic Acid locks in moisture, perfect for skin barrier repair and soothing sensitivity."
    }
}

def clean_ingredient_name(name):
    name = str(name).lower().strip()
    # Normalize common variations
    if "ascorbic acid" in name or "vitamin c" in name:
        return "vitamin c"
    if "niacinamide" in name:
        return "niacinamide"
    if "retinol" in name:
        return "retinol"
    if "ceramide" in name:
        return "ceramides"
    if "hyaluronic" in name:
        return "hyaluronic acid"
    if "salicylic" in name:
        return "salicylic acid"
    if "glycolic" in name:
        return "glycolic acid"
    if "peptide" in name:
        return "peptides"
    if "centella" in name or "cica" in name:
        return "centella asiatica"
    if "squalane" in name:
        return "squalane"
    if "zinc pca" in name:
        return "zinc pca"
    return name

def get_ingredient_analytics():
    """Compiles statistics and performance scores for all key skincare ingredients."""

    data = load_all_data()

    products = data["products"].copy()
    reviews = data["reviews"].copy()

    if products.empty:
        return []

    # Clean numeric columns
    products["rating"] = pd.to_numeric(
        products["rating"],
        errors="coerce"
    )

    products["loves_count"] = pd.to_numeric(
        products["loves_count"],
        errors="coerce"
    ).fillna(0)

    reviews["rating"] = pd.to_numeric(
        reviews["rating"],
        errors="coerce"
    )

    # Calculate actual review statistics
    product_stats = reviews.groupby("product_id").agg(
        avg_rating=("rating", "mean"),
        review_count=("rating", "count")
    ).reset_index()

    # Merge product info with review statistics
    prod_full = products.merge(
        product_stats,
        on="product_id",
        how="left"
    )

    prod_full["avg_rating"] = prod_full["avg_rating"].fillna(
        prod_full["rating"]
    )

    prod_full["avg_rating"] = prod_full["avg_rating"].fillna(4.0)

    prod_full["review_count"] = prod_full["review_count"].fillna(0)

    # Analyze ingredient frequencies and ratings
    ing_counts = defaultdict(int)
    ing_ratings = defaultdict(list)
    ing_loves = defaultdict(int)

    for _, row in prod_full.iterrows():

        ing_list = str(row["ingredients"]).split(",")

        for ing in ing_list:

            cleaned = clean_ingredient_name(ing)

            if cleaned in INGREDIENT_METADATA:

                ing_counts[cleaned] += 1

                ing_ratings[cleaned].append(
                    row["avg_rating"]
                )

                ing_loves[cleaned] += int(
                    row["loves_count"]
                )

    results = []

    max_count = max(ing_counts.values()) if ing_counts else 1
    max_loves = max(ing_loves.values()) if ing_loves else 1

    for ing_key, meta in INGREDIENT_METADATA.items():

        count = ing_counts.get(ing_key, 0)

        ratings = [
            r for r in ing_ratings.get(ing_key, [])
            if pd.notna(r)
        ]

        avg_rating = (
            sum(ratings) / len(ratings)
            if ratings else 4.0
        )

        loves = ing_loves.get(ing_key, 0)

        # Popularity Score
        pop_score = (
            (count / max_count) * 60
            +
            (loves / max_loves) * 40
        )

        # Success Score
        norm_rating = (
            ((avg_rating - 1) / 4) * 100
        )

        norm_loves = min(
            (loves / max_loves) * 100,
            100
        )

        success_score = (
            norm_rating * 0.7
            +
            norm_loves * 0.3
        )

        results.append({
            "key": ing_key,
            "name": meta["display_name"],
            "category": meta["category"],
            "description": meta["description"],
            "product_count": count,
            "avg_rating": round(avg_rating, 2),
            "total_loves": int(loves),
            "popularity_score": round(pop_score, 1),
            "success_score": round(success_score, 1)
        })

    results = sorted(
        results,
        key=lambda x: x["success_score"],
        reverse=True
    )

    return results
def check_pair_compatibility(ing1: str, ing2: str):
    """Checks compatibility status and details for two ingredients."""
    ing1 = clean_ingredient_name(ing1)
    ing2 = clean_ingredient_name(ing2)
    
    # Order ingredients alphabetically to ensure matching key works
    pair = tuple(sorted([ing1, ing2]))
    
    if pair in PAIR_COMPATIBILITY:
        return PAIR_COMPATIBILITY[pair]
        
    # Default fallback
    name1 = INGREDIENT_METADATA.get(ing1, {}).get("display_name", ing1.capitalize())
    name2 = INGREDIENT_METADATA.get(ing2, {}).get("display_name", ing2.capitalize())
    
    return {
        "status": "Compatible",
        "compatibility_index": 85,
        "description": f"{name1} and {name2} are generally compatible and can be used together in a standard skincare routine without issues. Always patch-test new combinations."
    }

from .customer_voice import get_product_customer_voice
from .ingredient_intel import clean_ingredient_name, get_ingredient_analytics
from .trend_intel import MOCK_TRENDS
from .data_loader import load_all_data


def get_product_details(product_id: str):
    data = load_all_data()
    products = data["products"]

    match = products[products["product_id"].astype(str) == str(product_id)]

    if match.empty:
        return None

    return match.iloc[0].to_dict()


def get_primary_ingredient(product):
    ingredients = [ing.strip() for ing in str(product.get("ingredients", "")).split(",")]

    for ing in ingredients:
        cleaned = clean_ingredient_name(ing)
        if cleaned in MOCK_TRENDS:
            return cleaned, MOCK_TRENDS[cleaned]["momentum"]

    return "niacinamide", 15.0


def get_ingredient_success(primary_ingredient):
    ingredients = get_ingredient_analytics()

    for item in ingredients:
        if item["key"] == primary_ingredient:
            return item["success_score"]

    return 50.0


def advise_budget_allocation(product_id: str):
    prod = get_product_details(product_id)

    if not prod:
        return None

    voice = get_product_customer_voice(product_id)

    if not voice:
        return {
            "product_id": product_id,
            "product_name": prod.get("product_name"),
            "brand_name": prod.get("brand_name"),
            "positive_sentiment_percent": 0.0,
            "negative_sentiment_percent": 0.0,
            "primary_ingredient": "unknown",
            "ingredient_success_score": 0.0,
            "trend_momentum_percent": 0.0,
            "recommendation": "Product Improvement",
            "reasoning": "No customer review data is available for this product. Focus on quality assurance and collect initial customer reviews before scaling marketing spend.",
            "allocation": {
                "marketing": 20,
                "product_improvement": 80
            },
            "recommended_actions": [
                "Collect initial reviews before launching a large influencer campaign.",
                "Run a small beta campaign to validate product-market fit."
            ],
            "estimates": {
                "roi": "Unknown",
                "cac": "Unknown",
                "conversion_rate": "Unknown"
            }
        }

    pos_sent = voice["sentiment_percentages"]["positive"]
    neg_sent = voice["sentiment_percentages"]["negative"]

    primary_ing, trend_momentum = get_primary_ingredient(prod)
    ingredient_success = get_ingredient_success(primary_ing)

    if pos_sent < 60.0:
        recommendation = "Product Improvement"
        reasoning = (
            f"Customer positive sentiment is only {pos_sent}%, which suggests that the product is not yet strong enough for aggressive marketing. "
            f"Before increasing ad or influencer spend, the brand should address product concerns such as irritation, texture, packaging, or formulation issues."
        )
        allocation = {
            "marketing": 25,
            "product_improvement": 75
        }

    elif ingredient_success < 60.0:
        recommendation = "Improve Formula Before Scaling"
        reasoning = (
            f"Customer sentiment is acceptable at {pos_sent}%, but the primary ingredient '{primary_ing.capitalize()}' has a lower success score of {ingredient_success}. "
            f"This suggests the product may need ingredient or formulation improvement before scaling marketing."
        )
        allocation = {
            "marketing": 40,
            "product_improvement": 60
        }

    elif trend_momentum < 0:
        recommendation = "Reposition & Diversify"
        reasoning = (
            f"Customer sentiment is strong at {pos_sent}%, and the ingredient success score is {ingredient_success}. "
            f"However, '{primary_ing.capitalize()}' is currently showing negative trend momentum ({trend_momentum}%). "
            f"Instead of simply increasing spend, reposition the campaign around broader benefits such as hydration, barrier repair, or sensitive-skin safety."
        )
        allocation = {
            "marketing": 50,
            "product_improvement": 50
        }

    else:
        recommendation = "Scale Marketing Spend"
        reasoning = (
            f"Customer sentiment is strong at {pos_sent}%, the ingredient success score is {ingredient_success}, "
            f"and '{primary_ing.capitalize()}' has positive trend momentum (+{trend_momentum}%). "
            f"This indicates strong product-market fit, so the brand can confidently increase influencer and social campaign spending."
        )
        allocation = {
            "marketing": 80,
            "product_improvement": 20
        }

    actions = []

    complaints = voice.get("complaints", {})

    if complaints.get("packaging_leak", {}).get("percentage", 0) > 10:
        actions.append("Fix leaking pump or bottle packaging before scaling campaigns.")

    if complaints.get("skin_irritation", {}).get("percentage", 0) > 10:
        actions.append("Add calming ingredients like Centella or Ceramides to reduce irritation complaints.")

    if complaints.get("greasy_residue", {}).get("percentage", 0) > 10:
        actions.append("Reformulate for a lighter texture to reduce greasy residue complaints.")

    if complaints.get("makeup_pilling", {}).get("percentage", 0) > 10:
        actions.append("Improve absorption speed to prevent pilling under makeup.")

    if not actions:
        if recommendation == "Product Improvement":
            actions.append("Audit negative reviews and identify the most repeated product flaw.")
        elif recommendation == "Improve Formula Before Scaling":
            actions.append("Improve the ingredient formulation before spending heavily on influencers.")
        elif recommendation == "Reposition & Diversify":
            actions.append("Reposition campaign messaging around stable benefits rather than a declining ingredient trend.")
        else:
            actions.append("Increase spend on Instagram Reels, TikTok-style short videos, and creator-led routines.")
            actions.append("Use social proof and authority-based messaging in campaign copy.")

    # Estimates based on recommendation
    if recommendation == "Scale Marketing Spend":
        roi_estimate = "250% - 350%"
        cac_estimate = "₹450 - ₹600"
        conversion_estimate = "4.5% - 6.0%"
    elif recommendation == "Reposition & Diversify":
        roi_estimate = "150% - 220%"
        cac_estimate = "₹700 - ₹900"
        conversion_estimate = "2.5% - 3.8%"
    elif recommendation == "Improve Formula Before Scaling":
        roi_estimate = "80% - 120%"
        cac_estimate = "₹1000 - ₹1300"
        conversion_estimate = "1.5% - 2.2%"
    else:
        roi_estimate = "< 50%"
        cac_estimate = "> ₹1500"
        conversion_estimate = "< 1.0%"

    return {
        "product_id": product_id,
        "product_name": prod.get("product_name"),
        "brand_name": prod.get("brand_name"),
        "positive_sentiment_percent": pos_sent,
        "negative_sentiment_percent": neg_sent,
        "primary_ingredient": primary_ing.capitalize(),
        "ingredient_success_score": ingredient_success,
        "trend_momentum_percent": trend_momentum,
        "recommendation": recommendation,
        "reasoning": reasoning,
        "allocation": allocation,
        "recommended_actions": actions,
        "estimates": {
            "roi": roi_estimate,
            "cac": cac_estimate,
            "conversion_rate": conversion_estimate
        }
    }
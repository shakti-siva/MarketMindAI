from .customer_voice import get_product_customer_voice
from .budget_advisor import advise_budget_allocation


def generate_marketing_consultation(product_id: str):

    voice = get_product_customer_voice(product_id)
    budget = advise_budget_allocation(product_id)

    if not voice or not budget:
        return {
            "status": "error",
            "message": "Product data not available."
        }

    pos = voice["sentiment_percentages"]["positive"]
    neg = voice["sentiment_percentages"]["negative"]

    recommendation = budget["recommendation"]

    if pos >= 80:
        market_fit = "Excellent"
    elif pos >= 65:
        market_fit = "Good"
    else:
        market_fit = "Needs Improvement"

    risks = []

    for complaint, data in voice["complaints"].items():
        if data["percentage"] > 10:
            risks.append(complaint)

    if not risks:
        risks.append("No major customer risks detected")

    campaign_idea = ""

    if recommendation == "Scale Marketing Spend":
        campaign_idea = (
            "Launch an Instagram Reels and TikTok creator campaign "
            "focused on before/after skincare transformations."
        )

    elif recommendation == "Reposition & Diversify":
        campaign_idea = (
            "Shift campaign messaging toward hydration, barrier repair "
            "and sensitive-skin benefits."
        )

    else:
        campaign_idea = (
            "Delay major marketing campaigns and focus on improving "
            "customer satisfaction first."
        )

    return {
        "product_name": budget["product_name"],
        "brand_name": budget["brand_name"],
        "market_fit_score": market_fit,
        "positive_sentiment": pos,
        "negative_sentiment": neg,
        "primary_ingredient": budget["primary_ingredient"],
        "recommendation": recommendation,
        "budget_split": budget["allocation"],
        "risks": risks,
        "campaign_idea": campaign_idea,
        "executive_summary": (
            f"{budget['product_name']} currently shows "
            f"{pos}% positive sentiment. "
            f"The product is categorized as '{market_fit}' "
            f"product-market fit and the recommended action "
            f"is '{recommendation}'."
        )
    }
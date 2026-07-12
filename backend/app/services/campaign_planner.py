import math


INFLUENCER_TIERS = {
    "nano": {
        "name": "Nano Influencers",
        "followers_range": "5k - 15k",
        "avg_cost": 5000,
        "avg_reach": 12000,
        "engagement_rate": 0.052,
        "description": "Best for authentic college/community-level promotion with high trust."
    },
    "micro": {
        "name": "Micro Influencers",
        "followers_range": "15k - 75k",
        "avg_cost": 20000,
        "avg_reach": 48000,
        "engagement_rate": 0.034,
        "description": "Best for credible skincare routines, product reviews, and mid-level reach."
    },
    "macro": {
        "name": "Macro Influencers",
        "followers_range": "75k - 300k+",
        "avg_cost": 60000,
        "avg_reach": 160000,
        "engagement_rate": 0.018,
        "description": "Best for large awareness campaigns and fast visibility."
    }
}


def generate_campaign_plan(product_name: str, product_type: str, target_audience: str, budget: float):
    budget = max(float(budget), 5000)

    nano_cost = INFLUENCER_TIERS["nano"]["avg_cost"]
    micro_cost = INFLUENCER_TIERS["micro"]["avg_cost"]
    macro_cost = INFLUENCER_TIERS["macro"]["avg_cost"]

    nano_count = 0
    micro_count = 0
    macro_count = 0

    if budget < 30000:
        nano_count = math.floor(budget / nano_cost)

    elif budget < 100000:
        nano_count = math.floor((budget * 0.7) / nano_cost)
        micro_count = math.floor((budget * 0.3) / micro_cost)

    elif budget < 300000:
        nano_count = math.floor((budget * 0.5) / nano_cost)
        micro_count = math.floor((budget * 0.5) / micro_cost)

    else:
        nano_count = math.floor((budget * 0.25) / nano_cost)
        micro_count = math.floor((budget * 0.45) / micro_cost)
        macro_count = math.floor((budget * 0.30) / macro_cost)

    total_spent = (
        nano_count * nano_cost
        + micro_count * micro_cost
        + macro_count * macro_cost
    )

    remaining_buffer = budget - total_spent

    expected_reach = (
        nano_count * INFLUENCER_TIERS["nano"]["avg_reach"]
        + micro_count * INFLUENCER_TIERS["micro"]["avg_reach"]
        + macro_count * INFLUENCER_TIERS["macro"]["avg_reach"]
    )

    expected_engagement = int(
        (nano_count * INFLUENCER_TIERS["nano"]["avg_reach"] * INFLUENCER_TIERS["nano"]["engagement_rate"])
        + (micro_count * INFLUENCER_TIERS["micro"]["avg_reach"] * INFLUENCER_TIERS["micro"]["engagement_rate"])
        + (macro_count * INFLUENCER_TIERS["macro"]["avg_reach"] * INFLUENCER_TIERS["macro"]["engagement_rate"])
    )

    avg_engagement_rate = round(
        (expected_engagement / max(1, expected_reach)) * 100,
        1
    )

    reels = nano_count + micro_count + macro_count
    stories = (nano_count * 2) + (micro_count * 3) + (macro_count * 4)
    posts = micro_count + macro_count

    if "college" in target_audience.lower() or "gen z" in target_audience.lower() or "teen" in target_audience.lower():
        strategy_focus = (
            "Use nano influencers heavily because college audiences trust relatable creators more than polished ads."
        )
    elif "professional" in target_audience.lower() or "millennial" in target_audience.lower():
        strategy_focus = (
            "Use micro influencers for educational skincare routines, ingredient explanations, and credible product reviews."
        )
    else:
        strategy_focus = (
            "Use a balanced creator mix focused on awareness, product education, and social proof."
        )

    if "serum" in product_type.lower() or "treatment" in product_type.lower():
        content_angle = (
            "Focus on active ingredients, visible results, before-after progress, and dermatologist-style authority messaging."
        )
    elif "cleanser" in product_type.lower():
        content_angle = (
            "Focus on daily routine usage, gentle skin feel, acne-safe cleansing, and honest texture reviews."
        )
    elif "moisturizer" in product_type.lower() or "cream" in product_type.lower():
        content_angle = (
            "Focus on hydration, barrier repair, glow, and non-greasy texture."
        )
    else:
        content_angle = (
            "Focus on honest usage experience, skin compatibility, and routine integration."
        )

    # Platform distribution based on target audience
    if "gen z" in target_audience.lower() or "teen" in target_audience.lower() or "college" in target_audience.lower():
        platform_split = {"Instagram": 30, "TikTok": 60, "YouTube Shorts": 10}
    elif "millennial" in target_audience.lower() or "professional" in target_audience.lower():
        platform_split = {"Instagram": 50, "TikTok": 35, "YouTube Shorts": 15}
    else:
        platform_split = {"Instagram": 40, "TikTok": 45, "YouTube Shorts": 15}
        
    campaign_duration = "3-4 Weeks" if budget < 50000 else "6-8 Weeks"
    best_posting_times = ["Tuesdays 5 PM", "Thursdays 7 PM", "Sundays 11 AM"]

    cpm = round((total_spent / max(1, expected_reach)) * 1000, 2)
    cpe = round(total_spent / max(1, expected_engagement), 2)

    return {
        "campaign_metadata": {
            "product_name": product_name,
            "product_type": product_type,
            "target_audience": target_audience,
            "allocated_budget": budget
        },
        "financial_summary": {
            "total_budget": budget,
            "total_spent": total_spent,
            "remaining_buffer": remaining_buffer,
            "average_cost_per_creator": round(total_spent / max(1, nano_count + micro_count + macro_count), 1)
        },
        "influencer_mix": {
            "nano": {
                "count": nano_count,
                "followers_range": INFLUENCER_TIERS["nano"]["followers_range"],
                "pay_each": nano_cost,
                "total_cost": nano_count * nano_cost,
                "description": INFLUENCER_TIERS["nano"]["description"]
            },
            "micro": {
                "count": micro_count,
                "followers_range": INFLUENCER_TIERS["micro"]["followers_range"],
                "pay_each": micro_cost,
                "total_cost": micro_count * micro_cost,
                "description": INFLUENCER_TIERS["micro"]["description"]
            },
            "macro": {
                "count": macro_count,
                "followers_range": INFLUENCER_TIERS["macro"]["followers_range"],
                "pay_each": macro_cost,
                "total_cost": macro_count * macro_cost,
                "description": INFLUENCER_TIERS["macro"]["description"]
            }
        },
        "content_distribution": {
            "reels": reels,
            "stories": stories,
            "posts": posts,
            "recommendation": (
                f"Ask each creator to make 1 Reel. Nano creators should add 2 Stories each, "
                f"while Micro/Macro creators should add more detailed review content."
            )
        },
        "logistics": {
            "platform_split": platform_split,
            "campaign_duration": campaign_duration,
            "best_posting_times": best_posting_times
        },
        "projections": {
            "expected_reach": expected_reach,
            "expected_engagement": expected_engagement,
            "avg_engagement_rate_percent": avg_engagement_rate,
            "estimated_cpm": cpm,
            "estimated_cpe": cpe
        },
        "strategy": {
            "focus": strategy_focus,
            "content_angle": content_angle
        }
    }
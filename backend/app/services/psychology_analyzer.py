import re

PSYCHOLOGICAL_TRIGGERS = {
    "Authority": {
        "keywords": [
            r"dermatologist", r"clinical", r"science", r"doctor", r"approved", r"recommended", 
            r"formula", r"expert", r"lab", r"test", r"study", r"proven", r"patent", r"medical"
        ],
        "description": "Establishes credibility and trust through professional, clinical, or scientific endorsement.",
        "tip": "To boost Authority: reference clinical test numbers (e.g. '98% saw improvement') or expert credentials."
    },
    "Scarcity": {
        "keywords": [
            r"limited edition", r"while stock lasts", r"few left", r"only \d+", r"vault", 
            r"restock", r"batch", r"exclusive", r"rare", r"selling out", r"almost gone"
        ],
        "description": "Creates a perception of high value by making the product seem rare or hard to obtain.",
        "tip": "To boost Scarcity: emphasize small-batch manufacturing or exclusive product variants."
    },
    "Urgency": {
        "keywords": [
            r"hurry", r"ends tonight", r"flash sale", r"limited time", r"fast", r"now", 
            r"today", r"hours left", r"don't wait", r"expires", r"clock is ticking", r"quick"
        ],
        "description": "Encourages immediate action by imposing a strict time constraint on the buyer.",
        "tip": "To boost Urgency: add time-bound offers or countdown timers to campaigns."
    },
    "Social Proof": {
        "keywords": [
            r"best seller", r"viral", r"tiktok", r"reviews", r"rated", r"\d+k? star", 
            r"cult favorite", r"people love", r"award winning", r"recommend", r"favorite", r"popular"
        ],
        "description": "Leverages the actions and approvals of others to validate the buyer's purchase decision.",
        "tip": "To boost Social Proof: display average ratings or aggregate customer review quotes."
    },
    "FOMO": {
        "keywords": [
            r"don't miss", r"everyone is", r"next big thing", r"join the waitlist", r"secret", 
            r"hype", r"be the first", r"insider", r"exclusive access", r"trend"
        ],
        "description": "Fear of Missing Out triggers the desire to belong and avoid missing a social trend.",
        "tip": "To boost FOMO: focus on community adoption (e.g., 'Join 50,000+ skincare enthusiasts')."
    }
}

def analyze_copy_psychology(text: str):
    """Analyzes text copy and scores the presence of five psychological triggers."""
    text_lower = text.lower()
    scores = {}
    matched_words = {}
    
    # Calculate score based on keyword match frequencies
    for trigger, info in PSYCHOLOGICAL_TRIGGERS.items():
        matches = []
        for kw in info["keywords"]:
            found = re.findall(kw, text_lower)
            if found:
                matches.extend(found)
                
        # Calculate raw score (cap at 100)
        score = min(100, len(matches) * 25 + (20 if len(matches) > 0 else 0))
        scores[trigger] = score
        matched_words[trigger] = list(set(matches))
        
    # Calculate Overall Persuasion Score
    # A great copy usually leverages 2-3 triggers heavily.
    total_raw = sum(scores.values())
    overall_score = min(100, int((total_raw / 250) * 100))
    if overall_score == 0 and len(text_lower) > 20:
        overall_score = 15 # Give some baseline for just having text
        
    # Determine dominant trigger
    dominant_trigger = max(scores, key=scores.get)
    if scores[dominant_trigger] == 0:
        dominant_trigger = "None Detected"
        suggestion = "Your copy feels neutral. Consider adding elements of Social Proof ('Over 10,000 happy customers') or Authority ('Clinically tested and dermatologist approved') to make it persuasive."
    else:
        suggestion = PSYCHOLOGICAL_TRIGGERS[dominant_trigger]["tip"]
        
    # Direct copywriter recommendations
    recommendations = []
    if scores.get("Authority", 0) < 30:
        recommendations.append("Lacking clinical backing. Add phrases like 'Dermatologist tested' or 'Clinically proven'.")
    if scores.get("Social Proof", 0) < 30:
        recommendations.append("Missing customer validation. Try adding '5-star rated' or 'Cult favorite'.")
    if scores.get("Urgency", 0) < 30 and scores.get("Scarcity", 0) < 30:
        recommendations.append("No immediate reason to buy. Consider a 'Limited time' offer or 'Almost gone' warning.")
        
    if not recommendations:
        recommendations.append("Excellent psychological balance! Monitor conversion rates and A/B test the headline.")
        
    # Detailed breakdown
    breakdown = []
    for trigger, score in scores.items():
        breakdown.append({
            "trigger": trigger,
            "score": score,
            "description": PSYCHOLOGICAL_TRIGGERS[trigger]["description"],
            "matches": matched_words[trigger]
        })
        
    return {
        "text": text,
        "scores": scores,
        "overall_score": overall_score,
        "dominant_trigger": dominant_trigger,
        "suggestion": suggestion,
        "recommendations": recommendations,
        "breakdown": breakdown
    }

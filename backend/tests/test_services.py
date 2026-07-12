import pytest
import os
import sys

# Add backend directory to path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.customer_voice import get_customer_voice_dashboard
from app.services.ingredient_intel import check_pair_compatibility, get_ingredient_analytics
from app.services.psychology_analyzer import analyze_copy_psychology
from app.services.campaign_planner import generate_campaign_plan
from app.services.budget_advisor import advise_budget_allocation
from app.services.data_loader import load_datasets

def test_data_loader_initialization():
    products, reviews = load_datasets()
    assert not products.empty
    assert not reviews.empty
    assert "product_id" in products.columns
    assert "review_text" in reviews.columns

def test_customer_voice():
    dashboard = get_customer_voice_dashboard()
    assert "total_reviews" in dashboard
    assert dashboard["total_reviews"] > 0
    assert "sentiment_distribution" in dashboard
    assert "complaints" in dashboard

def test_ingredient_intel():
    analytics = get_ingredient_analytics()
    assert len(analytics) > 0
    assert "success_score" in analytics[0]
    
    # Check pairing
    pairing = check_pair_compatibility("niacinamide", "zinc pca")
    assert pairing["status"] == "Synergistic"
    assert pairing["compatibility_index"] > 90

def test_psychology_analyzer():
    copy = "Dermatologist recommended and clinically proven formulation. Limited edition, buy today!"
    analysis = analyze_copy_psychology(copy)
    assert analysis["dominant_trigger"] in ["Authority", "Urgency", "Scarcity"]
    assert analysis["scores"]["Authority"] > 0
    assert analysis["scores"]["Scarcity"] > 0

def test_campaign_planner():
    plan = generate_campaign_plan(
        product_name="Youth Serum",
        product_type="Treatments",
        target_audience="Gen Z",
        budget=100000
    )
    assert plan["financial_summary"]["total_spent"] <= 100000
    assert plan["projections"]["expected_reach"] > 0
    assert plan["influencer_mix"]["nano"]["count"] > 0

def test_budget_advisor():
    # Test P001 which is in MOCK_PRODUCTS
    advice = advise_budget_allocation("P001")
    assert advice is not None
    assert "recommendation" in advice
    assert "allocation" in advice
    assert sum(advice["allocation"].values()) == 100

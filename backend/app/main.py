from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd

# Import services
from .config import APP_NAME, VERSION
from .services.data_loader import load_all_data
from .services.customer_voice import get_customer_voice_dashboard, get_product_customer_voice
from .services.ingredient_intel import get_ingredient_analytics, check_pair_compatibility
from .services.trend_intel import get_trend_intelligence, get_reddit_skincare_topics
from .services.psychology_analyzer import analyze_copy_psychology
from .services.campaign_planner import generate_campaign_plan
from .services.budget_advisor import advise_budget_allocation
from .services.ai_consultant import generate_marketing_consultation

app = FastAPI(title=APP_NAME, version=VERSION)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For local development ease
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event to verify/load data
@app.on_event("startup")
def startup_event():
    print("Pre-loading datasets...")
    load_all_data()

# Pydantic models for POST requests
class CopyAnalyzeRequest(BaseModel):
    text: str

class CampaignPlanRequest(BaseModel):
    product_name: str
    product_type: str
    target_audience: str
    budget: float

class ConsultRequest(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to MarketMind AI API", "version": VERSION}

@app.get("/api/products")
def list_products():
    data = load_all_data()

    products = data["products"].copy()
    reviews = data["reviews"].copy()

    # Count reviews for each product
    review_counts = (
        reviews.groupby("product_id")
        .size()
        .reset_index(name="review_count")
    )

    # Merge review counts into products
    products = products.merge(
        review_counts,
        on="product_id",
        how="left"
    )

    products["review_count"] = products["review_count"].fillna(0)

    # Architectural fix: Filter products that actually have reviews and sort by popularity
    products = products[products["review_count"] > 0]
    products = products.sort_values(by="review_count", ascending=False)

    return products.head(300).fillna("").to_dict(orient="records")

@app.get("/api/customer-voice")
def customer_voice_global():
    """Global customer sentiment, complaints, and praise dashboard."""
    return get_customer_voice_dashboard()

@app.get("/api/customer-voice/{product_id}")
def customer_voice_product(product_id: str):
    """Detailed review sentiment and complaint report for a specific product."""
    data = get_product_customer_voice(product_id)
    if not data:
        raise HTTPException(status_code=404, detail="Product not found or has no reviews")
    return data

@app.get("/api/ingredients")
def ingredient_analytics():
    """Rankings, popularity, and success scores of skincare ingredients."""
    return get_ingredient_analytics()

@app.get("/api/ingredients/compatibility")
def ingredient_compatibility(ing1: str = Query(...), ing2: str = Query(...)):
    """Determines compatibility status and details for two ingredients."""
    return check_pair_compatibility(ing1, ing2)

@app.get("/api/trends")
def trend_intelligence():
    """Google Trends and Reddit statistics with monthly momentum."""
    return get_trend_intelligence()

@app.get("/api/trends/reddit-topics")
def reddit_topics():
    """Simulated skincare subreddit hot discussion clusters."""
    return get_reddit_skincare_topics()

@app.post("/api/psychology/analyze")
def analyze_psychology(payload: CopyAnalyzeRequest):
    """Analyzes copy for psychological triggers."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text copy cannot be empty")
    return analyze_copy_psychology(payload.text)

@app.post("/api/campaign/plan")
def campaign_planner(payload: CampaignPlanRequest):
    """Calculates influencer distribution and overall marketing strategy."""
    return generate_campaign_plan(
        product_name=payload.product_name,
        product_type=payload.product_type,
        target_audience=payload.target_audience,
        budget=payload.budget
    )

@app.get("/api/budget/advise/{product_id}")
def budget_advisor(product_id: str):
    """Recommends spend allocation between Marketing and Product Improvement."""
    advice = advise_budget_allocation(product_id)
    if not advice:
        raise HTTPException(status_code=404, detail="Product not found")
    return advice

@app.post("/api/consult")
def consult_ai(payload: ConsultRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    response = generate_marketing_consultation(payload.query)

    return response

import os
import psutil
import tracemalloc

tracemalloc.start()

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Import services
from .config import APP_NAME, VERSION
from .services.data_loader import get_products
from .services.customer_voice import get_customer_voice_dashboard, get_product_customer_voice
from .services.ingredient_intel import get_ingredient_analytics, check_pair_compatibility
from .services.trend_intel import get_trend_intelligence, get_reddit_skincare_topics
from .services.psychology_analyzer import analyze_copy_psychology
from .services.campaign_planner import generate_campaign_plan
from .services.budget_advisor import advise_budget_allocation
from .services.ai_consultant import generate_marketing_consultation

def log_memory(context: str, stage: str):
    process = psutil.Process(os.getpid())
    rss_mb = process.memory_info().rss / 1024 / 1024
    print(f"[{context}] {stage} - RSS: {rss_mb:.2f} MB")

def log_tracemalloc(context: str):
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")
    print(f"[{context}] Top 5 memory allocations:")
    for stat in top_stats[:5]:
        print(stat)

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
    log_memory("Startup Hook", "Before hook")
    print("Backend initialized.")
    log_memory("Startup Hook", "After hook")
    log_tracemalloc("Startup Hook")

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
    log_memory("/api/products", "Before query")
    products = get_products()
    log_memory("/api/products", "After query / Before processing")
    
    # Add a safe 'review_count' field for the frontend if they expect it
    for p in products:
        p["review_count"] = float(p.get("reviews", 0))
        # Ensure NaN values are replaced with empty strings for JSON serialization
        for k, v in p.items():
            if v is None or (isinstance(v, float) and v != v):
                p[k] = ""
                
    log_memory("/api/products", "After processing / Before return JSON")
    log_tracemalloc("/api/products")
    return products[:300]

@app.get("/api/customer-voice")
def customer_voice_global():
    """Global customer sentiment, complaints, and praise dashboard."""
    log_memory("/api/customer-voice", "Before query")
    data = get_customer_voice_dashboard()
    log_memory("/api/customer-voice", "After query and processing / Before return JSON")
    log_tracemalloc("/api/customer-voice")
    return data

@app.get("/api/customer-voice/{product_id}")
def customer_voice_product(product_id: str):
    """Detailed review sentiment and complaint report for a specific product."""
    log_memory(f"/api/customer-voice/{product_id}", "Before query")
    data = get_product_customer_voice(product_id)
    log_memory(f"/api/customer-voice/{product_id}", "After query and processing / Before return JSON")
    log_tracemalloc(f"/api/customer-voice/{product_id}")
    if not data:
        raise HTTPException(status_code=404, detail="Product not found or has no reviews")
    return data

@app.get("/api/ingredients")
def ingredient_analytics():
    """Rankings, popularity, and success scores of skincare ingredients."""
    log_memory("/api/ingredients", "Before query")
    data = get_ingredient_analytics()
    log_memory("/api/ingredients", "After query and processing / Before return JSON")
    log_tracemalloc("/api/ingredients")
    return data

@app.get("/api/ingredients/compatibility")
def ingredient_compatibility(ing1: str = Query(...), ing2: str = Query(...)):
    """Determines compatibility status and details for two ingredients."""
    return check_pair_compatibility(ing1, ing2)

@app.get("/api/trends")
def trend_intelligence():
    """Google Trends and Reddit statistics with monthly momentum."""
    log_memory("/api/trends", "Before query")
    data = get_trend_intelligence()
    log_memory("/api/trends", "After query and processing / Before return JSON")
    log_tracemalloc("/api/trends")
    return data

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
    log_memory(f"/api/budget/advise/{product_id}", "Before query")
    advice = advise_budget_allocation(product_id)
    log_memory(f"/api/budget/advise/{product_id}", "After query and processing / Before return JSON")
    log_tracemalloc(f"/api/budget/advise/{product_id}")
    if not advice:
        raise HTTPException(status_code=404, detail="Product not found")
    return advice

@app.post("/api/consult")
def consult_ai(payload: ConsultRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    response = generate_marketing_consultation(payload.query)

    return response

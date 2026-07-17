from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import APP_NAME, VERSION
from .services.data_loader import get_products
from .services.customer_voice import get_customer_voice_dashboard, get_product_customer_voice
from .services.ingredient_intel import get_ingredient_analytics, check_pair_compatibility
from .services.trend_intel import get_trend_intelligence, get_reddit_skincare_topics
from .services.psychology_analyzer import analyze_copy_psychology
from .services.campaign_planner import generate_campaign_plan
from .services.budget_advisor import advise_budget_allocation
from .services.llm_consultant import consult_marketing


app = FastAPI(title=APP_NAME, version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class CopyAnalyzeRequest(BaseModel):
    text: str


class CampaignPlanRequest(BaseModel):
    product_name: str
    product_type: str
    target_audience: str
    budget: float


class ConsultRequest(BaseModel):
    query: str


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to MarketMind AI API", "version": VERSION}


@app.get("/api/products")
def list_products():
    """Returns all products ordered by review count."""
    products = get_products()

    # Sanitise NaN / None values so FastAPI can serialise the response
    for p in products:
        for k, v in p.items():
            if v is None or (isinstance(v, float) and v != v):
                p[k] = ""

    return products[:300]


@app.get("/api/customer-voice")
def customer_voice_global():
    """Global sentiment, complaints, and praise dashboard across all products."""
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
    """Rankings, popularity, and success scores of key skincare ingredients."""
    return get_ingredient_analytics()


@app.get("/api/ingredients/compatibility")
def ingredient_compatibility(ing1: str = Query(...), ing2: str = Query(...)):
    """Compatibility and synergy analysis for two ingredients."""
    return check_pair_compatibility(ing1, ing2)


@app.get("/api/trends")
def trend_intelligence():
    """Google Trends data with monthly momentum for top skincare ingredients."""
    return get_trend_intelligence()


@app.get("/api/trends/reddit-topics")
def reddit_topics():
    """Simulated skincare subreddit hot discussion clusters."""
    return get_reddit_skincare_topics()


@app.post("/api/psychology/analyze")
def analyze_psychology(payload: CopyAnalyzeRequest):
    """Scores marketing copy for five psychological persuasion triggers."""
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text copy cannot be empty")
    return analyze_copy_psychology(payload.text)


@app.post("/api/campaign/plan")
def campaign_planner(payload: CampaignPlanRequest):
    """Generates an influencer campaign plan with reach and cost projections."""
    return generate_campaign_plan(
        product_name=payload.product_name,
        product_type=payload.product_type,
        target_audience=payload.target_audience,
        budget=payload.budget,
    )


@app.get("/api/budget/advise/{product_id}")
def budget_advisor(product_id: str):
    """Recommends marketing vs. product-improvement spend allocation."""
    advice = advise_budget_allocation(product_id)
    if not advice:
        raise HTTPException(status_code=404, detail="Product not found")
    return advice


@app.post("/api/consult")
def consult_ai(payload: ConsultRequest):
    """AI marketing consultant — answers strategy questions about the platform data."""
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    answer = consult_marketing(payload.query)
    return {"response": answer}

from app.services.trend_intel import get_trend_intelligence

trends = get_trend_intelligence()

for trend in trends:
    print(trend["name"], trend["momentum"], trend["google_interest"])
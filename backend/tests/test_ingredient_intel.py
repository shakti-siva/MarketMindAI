from app.services.ingredient_intel import get_ingredient_analytics

results = get_ingredient_analytics()

for item in results:
    print(item)
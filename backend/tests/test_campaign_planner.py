from app.services.campaign_planner import generate_campaign_plan

result = generate_campaign_plan(
    product_name="Niacinamide Serum",
    product_type="Serum",
    target_audience="College girls",
    budget=100000
)

print(result)
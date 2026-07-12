from app.services.budget_advisor import advise_budget_allocation

product_id = "P504322"

result = advise_budget_allocation(product_id)

print(result)
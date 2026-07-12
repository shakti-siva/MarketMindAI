from app.services.data_loader import load_all_data

data = load_all_data()

print("Products:", len(data["products"]))
print("Reviews:", len(data["reviews"]))
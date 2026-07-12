import os
import pandas as pd
import random
from pathlib import Path
from ..config import DATA_DIR

# Sample skincare products
MOCK_PRODUCTS = [
    {
        "product_id": "P001",
        "product_name": "Ultra Hydrating Water Cream",
        "brand_name": "LumiSkin",
        "price_usd": 38.00,
        "ingredients": "Water, Squalane, Glycerin, Hyaluronic Acid, Ceramides, Niacinamide, Phenoxyethanol",
        "rating": 4.6,
        "loves_count": 25000,
        "category": "Moisturizers"
    },
    {
        "product_id": "P002",
        "product_name": "Retinol Youth Renewal Serum",
        "brand_name": "Dermacell",
        "price_usd": 85.00,
        "ingredients": "Water, Glycerin, Retinol, Ceramide NP, Hyaluronic Acid, Peptides, Tocopherol (Vitamin E)",
        "rating": 4.2,
        "loves_count": 42000,
        "category": "Treatments"
    },
    {
        "product_id": "P003",
        "product_name": "10% Niacinamide Oil-Control Serum",
        "brand_name": "GlowCo",
        "price_usd": 28.00,
        "ingredients": "Water, Niacinamide, Zinc PCA, Hyaluronic Acid, Phenoxyethanol, Ethylhexylglycerin",
        "rating": 3.9,
        "loves_count": 18000,
        "category": "Treatments"
    },
    {
        "product_id": "P004",
        "product_name": "C-Bright Radiance Booster",
        "brand_name": "Aura Organics",
        "price_usd": 52.00,
        "ingredients": "Water, Ascorbic Acid (Vitamin C), Ferulic Acid, Vitamin E, Squalane, Citrus Aurantium Dulcis Fruit Extract",
        "rating": 4.1,
        "loves_count": 15000,
        "category": "Treatments"
    },
    {
        "product_id": "P005",
        "product_name": "Salicylic Acid Pore Clearing Gel",
        "brand_name": "ClearSkin Labs",
        "price_usd": 24.00,
        "ingredients": "Water, Salicylic Acid, Tea Tree Oil, Centella Asiatica Extract, Glycerin, Alcohol Denat",
        "rating": 4.3,
        "loves_count": 29000,
        "category": "Treatments"
    },
    {
        "product_id": "P006",
        "product_name": "Ceramide Barrier Defense Balm",
        "brand_name": "Dermacell",
        "price_usd": 45.00,
        "ingredients": "Water, Caprylic/Capric Triglyceride, Ceramide NP, Ceramide AP, Ceramide EOP, Phytosphingosine, Cholesterol, Shea Butter",
        "rating": 4.8,
        "loves_count": 31000,
        "category": "Moisturizers"
    },
    {
        "product_id": "P007",
        "product_name": "Centella Soothing Gel Cleanser",
        "brand_name": "LumiSkin",
        "price_usd": 22.00,
        "ingredients": "Water, Cocamidopropyl Betaine, Glycerin, Centella Asiatica Extract, Green Tea Extract, Panthenol",
        "rating": 4.5,
        "loves_count": 12000,
        "category": "Cleansers"
    },
    {
        "product_id": "P008",
        "product_name": "Peptide Plumping Night Cream",
        "brand_name": "GlowCo",
        "price_usd": 64.00,
        "ingredients": "Water, Glycerin, Acetyl Hexapeptide-8, Palmitoyl Tripeptide-1, Ceramides, Squalane, Jojoba Oil",
        "rating": 4.7,
        "loves_count": 22000,
        "category": "Moisturizers"
    }
]

MOCK_PRAISE = [
    "Absolutely love this! It makes my skin feel incredibly hydrated and soft.",
    "My skin is glowing after using this for a week. Highly recommend!",
    "It cleared my acne and reduced the redness significantly. Will buy again.",
    "Absorbs so quickly without leaving any greasy residue. Perfect for makeup base.",
    "My skin looks so plump and healthy! The fine lines around my eyes are fading.",
    "The ingredients are amazing and it didn't irritate my sensitive skin.",
    "Wonderful product, my holy grail moisturizer. Gives a beautiful dewy finish.",
    "Great product, worth every penny. My skin barrier has never felt stronger."
]

MOCK_COMPLAINTS = [
    "Terrible packaging! The pump broke after two uses and it leaks everywhere.",
    "Broke me out in tiny bumps all over my forehead. Skin became very dry and irritated.",
    "It left a very oily, greasy residue on my skin. Definitely not for oily skin types.",
    "It started pilling under my makeup and SPF, creating tiny white flakes.",
    "This smells awful! Like plastic or chemicals. I couldn't stand it on my face.",
    "Made my skin turn red and blotchy instantly. Beware if you have sensitive skin.",
    "Not hydrating at all. My skin felt tight and flaky an hour after applying.",
    "The product itself is okay, but the packaging leak wasted half of the serum."
]

SKIN_TYPES = ["dry", "oily", "combination", "normal"]
SKIN_TONES = ["fair", "light", "medium", "tan", "deep"]

def generate_mock_data(force=False):
    products_file = DATA_DIR / "products_info.csv"
    reviews_file = DATA_DIR / "reviews_0_250.csv"
    
    # Check if files already exist
    if not force and products_file.exists() and reviews_file.exists():
        print("Mock datasets already exist. Skipping generation.")
        return False
        
    print("Generating high-fidelity mock Sephora dataset...")
    
    # 1. Generate Products Info CSV
    df_products = pd.DataFrame(MOCK_PRODUCTS)
    df_products.to_csv(products_file, index=False)
    
    # 2. Generate Skincare Reviews CSV
    reviews = []
    
    # Generate around 150 reviews per product (total ~1200 reviews)
    review_id_counter = 1
    for p in MOCK_PRODUCTS:
        p_id = p["product_id"]
        base_rating = p["rating"]
        
        # We want reviews to roughly average out to the product's base rating
        for _ in range(150):
            # Roll a rating based on product quality
            if base_rating >= 4.5:
                rating = random.choices([5, 4, 3, 2, 1], weights=[60, 25, 10, 3, 2])[0]
            elif base_rating >= 4.0:
                rating = random.choices([5, 4, 3, 2, 1], weights=[45, 35, 12, 5, 3])[0]
            else:
                rating = random.choices([5, 4, 3, 2, 1], weights=[30, 35, 20, 10, 5])[0]
            
            # Select praise or complaint text based on rating
            if rating >= 4:
                text = random.choice(MOCK_PRAISE)
                # Add some variety
                if random.random() > 0.5:
                    text += " It's become a staple in my daily skincare routine."
                is_rec = 1.0
                title = "Amazing!" if rating == 5 else "Really good product"
            elif rating == 3:
                text = "It's average. Didn't cause breakouts but didn't see massive results either. Average hydration."
                is_rec = 0.5
                title = "It's okay"
            else:
                text = random.choice(MOCK_COMPLAINTS)
                is_rec = 0.0
                title = "Disappointed" if rating == 2 else "Do not buy!"
                
            # Randomize attributes
            skin_type = random.choice(SKIN_TYPES)
            skin_tone = random.choice(SKIN_TONES)
            feedback = random.randint(0, 45)
            
            reviews.append({
                "product_id": p_id,
                "author_id": f"user_{random.randint(1000, 9999)}",
                "rating": rating,
                "review_text": text,
                "review_title": title,
                "skin_type": skin_type,
                "skin_tone": skin_tone,
                "is_recommended": is_rec,
                "feedback_count": feedback
            })
            review_id_counter += 1
            
    df_reviews = pd.DataFrame(reviews)
    df_reviews.to_csv(reviews_file, index=False)
    print(f"Generated {len(df_products)} products and {len(df_reviews)} reviews.")
    return True

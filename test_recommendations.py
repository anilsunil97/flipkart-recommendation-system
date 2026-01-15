"""
Test script for recommendation system
"""
from recommendation_engine import FlipkartRecommendationEngine
import pandas as pd

def test_recommendations():
    print("="*60)
    print("Testing Flipkart Recommendation System")
    print("="*60)
    
    # Initialize engine
    engine = FlipkartRecommendationEngine()
    
    try:
        engine.load_models()
        print("✅ Models loaded successfully\n")
    except:
        print("⚠️ Models not found. Please run data_generator.py and recommendation_engine.py first")
        return
    
    # Test 1: User Recommendations
    print("\n" + "="*60)
    print("TEST 1: Personalized User Recommendations")
    print("="*60)
    
    test_user = engine.users_df.iloc[0]['user_id']
    user_info = engine.users_df[engine.users_df['user_id'] == test_user].iloc[0]
    
    print(f"\nUser: {test_user}")
    print(f"Location: {user_info['location']}, Age: {user_info['age']}, Gender: {user_info['gender']}")
    
    print("\n🔹 Hybrid Recommendations:")
    hybrid_recs = engine.get_hybrid_recommendations(test_user, 5)
    products = engine.get_product_details(hybrid_recs)
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['product_name']}")
        print(f"   ₹{p['price']} | {p['category']} | ⭐{p['rating']}")
    
    print("\n🔹 Collaborative Filtering Recommendations:")
    collab_recs = engine.get_collaborative_recommendations(test_user, 5)
    products = engine.get_product_details(collab_recs)
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['product_name']}")
        print(f"   ₹{p['price']} | {p['category']} | ⭐{p['rating']}")
    
    # Test 2: Similar Products
    print("\n" + "="*60)
    print("TEST 2: Similar Product Recommendations")
    print("="*60)
    
    test_product_id = engine.products_df.iloc[0]['product_id']
    test_product = engine.products_df[engine.products_df['product_id'] == test_product_id].iloc[0]
    
    print(f"\nOriginal Product: {test_product['product_name']}")
    print(f"Category: {test_product['category']}, Brand: {test_product['brand']}")
    print(f"Price: ₹{test_product['price']}, Rating: ⭐{test_product['rating']}")
    
    print("\n🔹 Similar Products:")
    similar_recs = engine.get_content_based_recommendations(test_product_id, 5)
    products = engine.get_product_details(similar_recs)
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['product_name']}")
        print(f"   ₹{p['price']} | {p['category']} | ⭐{p['rating']}")
    
    # Test 3: Category Recommendations
    print("\n" + "="*60)
    print("TEST 3: Category-Based Recommendations")
    print("="*60)
    
    test_category = 'Electronics'
    print(f"\nCategory: {test_category}")
    
    print("\n🔹 Top Products:")
    category_recs = engine.get_category_recommendations(test_category, 5)
    products = engine.get_product_details(category_recs)
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['product_name']}")
        print(f"   ₹{p['price']} | Brand: {p['brand']} | ⭐{p['rating']}")
    
    # Test 4: Popular Products
    print("\n" + "="*60)
    print("TEST 4: Popular Products")
    print("="*60)
    
    print("\n🔹 Most Popular:")
    popular_recs = engine.get_popular_products(5)
    products = engine.get_product_details(popular_recs)
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['product_name']}")
        print(f"   ₹{p['price']} | {p['category']} | ⭐{p['rating']} ({p['num_reviews']} reviews)")
    
    # Statistics
    print("\n" + "="*60)
    print("SYSTEM STATISTICS")
    print("="*60)
    
    print(f"\n📊 Total Products: {len(engine.products_df)}")
    print(f"👥 Total Users: {len(engine.users_df)}")
    print(f"🔄 Total Interactions: {len(engine.interactions_df)}")
    print(f"📂 Categories: {engine.products_df['category'].nunique()}")
    print(f"🏷️ Brands: {engine.products_df['brand'].nunique()}")
    print(f"⭐ Average Rating: {engine.products_df['rating'].mean():.2f}")
    
    purchases = len(engine.interactions_df[engine.interactions_df['interaction_type'] == 'purchase'])
    print(f"🛒 Total Purchases: {purchases}")
    
    print("\n" + "="*60)
    print("✅ All tests completed successfully!")
    print("="*60)

if __name__ == "__main__":
    test_recommendations()
"""
Quick demo of the Flipkart Recommendation API
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def demo_stats():
    """Show system statistics"""
    print_section("📊 SYSTEM STATISTICS")
    response = requests.get(f"{BASE_URL}/stats")
    stats = response.json()
    
    print(f"\n✅ Total Products: {stats['total_products']}")
    print(f"✅ Total Users: {stats['total_users']}")
    print(f"✅ Total Interactions: {stats['total_interactions']}")
    print(f"✅ Categories: {stats['categories']}")
    print(f"✅ Brands: {stats['brands']}")
    print(f"✅ Average Rating: {stats['avg_rating']}⭐")
    print(f"✅ Total Purchases: {stats['total_purchases']}")

def demo_user_recommendations():
    """Show personalized recommendations"""
    print_section("👤 PERSONALIZED RECOMMENDATIONS FOR USER0001")
    
    response = requests.get(
        f"{BASE_URL}/recommend/user/USER0001",
        params={'method': 'hybrid', 'n': 5}
    )
    data = response.json()
    
    print(f"\nMethod: {data['method'].upper()}")
    print(f"\nTop 5 Recommendations:\n")
    
    for i, product in enumerate(data['recommendations'], 1):
        print(f"{i}. {product['product_name']}")
        print(f"   💰 Price: ₹{product['price']:,.2f}")
        print(f"   📂 Category: {product['category']}")
        print(f"   ⭐ Rating: {product['rating']} ({product['num_reviews']} reviews)")
        if product['discount'] > 0:
            print(f"   🎉 Discount: {product['discount']}% OFF")
        print()

def demo_similar_products():
    """Show similar products"""
    print_section("🔍 SIMILAR PRODUCTS TO PROD0001")
    
    response = requests.get(
        f"{BASE_URL}/recommend/product/PROD0001",
        params={'n': 5}
    )
    data = response.json()
    
    original = data['product']
    print(f"\nOriginal Product:")
    print(f"  {original['product_name']}")
    print(f"  ₹{original['price']:,.2f} | {original['category']} | ⭐{original['rating']}")
    
    print(f"\nSimilar Products:\n")
    
    for i, product in enumerate(data['similar_products'], 1):
        print(f"{i}. {product['product_name']}")
        print(f"   💰 ₹{product['price']:,.2f} | ⭐{product['rating']}")
        print()

def demo_category():
    """Show category recommendations"""
    print_section("📂 TOP ELECTRONICS PRODUCTS")
    
    response = requests.get(
        f"{BASE_URL}/recommend/category/Electronics",
        params={'n': 5}
    )
    data = response.json()
    
    print(f"\nCategory: {data['category']}")
    print(f"\nTop Products:\n")
    
    for i, product in enumerate(data['recommendations'], 1):
        print(f"{i}. {product['product_name']}")
        print(f"   💰 ₹{product['price']:,.2f}")
        print(f"   🏷️ Brand: {product['brand']}")
        print(f"   ⭐ {product['rating']} ({product['num_reviews']} reviews)")
        print()

def demo_popular():
    """Show popular products"""
    print_section("🔥 POPULAR PRODUCTS")
    
    response = requests.get(
        f"{BASE_URL}/recommend/popular",
        params={'n': 5}
    )
    data = response.json()
    
    print(f"\nTrending Now:\n")
    
    for i, product in enumerate(data['recommendations'], 1):
        print(f"{i}. {product['product_name']}")
        print(f"   💰 ₹{product['price']:,.2f}")
        print(f"   📂 {product['category']}")
        print(f"   ⭐ {product['rating']} ({product['num_reviews']} reviews)")
        print()

def main():
    print("\n" + "🛒"*30)
    print("  FLIPKART RECOMMENDATION SYSTEM - LIVE DEMO")
    print("🛒"*30)
    
    try:
        demo_stats()
        demo_user_recommendations()
        demo_similar_products()
        demo_category()
        demo_popular()
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETE!")
        print("="*60)
        print("\n💡 Open http://localhost:5000 in your browser")
        print("   to explore the interactive web interface!")
        print()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to the server")
        print("   Make sure the Flask server is running:")
        print("   python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
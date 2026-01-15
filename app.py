from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from recommendation_engine import FlipkartRecommendationEngine
import pandas as pd

app = Flask(__name__)
CORS(app)

# Initialize recommendation engine
engine = FlipkartRecommendationEngine()

@app.route('/')
def home():
    """Home page"""
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users"""
    users = engine.users_df.to_dict('records')
    return jsonify({'users': users[:50]})  # Return first 50 users

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    category = request.args.get('category')
    
    if category:
        products = engine.products_df[
            engine.products_df['category'] == category
        ].to_dict('records')
    else:
        products = engine.products_df.to_dict('records')
    
    return jsonify({'products': products[:100]})  # Limit to 100

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    categories = engine.products_df['category'].unique().tolist()
    return jsonify({'categories': categories})

@app.route('/api/recommend/user/<user_id>', methods=['GET'])
def recommend_for_user(user_id):
    """Get personalized recommendations for a user"""
    n = int(request.args.get('n', 10))
    method = request.args.get('method', 'hybrid')
    
    try:
        if method == 'collaborative':
            recommendations = engine.get_collaborative_recommendations(user_id, n)
        elif method == 'hybrid':
            recommendations = engine.get_hybrid_recommendations(user_id, n)
        else:
            recommendations = engine.get_popular_products(n)
        
        products = engine.get_product_details(recommendations)
        
        return jsonify({
            'user_id': user_id,
            'method': method,
            'recommendations': products
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/product/<product_id>', methods=['GET'])
def recommend_similar_products(product_id):
    """Get similar products based on content"""
    n = int(request.args.get('n', 10))
    
    try:
        recommendations = engine.get_content_based_recommendations(product_id, n)
        products = engine.get_product_details(recommendations)
        
        # Get original product details
        original = engine.products_df[
            engine.products_df['product_id'] == product_id
        ].to_dict('records')
        
        return jsonify({
            'product': original[0] if original else None,
            'similar_products': products
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/category/<category>', methods=['GET'])
def recommend_by_category(category):
    """Get top products in a category"""
    n = int(request.args.get('n', 10))
    
    try:
        recommendations = engine.get_category_recommendations(category, n)
        products = engine.get_product_details(recommendations)
        
        return jsonify({
            'category': category,
            'recommendations': products
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommend/popular', methods=['GET'])
def recommend_popular():
    """Get popular products"""
    n = int(request.args.get('n', 10))
    
    recommendations = engine.get_popular_products(n)
    products = engine.get_product_details(recommendations)
    
    return jsonify({'recommendations': products})

@app.route('/api/product/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product details"""
    product = engine.products_df[
        engine.products_df['product_id'] == product_id
    ].to_dict('records')
    
    if product:
        return jsonify({'product': product[0]})
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/api/user/<user_id>/history', methods=['GET'])
def get_user_history(user_id):
    """Get user interaction history"""
    history = engine.interactions_df[
        engine.interactions_df['user_id'] == user_id
    ].sort_values('timestamp', ascending=False).head(20)
    
    # Get product details for each interaction
    product_ids = history['product_id'].tolist()
    products = engine.get_product_details(product_ids)
    
    # Merge interaction data with product details
    history_with_products = []
    for _, interaction in history.iterrows():
        product = next(
            (p for p in products if p['product_id'] == interaction['product_id']),
            None
        )
        if product:
            history_with_products.append({
                'interaction_type': interaction['interaction_type'],
                'timestamp': interaction['timestamp'],
                'rating': interaction['rating'],
                'product': product
            })
    
    return jsonify({
        'user_id': user_id,
        'history': history_with_products
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    stats = {
        'total_products': len(engine.products_df),
        'total_users': len(engine.users_df),
        'total_interactions': len(engine.interactions_df),
        'categories': engine.products_df['category'].nunique(),
        'brands': engine.products_df['brand'].nunique(),
        'avg_rating': round(engine.products_df['rating'].mean(), 2),
        'total_purchases': len(engine.interactions_df[
            engine.interactions_df['interaction_type'] == 'purchase'
        ])
    }
    
    return jsonify(stats)

def initialize_app():
    """Initialize the recommendation engine"""
    print("Initializing Flipkart Recommendation System...")
    try:
        engine.load_models()
        print("✅ Models loaded successfully")
    except:
        print("⚠️ Models not found. Training new models...")
        engine.train()
        engine.save_models()
    print("✅ System ready!")

if __name__ == '__main__':
    initialize_app()
    print("\n" + "="*50)
    print("🚀 Starting Flask server...")
    print("API available at: http://localhost:5000")
    print("="*50 + "\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
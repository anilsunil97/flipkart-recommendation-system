"""
Streamlit App for Flipkart Product Recommendation System
"""
import streamlit as st
import pandas as pd
import numpy as np
import os
from recommendation_engine import FlipkartRecommendationEngine

# Page configuration
st.set_page_config(
    page_title="Flipkart Product Recommendations",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2874f0;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #eee;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_engine():
    """Load or initialize the recommendation engine"""
    engine = FlipkartRecommendationEngine()
    
    # Check if data exists
    if not os.path.exists('data/products.csv'):
        st.info("Generating sample data... This will take a moment.")
        from data_generator import FlipkartDataGenerator
        generator = FlipkartDataGenerator()
        generator.save_data()
    
    # Check if models exist
    if not os.path.exists('models/knn_model.pkl'):
        st.info("Training recommendation models... This will take a moment.")
        engine.train()
        engine.save_models()
    else:
        engine.load_models()
    
    return engine

def display_product_card(product, index):
    """Display a product card"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"### {index}. {product['product_name']}")
        st.markdown(f"**Category:** {product['category']} | **Brand:** {product['brand']}")
        
    with col2:
        st.markdown(f"### ₹{product['price']:,.2f}")
        st.markdown(f"⭐ {product['rating']} ({product['num_reviews']} reviews)")
    
    if product['discount'] > 0:
        st.success(f"🎉 {product['discount']}% OFF")
    
    if product['stock'] < 10:
        st.warning(f"⚠️ Only {product['stock']} left in stock!")
    
    st.markdown("---")

def main():
    # Header
    st.markdown('<h1 class="main-header">🛒 Flipkart Product Recommendations</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Product Discovery System</p>', unsafe_allow_html=True)
    
    # Load engine
    try:
        engine = load_engine()
    except Exception as e:
        st.error(f"Error loading recommendation engine: {e}")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/shopping-cart.png", width=80)
        st.title("Navigation")
        
        page = st.radio(
            "Choose a page:",
            ["🏠 Home", "👤 User Recommendations", "🔍 Similar Products", 
             "📂 Category Browse", "📊 Statistics"]
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This system uses machine learning to provide personalized product recommendations:
        - **Collaborative Filtering**: Based on similar users
        - **Content-Based**: Based on product features
        - **Hybrid**: Best of both worlds
        """)
    
    # Main content
    if page == "🏠 Home":
        show_home(engine)
    elif page == "👤 User Recommendations":
        show_user_recommendations(engine)
    elif page == "🔍 Similar Products":
        show_similar_products(engine)
    elif page == "📂 Category Browse":
        show_category_browse(engine)
    elif page == "📊 Statistics":
        show_statistics(engine)

def show_home(engine):
    """Home page with popular products"""
    st.header("🔥 Popular Products")
    st.markdown("Trending products with high ratings and reviews")
    
    # Get popular products
    popular_ids = engine.get_popular_products(10)
    products = engine.get_product_details(popular_ids)
    
    # Display in grid
    cols = st.columns(2)
    for idx, product in enumerate(products):
        with cols[idx % 2]:
            with st.container():
                display_product_card(product, idx + 1)

def show_user_recommendations(engine):
    """User recommendations page"""
    st.header("👤 Personalized Recommendations")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # User selection
        user_ids = engine.users_df['user_id'].tolist()
        selected_user = st.selectbox("Select a user:", user_ids, index=0)
    
    with col2:
        # Method selection
        method = st.selectbox(
            "Recommendation method:",
            ["hybrid", "collaborative", "popular"],
            format_func=lambda x: {
                "hybrid": "🎯 Hybrid (Best)",
                "collaborative": "👥 Collaborative",
                "popular": "🔥 Popular"
            }[x]
        )
    
    # Number of recommendations
    n_recs = st.slider("Number of recommendations:", 5, 20, 10)
    
    if st.button("Get Recommendations", type="primary"):
        with st.spinner("Finding best products for you..."):
            # Get user info
            user_info = engine.users_df[engine.users_df['user_id'] == selected_user].iloc[0]
            
            st.info(f"**User:** {selected_user} | **Location:** {user_info['location']} | **Age:** {user_info['age']} | **Gender:** {user_info['gender']}")
            
            # Get recommendations
            if method == "hybrid":
                rec_ids = engine.get_hybrid_recommendations(selected_user, n_recs)
            elif method == "collaborative":
                rec_ids = engine.get_collaborative_recommendations(selected_user, n_recs)
            else:
                rec_ids = engine.get_popular_products(n_recs)
            
            products = engine.get_product_details(rec_ids)
            
            st.success(f"Found {len(products)} recommendations!")
            
            # Display products
            for idx, product in enumerate(products):
                display_product_card(product, idx + 1)

def show_similar_products(engine):
    """Similar products page"""
    st.header("🔍 Find Similar Products")
    
    # Product selection
    product_ids = engine.products_df['product_id'].tolist()
    product_names = engine.products_df['product_name'].tolist()
    
    product_options = {f"{pid} - {name}": pid for pid, name in zip(product_ids, product_names)}
    
    selected_option = st.selectbox("Select a product:", list(product_options.keys()))
    selected_product_id = product_options[selected_option]
    
    n_similar = st.slider("Number of similar products:", 5, 20, 10)
    
    if st.button("Find Similar Products", type="primary"):
        with st.spinner("Finding similar products..."):
            # Get original product
            original = engine.products_df[engine.products_df['product_id'] == selected_product_id].iloc[0]
            
            st.markdown("### Original Product")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Price", f"₹{original['price']:,.2f}")
            with col2:
                st.metric("Rating", f"{original['rating']}⭐")
            with col3:
                st.metric("Category", original['category'])
            
            st.markdown("---")
            
            # Get similar products
            similar_ids = engine.get_content_based_recommendations(selected_product_id, n_similar)
            products = engine.get_product_details(similar_ids)
            
            st.markdown("### Similar Products")
            st.success(f"Found {len(products)} similar products!")
            
            for idx, product in enumerate(products):
                display_product_card(product, idx + 1)

def show_category_browse(engine):
    """Category browse page"""
    st.header("📂 Browse by Category")
    
    # Category selection
    categories = engine.products_df['category'].unique().tolist()
    selected_category = st.selectbox("Select a category:", categories)
    
    n_products = st.slider("Number of products:", 5, 20, 10)
    
    if st.button("Show Products", type="primary"):
        with st.spinner(f"Loading {selected_category} products..."):
            # Get category products
            product_ids = engine.get_category_recommendations(selected_category, n_products)
            products = engine.get_product_details(product_ids)
            
            st.success(f"Found {len(products)} products in {selected_category}")
            
            # Display products
            for idx, product in enumerate(products):
                display_product_card(product, idx + 1)

def show_statistics(engine):
    """Statistics page"""
    st.header("📊 System Statistics")
    
    # Overall stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{len(engine.products_df)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Products</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{len(engine.users_df)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Users</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{len(engine.interactions_df)}</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Interactions</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        avg_rating = engine.products_df['rating'].mean()
        st.markdown('<div class="stat-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value">{avg_rating:.2f}⭐</div>', unsafe_allow_html=True)
        st.markdown('<div class="stat-label">Avg Rating</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Category distribution
    st.subheader("📂 Products by Category")
    category_counts = engine.products_df['category'].value_counts()
    st.bar_chart(category_counts)
    
    # Brand distribution
    st.subheader("🏷️ Products by Brand")
    brand_counts = engine.products_df['brand'].value_counts()
    st.bar_chart(brand_counts)
    
    # Price distribution
    st.subheader("💰 Price Distribution")
    st.line_chart(engine.products_df['price'].value_counts().sort_index())
    
    # Interaction types
    st.subheader("🔄 Interaction Types")
    interaction_counts = engine.interactions_df['interaction_type'].value_counts()
    st.bar_chart(interaction_counts)

if __name__ == "__main__":
    main()
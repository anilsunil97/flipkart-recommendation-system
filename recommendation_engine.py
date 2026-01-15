import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import joblib
import os

class FlipkartRecommendationEngine:
    """Product recommendation engine with multiple algorithms"""
    
    def __init__(self):
        self.products_df = None
        self.users_df = None
        self.interactions_df = None
        self.user_item_matrix = None
        self.content_similarity = None
        self.knn_model = None
        
    def load_data(self):
        """Load datasets"""
        self.products_df = pd.read_csv('data/products.csv')
        self.users_df = pd.read_csv('data/users.csv')
        self.interactions_df = pd.read_csv('data/interactions.csv')
        print("✅ Data loaded successfully")
        
    def prepare_user_item_matrix(self):
        """Create user-item interaction matrix"""
        # Filter only purchases and ratings
        purchase_data = self.interactions_df[
            self.interactions_df['interaction_type'].isin(['purchase', 'cart'])
        ].copy()
        
        # Create implicit ratings (purchase=5, cart=3, view=1)
        purchase_data['implicit_rating'] = purchase_data['interaction_type'].map({
            'purchase': 5,
            'cart': 3,
            'view': 1
        })
        
        # Use explicit rating if available, otherwise implicit
        purchase_data['final_rating'] = purchase_data['rating'].fillna(
            purchase_data['implicit_rating']
        )
        
        # Create pivot table
        self.user_item_matrix = purchase_data.pivot_table(
            index='user_id',
            columns='product_id',
            values='final_rating',
            fill_value=0
        )
        
        print(f"✅ User-item matrix created: {self.user_item_matrix.shape}")
        
    def build_collaborative_filtering(self):
        """Build collaborative filtering model using KNN"""
        # Convert to sparse matrix for efficiency
        sparse_matrix = csr_matrix(self.user_item_matrix.values)
        
        # Train KNN model
        self.knn_model = NearestNeighbors(
            metric='cosine',
            algorithm='brute',
            n_neighbors=20
        )
        self.knn_model.fit(sparse_matrix)
        
        print("✅ Collaborative filtering model built")
        
    def build_content_based_filtering(self):
        """Build content-based filtering using product features"""
        # Create product feature text
        self.products_df['features'] = (
            self.products_df['category'] + ' ' +
            self.products_df['brand'] + ' ' +
            self.products_df['product_name']
        )
        
        # Create TF-IDF vectors
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.products_df['features'])
        
        # Calculate similarity
        self.content_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        print("✅ Content-based filtering model built")
        
    def get_collaborative_recommendations(self, user_id, n_recommendations=10):
        """Get recommendations using collaborative filtering"""
        if user_id not in self.user_item_matrix.index:
            return self.get_popular_products(n_recommendations)
        
        # Get user index
        user_idx = self.user_item_matrix.index.get_loc(user_id)
        
        # Find similar users
        distances, indices = self.knn_model.kneighbors(
            self.user_item_matrix.iloc[user_idx].values.reshape(1, -1),
            n_neighbors=11
        )
        
        # Get products liked by similar users
        similar_users_indices = indices.flatten()[1:]  # Exclude the user itself
        
        # Aggregate ratings from similar users
        recommendations = {}
        user_products = set(self.user_item_matrix.columns[
            self.user_item_matrix.iloc[user_idx] > 0
        ])
        
        for idx in similar_users_indices:
            similar_user_products = self.user_item_matrix.iloc[idx]
            for product_id, rating in similar_user_products.items():
                if rating > 0 and product_id not in user_products:
                    if product_id not in recommendations:
                        recommendations[product_id] = []
                    recommendations[product_id].append(rating)
        
        # Calculate average ratings
        avg_recommendations = {
            product: np.mean(ratings)
            for product, ratings in recommendations.items()
        }
        
        # Sort and get top N
        top_products = sorted(
            avg_recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        return [prod[0] for prod in top_products]
    
    def get_content_based_recommendations(self, product_id, n_recommendations=10):
        """Get similar products using content-based filtering"""
        if product_id not in self.products_df['product_id'].values:
            return []
        
        # Get product index
        idx = self.products_df[
            self.products_df['product_id'] == product_id
        ].index[0]
        
        # Get similarity scores
        sim_scores = list(enumerate(self.content_similarity[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N similar products (excluding itself)
        sim_scores = sim_scores[1:n_recommendations+1]
        product_indices = [i[0] for i in sim_scores]
        
        return self.products_df.iloc[product_indices]['product_id'].tolist()
    
    def get_hybrid_recommendations(self, user_id, n_recommendations=10):
        """Hybrid approach combining collaborative and content-based"""
        # Get collaborative recommendations
        collab_recs = self.get_collaborative_recommendations(user_id, n_recommendations * 2)
        
        if not collab_recs:
            return self.get_popular_products(n_recommendations)
        
        # Get user's recent interactions
        user_interactions = self.interactions_df[
            self.interactions_df['user_id'] == user_id
        ].sort_values('timestamp', ascending=False)
        
        if len(user_interactions) > 0:
            recent_product = user_interactions.iloc[0]['product_id']
            content_recs = self.get_content_based_recommendations(
                recent_product,
                n_recommendations
            )
        else:
            content_recs = []
        
        # Combine recommendations (70% collaborative, 30% content-based)
        hybrid_recs = []
        collab_count = int(n_recommendations * 0.7)
        content_count = n_recommendations - collab_count
        
        hybrid_recs.extend(collab_recs[:collab_count])
        
        for rec in content_recs:
            if rec not in hybrid_recs and len(hybrid_recs) < n_recommendations:
                hybrid_recs.append(rec)
        
        # Fill remaining with collaborative
        for rec in collab_recs:
            if rec not in hybrid_recs and len(hybrid_recs) < n_recommendations:
                hybrid_recs.append(rec)
        
        return hybrid_recs[:n_recommendations]
    
    def get_popular_products(self, n_recommendations=10):
        """Get popular products as fallback"""
        popular = self.products_df.sort_values(
            ['rating', 'num_reviews'],
            ascending=False
        ).head(n_recommendations)
        
        return popular['product_id'].tolist()
    
    def get_category_recommendations(self, category, n_recommendations=10):
        """Get top products in a category"""
        category_products = self.products_df[
            self.products_df['category'] == category
        ].sort_values(['rating', 'num_reviews'], ascending=False)
        
        return category_products.head(n_recommendations)['product_id'].tolist()
    
    def get_product_details(self, product_ids):
        """Get detailed information for products"""
        return self.products_df[
            self.products_df['product_id'].isin(product_ids)
        ].to_dict('records')
    
    def train(self):
        """Train all recommendation models"""
        print("Training recommendation engine...")
        self.load_data()
        self.prepare_user_item_matrix()
        self.build_collaborative_filtering()
        self.build_content_based_filtering()
        print("✅ Training complete!")
        
    def save_models(self):
        """Save trained models"""
        os.makedirs('models', exist_ok=True)
        
        joblib.dump(self.knn_model, 'models/knn_model.pkl')
        joblib.dump(self.user_item_matrix, 'models/user_item_matrix.pkl')
        joblib.dump(self.content_similarity, 'models/content_similarity.pkl')
        
        print("✅ Models saved")
        
    def load_models(self):
        """Load trained models"""
        self.load_data()
        self.knn_model = joblib.load('models/knn_model.pkl')
        self.user_item_matrix = joblib.load('models/user_item_matrix.pkl')
        self.content_similarity = joblib.load('models/content_similarity.pkl')
        
        print("✅ Models loaded")

if __name__ == "__main__":
    engine = FlipkartRecommendationEngine()
    engine.train()
    engine.save_models()
    
    # Test recommendations
    print("\n" + "="*50)
    print("Testing Recommendations")
    print("="*50)
    
    test_user = engine.users_df.iloc[0]['user_id']
    print(f"\nRecommendations for {test_user}:")
    recs = engine.get_hybrid_recommendations(test_user, 5)
    details = engine.get_product_details(recs)
    
    for i, product in enumerate(details, 1):
        print(f"{i}. {product['product_name']} - ₹{product['price']} ({product['category']})")
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

class FlipkartDataGenerator:
    """Generate synthetic Flipkart product and user interaction data"""
    
    def __init__(self):
        self.categories = ['Electronics', 'Fashion', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys']
        self.brands = ['Samsung', 'Apple', 'Nike', 'Adidas', 'Sony', 'LG', 'Puma', 'Levi\'s', 'HP', 'Dell']
        
        self.product_names = {
            'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Smart Watch', 'Tablet', 'Camera', 'Speaker'],
            'Fashion': ['T-Shirt', 'Jeans', 'Shoes', 'Jacket', 'Dress', 'Sneakers', 'Watch'],
            'Home & Kitchen': ['Mixer', 'Cookware Set', 'Bedsheet', 'Curtains', 'Vacuum Cleaner', 'Iron'],
            'Books': ['Fiction Novel', 'Self-Help Book', 'Cookbook', 'Biography', 'Science Book'],
            'Sports': ['Cricket Bat', 'Football', 'Yoga Mat', 'Dumbbells', 'Running Shoes', 'Gym Bag'],
            'Beauty': ['Face Cream', 'Shampoo', 'Lipstick', 'Perfume', 'Face Wash', 'Hair Oil'],
            'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'Remote Car', 'Building Blocks']
        }
    
    def generate_products(self, n_products=500):
        """Generate synthetic product data"""
        products = []
        
        for i in range(n_products):
            category = random.choice(self.categories)
            product_name = random.choice(self.product_names[category])
            brand = random.choice(self.brands)
            
            product = {
                'product_id': f'PROD{i+1:04d}',
                'product_name': f'{brand} {product_name}',
                'category': category,
                'brand': brand,
                'price': round(random.uniform(500, 50000), 2),
                'rating': round(random.uniform(3.0, 5.0), 1),
                'num_reviews': random.randint(10, 5000),
                'discount': random.choice([0, 5, 10, 15, 20, 25, 30, 40, 50]),
                'stock': random.randint(0, 500)
            }
            products.append(product)
        
        return pd.DataFrame(products)
    
    def generate_users(self, n_users=1000):
        """Generate synthetic user data"""
        users = []
        
        for i in range(n_users):
            user = {
                'user_id': f'USER{i+1:04d}',
                'age': random.randint(18, 65),
                'gender': random.choice(['M', 'F']),
                'location': random.choice(['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata']),
                'member_since': (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime('%Y-%m-%d')
            }
            users.append(user)
        
        return pd.DataFrame(users)
    
    def generate_interactions(self, products_df, users_df, n_interactions=5000):
        """Generate user-product interactions (views, purchases, ratings)"""
        interactions = []
        
        product_ids = products_df['product_id'].tolist()
        user_ids = users_df['user_id'].tolist()
        
        for _ in range(n_interactions):
            interaction = {
                'user_id': random.choice(user_ids),
                'product_id': random.choice(product_ids),
                'interaction_type': random.choice(['view', 'view', 'view', 'cart', 'cart', 'purchase']),
                'rating': random.choice([None, None, None, 3, 4, 5]),
                'timestamp': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
            }
            interactions.append(interaction)
        
        return pd.DataFrame(interactions)
    
    def save_data(self):
        """Generate and save all datasets"""
        print("Generating products...")
        products_df = self.generate_products(500)
        products_df.to_csv('data/products.csv', index=False)
        print(f"✅ Generated {len(products_df)} products")
        
        print("Generating users...")
        users_df = self.generate_users(1000)
        users_df.to_csv('data/users.csv', index=False)
        print(f"✅ Generated {len(users_df)} users")
        
        print("Generating interactions...")
        interactions_df = self.generate_interactions(products_df, users_df, 5000)
        interactions_df.to_csv('data/interactions.csv', index=False)
        print(f"✅ Generated {len(interactions_df)} interactions")
        
        return products_df, users_df, interactions_df

if __name__ == "__main__":
    import os
    os.makedirs('data', exist_ok=True)
    
    generator = FlipkartDataGenerator()
    generator.save_data()
    print("\n✅ All data generated successfully!")
# Flipkart Product Recommendation System

A machine learning-based product recommendation system for Flipkart using collaborative filtering, content-based filtering, and hybrid approaches.

## Features

- **Multiple Recommendation Algorithms**:
  - Collaborative Filtering (User-based KNN)
  - Content-Based Filtering (TF-IDF + Cosine Similarity)
  - Hybrid Approach (Combines both methods)
  
- **Recommendation Types**:
  - Personalized user recommendations
  - Similar product recommendations
  - Category-based recommendations
  - Popular products

- **Web Interface**:
  - Interactive Flask web application
  - Real-time recommendations
  - Product browsing and filtering
  - User interaction history

## Project Structure

```
├── data/                      # Generated datasets
│   ├── products.csv          # Product catalog
│   ├── users.csv             # User profiles
│   └── interactions.csv      # User-product interactions
├── models/                    # Trained ML models
│   ├── knn_model.pkl
│   ├── user_item_matrix.pkl
│   └── content_similarity.pkl
├── templates/                 # HTML templates
│   └── index.html
├── data_generator.py         # Synthetic data generation
├── recommendation_engine.py  # ML recommendation algorithms
├── app.py                    # Flask web application
└── requirements.txt          # Python dependencies
```

## Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Generate sample data**:
```bash
python data_generator.py
```

3. **Train recommendation models**:
```bash
python recommendation_engine.py
```

4. **Run the web application**:
```bash
python app.py
```

5. **Access the application**:
Open http://localhost:5000 in your browser

## How It Works

### 1. Collaborative Filtering
- Uses K-Nearest Neighbors (KNN) algorithm
- Finds similar users based on purchase/interaction history
- Recommends products liked by similar users
- Works well for users with sufficient interaction history

### 2. Content-Based Filtering
- Analyzes product features (category, brand, name)
- Uses TF-IDF vectorization for text features
- Calculates cosine similarity between products
- Recommends similar products based on content

### 3. Hybrid Approach
- Combines collaborative and content-based methods
- 70% weight to collaborative filtering
- 30% weight to content-based filtering
- Provides balanced and diverse recommendations

## API Endpoints

### User Recommendations
```
GET /api/recommend/user/<user_id>?method=hybrid&n=10
```
Methods: `hybrid`, `collaborative`, `popular`

### Similar Products
```
GET /api/recommend/product/<product_id>?n=10
```

### Category Recommendations
```
GET /api/recommend/category/<category>?n=10
```

### Popular Products
```
GET /api/recommend/popular?n=10
```

### Product Details
```
GET /api/product/<product_id>
```

### User History
```
GET /api/user/<user_id>/history
```

### System Statistics
```
GET /api/stats
```

## Data Schema

### Products
- product_id: Unique identifier
- product_name: Product name
- category: Product category
- brand: Brand name
- price: Product price
- rating: Average rating (1-5)
- num_reviews: Number of reviews
- discount: Discount percentage
- stock: Available stock

### Users
- user_id: Unique identifier
- age: User age
- gender: M/F
- location: City
- member_since: Registration date

### Interactions
- user_id: User identifier
- product_id: Product identifier
- interaction_type: view/cart/purchase
- rating: User rating (optional)
- timestamp: Interaction time

## Machine Learning Models

### K-Nearest Neighbors (KNN)
- Algorithm: Brute force
- Metric: Cosine similarity
- Neighbors: 20
- Used for finding similar users

### TF-IDF Vectorizer
- Stop words: English
- Used for product feature extraction
- Creates sparse matrix of product features

### Cosine Similarity
- Measures similarity between product vectors
- Range: 0 (dissimilar) to 1 (identical)
- Used for content-based recommendations

## Performance Optimization

- Sparse matrix representation for user-item matrix
- Efficient KNN with brute force algorithm
- Cached similarity matrices
- Model persistence with joblib

## Customization

### Adjust Recommendation Parameters
Edit `recommendation_engine.py`:
```python
# Number of similar users to consider
n_neighbors=20

# Hybrid weights
collab_weight = 0.7
content_weight = 0.3
```

### Generate More Data
Edit `data_generator.py`:
```python
products_df = self.generate_products(1000)  # More products
users_df = self.generate_users(2000)        # More users
interactions_df = self.generate_interactions(10000)  # More interactions
```

## Future Enhancements

- Deep learning models (Neural Collaborative Filtering)
- Real-time recommendation updates
- A/B testing framework
- Recommendation explanations
- Multi-armed bandit algorithms
- Session-based recommendations
- Image-based product similarity
- Price optimization
- Inventory-aware recommendations

## Technologies Used

- **Python 3.8+**
- **Flask**: Web framework
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning
- **SciPy**: Scientific computing
- **Joblib**: Model persistence

## License

MIT License - Feel free to use and modify for your projects!
# System Architecture

## Overview

The Flipkart Product Recommendation System uses a hybrid machine learning approach combining collaborative filtering and content-based filtering to provide personalized product recommendations.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                                                                 │
│  ┌──────────────────┐              ┌──────────────────┐       │
│  │  Web Browser     │              │   API Clients    │       │
│  │  (HTML/CSS/JS)   │              │   (Python/curl)  │       │
│  └────────┬─────────┘              └────────┬─────────┘       │
└───────────┼──────────────────────────────────┼─────────────────┘
            │                                  │
            └──────────────┬───────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FLASK WEB SERVER                           │
│                         (app.py)                                │
│                                                                 │
│  API Endpoints:                                                 │
│  • /api/recommend/user/<id>     - User recommendations         │
│  • /api/recommend/product/<id>  - Similar products             │
│  • /api/recommend/category/<c>  - Category products            │
│  • /api/recommend/popular       - Popular products             │
│  • /api/stats                   - System statistics            │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              RECOMMENDATION ENGINE                              │
│           (recommendation_engine.py)                            │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           HYBRID RECOMMENDATION SYSTEM                   │  │
│  │                                                          │  │
│  │  ┌────────────────────┐    ┌────────────────────┐      │  │
│  │  │  Collaborative     │    │   Content-Based    │      │  │
│  │  │    Filtering       │    │     Filtering      │      │  │
│  │  │                    │    │                    │      │  │
│  │  │  • User-based KNN  │    │  • TF-IDF          │      │  │
│  │  │  • Cosine Sim      │    │  • Cosine Sim      │      │  │
│  │  │  • 20 neighbors    │    │  • Product features│      │  │
│  │  └────────────────────┘    └────────────────────┘      │  │
│  │                                                          │  │
│  │         70% Weight              30% Weight              │  │
│  │                 │                    │                   │  │
│  │                 └──────────┬─────────┘                  │  │
│  │                            ▼                            │  │
│  │                  ┌──────────────────┐                   │  │
│  │                  │ Hybrid Combiner  │                   │  │
│  │                  └──────────────────┘                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  products.csv│  │   users.csv  │  │interactions  │        │
│  │              │  │              │  │    .csv      │        │
│  │ • 500 items  │  │ • 1000 users │  │ • 5000 items │        │
│  │ • Categories │  │ • Demographics│ │ • Views      │        │
│  │ • Prices     │  │ • Location   │  │ • Purchases  │        │
│  │ • Ratings    │  │ • Age/Gender │  │ • Ratings    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              TRAINED MODELS (Pickled)                    │  │
│  │                                                          │  │
│  │  • knn_model.pkl          - KNN model                   │  │
│  │  • user_item_matrix.pkl   - User-product interactions   │  │
│  │  • content_similarity.pkl - Product similarity matrix   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Data Layer

#### Products Dataset
- **Size**: 500 products
- **Features**: 
  - product_id, product_name, category, brand
  - price, rating, num_reviews, discount, stock
- **Categories**: Electronics, Fashion, Home & Kitchen, Books, Sports, Beauty, Toys

#### Users Dataset
- **Size**: 1000 users
- **Features**: user_id, age, gender, location, member_since
- **Demographics**: Ages 18-65, Multiple cities

#### Interactions Dataset
- **Size**: 5000 interactions
- **Types**: view, cart, purchase
- **Features**: user_id, product_id, interaction_type, rating, timestamp

### 2. Machine Learning Models

#### Collaborative Filtering
```python
Algorithm: K-Nearest Neighbors (KNN)
Metric: Cosine Similarity
Neighbors: 20
Matrix: User-Item (925 x 497)
```

**How it works**:
1. Create user-item interaction matrix
2. Find similar users using KNN
3. Recommend products liked by similar users
4. Filter out already purchased items

#### Content-Based Filtering
```python
Vectorization: TF-IDF
Similarity: Cosine Similarity
Features: category + brand + product_name
```

**How it works**:
1. Create feature vectors for each product
2. Calculate similarity between products
3. Recommend products similar to user's history
4. Based on product attributes

#### Hybrid Approach
```python
Combination: Weighted Average
Collaborative Weight: 70%
Content-Based Weight: 30%
```

**How it works**:
1. Get recommendations from both methods
2. Combine with weighted approach
3. Remove duplicates
4. Return top N products

### 3. API Layer

#### Flask Routes
- **GET /**: Web interface
- **GET /api/stats**: System statistics
- **GET /api/users**: List users
- **GET /api/products**: List products
- **GET /api/categories**: List categories
- **GET /api/recommend/user/<id>**: User recommendations
- **GET /api/recommend/product/<id>**: Similar products
- **GET /api/recommend/category/<c>**: Category products
- **GET /api/recommend/popular**: Popular products
- **GET /api/user/<id>/history**: User history

### 4. Web Interface

#### Features
- Interactive product cards
- Real-time recommendations
- Method selection (Hybrid/Collaborative/Popular)
- Category filtering
- User selection
- System statistics dashboard

## Data Flow

### User Recommendation Flow
```
1. User selects user_id and method
2. Frontend sends GET request to /api/recommend/user/<id>
3. Backend loads user interaction history
4. Collaborative filtering finds similar users
5. Content-based filtering finds similar products
6. Hybrid combiner merges results
7. Top N products returned as JSON
8. Frontend displays product cards
```

### Similar Product Flow
```
1. User selects product_id
2. Frontend sends GET request to /api/recommend/product/<id>
3. Backend loads product features
4. TF-IDF vectorization of features
5. Cosine similarity calculation
6. Top N similar products returned
7. Frontend displays recommendations
```

## Performance Characteristics

### Time Complexity
- **Collaborative Filtering**: O(k * n) where k=neighbors, n=products
- **Content-Based**: O(n²) for similarity matrix (pre-computed)
- **Hybrid**: O(k * n) + O(1) for lookup

### Space Complexity
- **User-Item Matrix**: O(users * products) = ~460KB
- **Similarity Matrix**: O(products²) = ~1MB
- **Models**: ~2MB total

### Scalability
- Current: 500 products, 1000 users
- Recommended: Up to 10K products, 100K users
- For larger scale: Consider approximate nearest neighbors (ANN)

## Technology Stack

- **Backend**: Flask 3.0+
- **ML Libraries**: scikit-learn, scipy, numpy, pandas
- **Model Persistence**: joblib
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Format**: CSV files
- **Model Format**: Pickle files (.pkl)

## Future Enhancements

1. **Deep Learning**: Neural Collaborative Filtering
2. **Real-time**: Stream processing for live updates
3. **A/B Testing**: Compare algorithm performance
4. **Explainability**: Show why products were recommended
5. **Multi-armed Bandits**: Exploration vs exploitation
6. **Session-based**: RNN/LSTM for sequential recommendations
7. **Image Similarity**: CNN for visual product matching
8. **Graph Neural Networks**: For complex user-product relationships
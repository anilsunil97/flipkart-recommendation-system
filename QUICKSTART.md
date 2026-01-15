# Quick Start Guide

## 🚀 Your Flipkart Recommendation System is Ready!

The system is currently running and ready to use.

## 📍 Access Points

### Web Interface
**URL**: http://localhost:5000

Open this in your browser to access the interactive web interface where you can:
- Get personalized recommendations for users
- Find similar products
- Browse products by category
- View system statistics

### API Endpoints

All endpoints are available at `http://localhost:5000/api/`

#### Get System Statistics
```bash
curl http://localhost:5000/api/stats
```

#### Get User Recommendations
```bash
curl "http://localhost:5000/api/recommend/user/USER0001?method=hybrid&n=10"
```

Methods: `hybrid`, `collaborative`, `popular`

#### Get Similar Products
```bash
curl "http://localhost:5000/api/recommend/product/PROD0001?n=10"
```

#### Get Category Recommendations
```bash
curl "http://localhost:5000/api/recommend/category/Electronics?n=10"
```

#### Get Popular Products
```bash
curl "http://localhost:5000/api/recommend/popular?n=10"
```

## 📊 Current System Stats

- **Products**: 500
- **Users**: 1000
- **Interactions**: 5000
- **Categories**: 7 (Electronics, Fashion, Home & Kitchen, Books, Sports, Beauty, Toys)
- **Brands**: 10
- **Average Rating**: 4.02⭐
- **Total Purchases**: 823

## 🎯 How to Use

### 1. Web Interface (Easiest)
1. Open http://localhost:5000 in your browser
2. Select a user from the dropdown
3. Choose recommendation method (Hybrid recommended)
4. Click "Get Recommendations"
5. Explore similar products and category recommendations

### 2. Python API
```python
import requests

# Get recommendations for a user
response = requests.get('http://localhost:5000/api/recommend/user/USER0001?method=hybrid&n=5')
data = response.json()

for product in data['recommendations']:
    print(f"{product['product_name']} - ₹{product['price']}")
```

### 3. Command Line
```bash
# Get user recommendations
curl "http://localhost:5000/api/recommend/user/USER0001?method=hybrid&n=5"

# Get similar products
curl "http://localhost:5000/api/recommend/product/PROD0001?n=5"
```

## 🔧 Recommendation Methods

### Hybrid (Recommended)
- Combines collaborative and content-based filtering
- Best overall performance
- 70% collaborative + 30% content-based

### Collaborative Filtering
- Based on similar users' preferences
- Works well for users with interaction history
- Uses K-Nearest Neighbors algorithm

### Content-Based
- Based on product features (category, brand, name)
- Good for finding similar products
- Uses TF-IDF and cosine similarity

### Popular
- Trending products with high ratings
- Good for new users (cold start)
- Based on rating and review count

## 📁 Project Files

```
├── data/                      # Generated datasets
│   ├── products.csv          # 500 products
│   ├── users.csv             # 1000 users
│   └── interactions.csv      # 5000 interactions
├── models/                    # Trained ML models
│   ├── knn_model.pkl
│   ├── user_item_matrix.pkl
│   └── content_similarity.pkl
├── templates/
│   └── index.html            # Web interface
├── app.py                    # Flask server (RUNNING)
├── recommendation_engine.py  # ML algorithms
├── data_generator.py         # Data generation
└── test_recommendations.py   # Testing script
```

## 🧪 Testing

Run the test script to see all recommendation types:
```bash
python test_recommendations.py
```

## 🛑 Stop the Server

To stop the Flask server, press `Ctrl+C` in the terminal where it's running.

## 🔄 Regenerate Data

To create new data:
```bash
python data_generator.py
python recommendation_engine.py
```

## 💡 Tips

1. **Try different users** - Each user has different preferences based on their interaction history
2. **Compare methods** - Switch between hybrid, collaborative, and popular to see differences
3. **Explore categories** - Each category has unique top products
4. **Check similar products** - Content-based filtering finds products with similar features

## 🎉 Enjoy Your Recommendation System!

The system is fully functional and ready for exploration. Open http://localhost:5000 to get started!
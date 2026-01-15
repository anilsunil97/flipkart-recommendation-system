# Project Structure

## 📁 Flipkart Product Recommendation System

```
flipkart-recommendation-system/
│
├── 📂 data/                          # Data files
│   ├── products.csv                  # 500 products
│   ├── users.csv                     # 1000 users
│   └── interactions.csv              # 5000 interactions
│
├── 📂 models/                        # Trained ML models (generated)
│   ├── knn_model.pkl
│   ├── user_item_matrix.pkl
│   └── content_similarity.pkl
│
├── 📂 templates/                     # Web templates
│   └── index.html                    # Flask web interface
│
├── 📂 .streamlit/                    # Streamlit configuration
│   └── config.toml
│
├── 🐍 Core Python Files
│   ├── app.py                        # Flask REST API server
│   ├── streamlit_app_main.py        # Streamlit web app
│   ├── recommendation_engine.py     # ML recommendation algorithms
│   ├── data_generator.py            # Synthetic data generation
│   ├── test_recommendations.py      # Testing suite
│   └── demo_api.py                  # API demonstration
│
├── 📚 Documentation
│   ├── README.md                    # Main documentation
│   ├── QUICKSTART.md               # Quick start guide
│   ├── ARCHITECTURE.md             # System architecture
│   ├── STREAMLIT_DEPLOYMENT.md     # Streamlit deployment guide
│   └── GITHUB_UPLOAD_INSTRUCTIONS.txt  # GitHub upload guide
│
└── ⚙️ Configuration
    ├── requirements.txt             # Python dependencies
    ├── packages.txt                 # System packages
    ├── .gitignore                   # Git ignore rules
    └── LICENSE                      # MIT License
```

## 📊 File Count

- **Source Code**: 6 files
- **Data Files**: 3 files
- **Documentation**: 5 files
- **Configuration**: 4 files
- **Total**: 18 files (excluding generated models)

## 🚀 Quick Commands

```bash
# Generate data
python data_generator.py

# Train models
python recommendation_engine.py

# Run Flask API
python app.py

# Run Streamlit app
streamlit run streamlit_app_main.py

# Run tests
python test_recommendations.py

# Run demo
python demo_api.py
```

## 📖 Documentation Guide

- **README.md** - Start here for complete overview
- **QUICKSTART.md** - Get started in 5 minutes
- **ARCHITECTURE.md** - Understand the system design
- **STREAMLIT_DEPLOYMENT.md** - Deploy to Streamlit Cloud
- **GITHUB_UPLOAD_INSTRUCTIONS.txt** - Upload to GitHub
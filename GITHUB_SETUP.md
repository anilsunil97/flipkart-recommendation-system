# GitHub Setup Guide

## Step-by-Step Instructions to Upload to GitHub

### Option 1: Using GitHub Desktop (Easiest)

1. **Download GitHub Desktop**
   - Go to https://desktop.github.com/
   - Download and install

2. **Sign in to GitHub**
   - Open GitHub Desktop
   - Sign in with your GitHub account

3. **Add Repository**
   - Click "File" → "Add Local Repository"
   - Browse to: `C:\Users\Petpooja-1371\Desktop\RAGPROJECT`
   - Click "Add Repository"

4. **Create Repository on GitHub**
   - Click "Publish repository"
   - Name: `flipkart-recommendation-system`
   - Description: "ML-based product recommendation system for Flipkart"
   - Uncheck "Keep this code private" (or keep checked for private repo)
   - Click "Publish repository"

5. **Done!** Your project is now on GitHub

---

### Option 2: Using Command Line (Git)

1. **Initialize Git Repository**
```bash
cd C:\Users\Petpooja-1371\Desktop\RAGPROJECT
git init
```

2. **Add All Files**
```bash
git add .
```

3. **Create First Commit**
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
git commit -m "Initial commit: Flipkart recommendation system"
```

4. **Create Repository on GitHub**
   - Go to https://github.com/new
   - Repository name: `flipkart-recommendation-system`
   - Description: "ML-based product recommendation system for Flipkart"
   - Choose Public or Private
   - DO NOT initialize with README (we already have one)
   - Click "Create repository"

5. **Connect and Push**
```bash
git remote add origin https://github.com/YOUR_USERNAME/flipkart-recommendation-system.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your actual GitHub username.

---

### Option 3: Using GitHub Web Interface

1. **Create a ZIP file**
```bash
# In PowerShell
Compress-Archive -Path * -DestinationPath flipkart-recommendation.zip
```

2. **Go to GitHub**
   - Visit https://github.com/new
   - Create new repository: `flipkart-recommendation-system`
   - Click "uploading an existing file"
   - Drag and drop the ZIP file or individual files
   - Commit changes

---

## What Will Be Uploaded

### Included Files:
✅ Source code (Python files)
✅ Data files (CSV)
✅ Templates (HTML)
✅ Documentation (README, guides)
✅ Requirements.txt
✅ LICENSE
✅ .gitignore

### Excluded Files (via .gitignore):
❌ __pycache__/
❌ .vscode/
❌ *.pkl (model files - too large)
❌ Virtual environments

---

## After Upload

### Update README with GitHub Badge
Add this to the top of README.md:
```markdown
# Flipkart Product Recommendation System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

### Repository Settings
1. Add topics: `machine-learning`, `recommendation-system`, `flask`, `python`, `collaborative-filtering`
2. Add description
3. Set up GitHub Pages (optional) for documentation

---

## Recommended Repository Structure on GitHub

```
flipkart-recommendation-system/
├── .github/
│   └── workflows/          # CI/CD (optional)
├── data/                   # Sample data
├── templates/              # Web templates
├── app.py
├── recommendation_engine.py
├── data_generator.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── docs/                   # Documentation
```

---

## Important Notes

⚠️ **Model Files**: The trained model files (*.pkl) are excluded from Git because they're large. Users will need to run:
```bash
python data_generator.py
python recommendation_engine.py
```

⚠️ **Data Files**: CSV files are included but you can exclude them if they're too large by adding to .gitignore:
```
data/*.csv
```

⚠️ **Environment Variables**: .env file is excluded for security

---

## Quick Commands Reference

```bash
# Check status
git status

# Add new files
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View remote URL
git remote -v
```

---

## Troubleshooting

### "Git is not recognized"
Install Git from: https://git-scm.com/download/win

### "Permission denied"
Use HTTPS instead of SSH, or set up SSH keys

### "Large files"
Remove model files from tracking:
```bash
git rm --cached models/*.pkl
```

### "Already exists"
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/flipkart-recommendation-system.git
```

---

## Next Steps After Upload

1. ✅ Add repository description and topics
2. ✅ Enable GitHub Issues for bug tracking
3. ✅ Add CONTRIBUTING.md for contributors
4. ✅ Set up GitHub Actions for CI/CD (optional)
5. ✅ Add screenshots to README
6. ✅ Create releases/tags for versions

---

## Need Help?

- GitHub Docs: https://docs.github.com
- Git Tutorial: https://git-scm.com/docs/gittutorial
- GitHub Desktop: https://docs.github.com/en/desktop
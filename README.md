# End-to-End Demand Forecasting for Wooden Pallets

🎯 **Unified Dependency System** - One `requirements.txt` works everywhere: Local API, Local Dashboard, Render, and Streamlit Cloud!

## 🚀 Quick Start

### Automated Setup (Recommended)
```powershell
# Run unified setup script
.\setup.ps1
```

### Manual Setup
```bash
# 1. Ensure Python 3.12.x is installed
python --version  # Should show 3.12.x

# 2. Install dependencies (works for API + Dashboard)
pip install -r requirements.txt

# 3. Run API
uvicorn src.api.main:app --reload

# 4. Run Dashboard (in another terminal)
streamlit run dashboard/app.py
```

## 📦 Dependency Management

**No more version conflicts!** All dependencies are standardized:
- ✅ **Single requirements.txt** for all use cases
- ✅ **Python 3.12.0** everywhere (local, Render, Streamlit Cloud)
- ✅ **Tested compatible versions** across all platforms

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide.

## 🧪 Testing
```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v
```

## 📚 Project Structure
```
demand-forecasting/
├── requirements.txt          ← Single source of truth for ALL dependencies
├── runtime.txt              ← Python 3.12.0 for Streamlit Cloud
├── render.yaml              ← Python 3.12.0 for Render
├── setup.py                 ← Auto-reads from requirements.txt
├── DEPLOYMENT.md            ← Complete deployment guide
├── src/                     ← API & core logic
├── dashboard/               ← Streamlit dashboard
├── tests/                   ← Test suite
└── scripts/                 ← Utility scripts
```

## 🌐 Deployments

### API (Render)
Push to GitHub → Render auto-deploys with `requirements.txt`

### Dashboard (Streamlit Cloud)  
Push to GitHub → Streamlit Cloud auto-deploys with `requirements.txt`

Both use **Python 3.12.0** and **same dependencies** - no conflicts!

---

For detailed deployment instructions and troubleshooting, see [DEPLOYMENT.md](DEPLOYMENT.md)

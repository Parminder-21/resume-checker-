# QUICK START GUIDE - OptiResume AI

## ⚡ 5-Minute Setup

### Windows PowerShell Setup

```powershell
# 1. Open two PowerShell terminals

# TERMINAL 1: Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python run.py

# TERMINAL 2: Frontend
cd frontend
npm install
npm run dev
```

### What You'll See
- Backend: `INFO:     Application startup complete` on localhost:8000
- Frontend: Opens automatically at localhost:5173

## 🔑 API Key Setup

1. Get Anthropic API key from: https://console.anthropic.com/
2. Copy the key starting with `sk-ant-`
3. Add to `backend/.env`: `ANTHROPIC_API_KEY=sk-ant-xxxx`

## ✅ Verify Installation

Backend is ready when:
- `uvicorn running on http://0.0.0.0:8000`
- API docs available at http://localhost:8000/docs

Frontend is ready when:
- React dev server shows `ready in Xms`
- Browser opens to http://localhost:5173

## 🎯 Test the App

1. **Upload Resume**
   - Click drag-drop zone or select file
   - Use any PDF resume

2. **Paste Job Description**
   - Scroll to "sample data" section for examples
   - Or paste real job description

3. **Click "Optimize My Resume"**
   - Wait 8-10 seconds for processing
   - View before/after scores
   - Download optimized PDF

## 📋 File Locations

| Component | Start Command | Port | Docs |
|-----------|---------------|------|------|
| Backend | `python run.py` | 8000 | http://localhost:8000/docs |
| Frontend | `npm run dev` | 5173 | http://localhost:5173 |
| Logs | Check console | - | Both terminals |

## ⚠️ Common Issues

### "Module not found" errors
```bash
pip install -r requirements.txt --upgrade
```

### SBERT model not downloading
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### CORS/API connection errors
- Ensure backend is running
- Clear browser cache
- Check ALLOWED_ORIGINS in .env

### Claude API errors
- Verify ANTHROPIC_API_KEY is correct
- Check API quota on console.anthropic.com
- Ensure model name matches available models

## 🚀 Demo Day Checklist

- [ ] Backend running & API passing /health check
- [ ] Frontend loads without errors
- [ ] Sample data section works
- [ ] Can upload PDF resume
- [ ] Can paste job description
- [ ] Optimization returns results in <10 sec
- [ ] PDF download works
- [ ] Before/After scores visible and improved
- [ ] All logos/styling display correctly

## 📖 Detailed Setup

For full setup guide, see: `docs/SETUP.md`
For architecture details, see: `docs/architecture.md`
For troubleshooting, see: `docs/SETUP.md#troubleshooting`

---
**Questions?** Check the documentation folder or run with DEBUG=True for verbose logs

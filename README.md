# OptiResume AI
Real-time ATS Simulator & Resume Optimizer with Measurable Improvement

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm  # Download language model
python run.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

The app will open at `http://localhost:5173`

## 🔧 Configuration

Create a `.env` file in the `backend` folder:
```env
ANTHROPIC_API_KEY=your_key_here
MODEL_NAME=claude-sonnet-4-20250514
SBERT_MODEL=all-MiniLM-L6-v2
ALLOWED_ORIGINS=http://localhost:5173
MAX_TOKENS=2000
```

## 📁 Project Structure
- `frontend/` - React + Vite UI
- `backend/` - FastAPI server
- `ai_engine/` - AI/NLP modules
- `data/` - Sample data for testing
- `docs/` - Complete documentation

## ✨ Features
- 📄 PDF resume upload & parsing
- 🤖 AI-powered resume rewriting with Claude
- 📊 Multi-dimensional ATS scoring
- 🎯 Skill gap detection
- 👀 Side-by-side resume comparison
- 💾 PDF download of optimized resume

## 📋 Tech Stack
- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, Python
- **AI**: Claude API, Sentence Transformers (SBERT), spaCy
- **PDF**: pdfplumber, ReportLab

## 🏆 Demo Flow
1. Upload PDF resume
2. Paste job description
3. System optimizes resume with AI
4. View before/after scores & improvements
5. Download optimized PDF

---
**Version**: 1.0.0 | **Status**: Hackathon MVP ✅

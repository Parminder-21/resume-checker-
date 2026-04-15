# OptiResume AI

Real-time ATS Simulator & Resume Optimizer with AI-powered resume enhancement.

## 🚀 Features

- **PDF Resume Upload & Parsing** - Extract text from PDF resumes
- **ATS Score Calculation** - Real-time scoring based on job description
- **Skill Gap Analysis** - Identify missing skills with priority levels
- **AI Resume Rewriting** - Intelligent bullet point optimization using Groq API
- **Resume Diff Viewer** - See what changed in your resume
- **PDF Download** - Export optimized resume as PDF

## ⚡ Tech Stack

**Backend:**
- FastAPI (Python)
- Groq API (Free LLM for optimization)
- Sentence Transformers (Semantic matching)
- PostgreSQL support

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Framer Motion

**Deployment Ready:**
- Docker support
- CI/CD with GitHub Actions

---

## 🔑 Prerequisites

1. **Groq API Key** (FREE) - Get from https://console.groq.com
2. **Node.js** v16+ (for frontend)
3. **Python** 3.8+ (for backend)

---

## 📦 Setup & Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Groq API

Create `.env` file in `backend/`:

```env
GROQ_API_KEY=gsk_your_api_key_here
MODEL_NAME=mixtral-8x7b-32768
SBERT_MODEL=all-MiniLM-L6-v2
MAX_TOKENS=2000
ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend Setup

```bash
cd frontend
npm install
```

---

## 🎯 Running the Application

### Option 1: Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```
Backend runs on: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs on: http://localhost:5173

### Option 2: Using Batch Files (Windows)

```bash
START_ALL.bat
```

---

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| POST | `/api/v1/upload` | Upload resume PDF |
| POST | `/api/v1/optimize` | Run optimization pipeline |
| POST | `/api/v1/download` | Generate optimized PDF |

### API Documentation

Interactive documentation available at: **http://localhost:8000/docs**

---

## 🧪 Testing

Run comprehensive tests:

```bash
cd backend
python test_api.py
```

Tests include:
- ✅ Health check
- ✅ Resume upload
- ✅ Optimization pipeline
- ✅ PDF generation

---

## 📂 Project Structure

```
resume-checker/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── routes/           # API endpoints
│   │   ├── services/         # Business logic
│   │   ├── models/           # Pydantic models
│   │   └── core/             # Config & utils
│   ├── .env                  # Environment variables
│   ├── requirements.txt      # Python dependencies
│   └── run.py               # Start script
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API client
│   │   └── utils/           # Helpers
│   ├── package.json         # npm dependencies
│   └── vite.config.js       # Vite config
│
├── ai_engine/
│   ├── pdf/                 # PDF operations
│   ├── embedding/           # Semantic matching
│   ├── extraction/          # Text extraction
│   ├── rewriting/           # LLM rewriting
│   └── scoring/             # ATS scoring
│
└── data/
    ├── sample_resumes/      # Test resumes
    └── job_descriptions/    # Test JDs
```

---

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
# Required
GROQ_API_KEY=gsk_your_key
MODEL_NAME=mixtral-8x7b-32768  # or llama2-70b-4096, llama-2-7b-chat

# Optional
SBERT_MODEL=all-MiniLM-L6-v2
MAX_TOKENS=2000
ALLOWED_ORIGINS=http://localhost:5173
```

### CORS Configuration

Update `ALLOWED_ORIGINS` in `.env` for production:
```env
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

---

## 🚀 Deployment

### Docker

```bash
docker build -t optiresume-api ./backend
docker run -p 8000:8000 --env-file backend/.env optiresume-api
```

### Vercel Frontend (Recommended)

```bash
cd frontend
npm run build
vercel deploy --prod
```

### Heroku Backend

```bash
heroku create your-app-name
git push heroku main
```
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

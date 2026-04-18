# OptiResume AI

Real-time ATS Simulator & Resume Optimizer with AI-powered resume enhancement.

## 🚀 Features

- **Secure Authentication** - Full JWT-based user login and registration system.
- **PDF Resume Upload & Parsing** - Extract text from PDF resumes accurately.
- **ATS Score Calculation** - Real-time scoring based on semantic match and keyword overlap.
- **Skill Gap Analysis** - Identify missing skills with priority levels.
- **AI Resume Rewriting** - Intelligent bullet point optimization using Groq API (Mixtral/Llama).
- **Resume Diff Viewer** - See what changed in your resume side-by-side.
- **Professional PDF Download** - Export optimized resume as a highly-structured ATS-safe PDF (powered by `docx2pdf` and `python-docx`).

## ⚡ Tech Stack

**Backend:**
- FastAPI (Python)
- Groq API (Free LLM for optimization)
- Sentence Transformers (Semantic matching SBERT)
- SQLite (Local Database)
- PyJWT & Passlib (Authentication)

**Frontend:**
- React 18 & Vite
- Tailwind CSS & Framer Motion
- Axios (API Client)

**PDF Engine:**
- python-docx (Document structuring)
- docx2pdf (Native Windows Word COM integration for perfect PDF export)

---

## 🔑 Prerequisites

1. **Groq API Key** (FREE) - Get from https://console.groq.com
2. **Node.js** v16+ (for frontend)
3. **Python** 3.8+ (for backend)
4. **Microsoft Word** (installed locally for native PDF conversion via docx2pdf)

---

## 📦 Setup & Installation

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure Backend Environment

Create a `.env` file in `backend/`:

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

### Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
# Backend runs on: http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend runs on: http://localhost:5173
```

*(Optional for Windows)*: You can double click `START_ALL.bat` in the root directory to launch both automatically.

---

## 📊 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | Authenticate user & get JWT Token | No |
| POST | `/register` | Register new user account | No |
| POST | `/api/v1/optimize` | Run multi-modal optimization pipeline | Yes |
| POST | `/api/v1/download` | Generate optimized PDF | Yes |

### API Documentation
Interactive documentation available at: **http://localhost:8000/docs**

---

## 📂 Project Structure

```
resume-checker/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI server
│   │   ├── routes/           # API endpoints (auth, optimize, download)
│   │   ├── services/         # Handlers (parser, scoring, rewriter, pdf)
│   │   ├── models/           # DB tables & Pydantic models
│   │   └── core/             # JWT Security & Config
│   ├── .env                  
│   ├── requirements.txt      
│   └── run.py               
│
├── frontend/
│   ├── src/
│   │   ├── components/       # UI elements
│   │   ├── context/          # Auth context state
│   │   ├── pages/            # Home, Result, AuthPage
│   │   └── services/         # API client connection
│
├── ai_engine/
│   ├── pdf/                 # PDF layout and MS Word integration
│   ├── embedding/           # SBERT Semantic mapping
│   ├── extraction/          # NLP text extraction
│   ├── rewriting/           # LLM rewriting prompts
│   └── scoring/             # ATS logic
│
└── data/                    # Sample testing assets
```

---
**Version**: 1.1.0 | **Status**: Production Ready ✅

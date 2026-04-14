# Installation & Setup Guide for OptiResume AI

## Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn
- Git

## Backend Setup (Windows)

### 1. Create and activate virtual environment
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Create .env file
Create `backend/.env`:
```env
ANTHROPIC_API_KEY=sk-ant-your-key
MODEL_NAME=claude-sonnet-4-20250514
SBERT_MODEL=all-MiniLM-L6-v2
ALLOWED_ORIGINS=http://localhost:5173
MAX_TOKENS=2000
```

### 4. Pre-download SBERT model (optional but recommended)
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### 5. Run backend server
```bash
python run.py
```
Server runs at: http://localhost:8000
API Docs at: http://localhost:8000/docs

## Frontend Setup

### 1. Install dependencies
```bash
cd frontend
npm install
```

### 2. Start development server
```bash
npm run dev
```
App opens at: http://localhost:5173

## Testing

### Upload Sample Files
- Sample resume: `data/sample_resumes/weak_resume.txt`
- Sample JD: `data/job_descriptions/senior_backend_jd.txt`

### Manual Testing Steps
1. Go to http://localhost:5173
2. Upload the weak_resume.pdf (convert txt to PDF or use any resume)
3. Paste the job description
4. Click "Optimize My Resume"
5. Review results (scores should improve significantly)
6. Download optimized PDF

## Troubleshooting

### SBERT Model Not Loading
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### API Connection Error
- Ensure backend is running on port 8000
- Check CORS is enabled (should be in main.py)
- Clear browser cache

### PDF Upload Fails
- Ensure file is valid PDF
- Max file size is 5MB
- Try text-based input instead

## Deployment (Demo Day)

### Option 1: Local Only (Recommended)
- No internet required
- Zero latency issues
- Most reliable for demo

### Option 2: Cloud Deploym

ent
- **Backend**: Render, Railway, or Heroku
- **Frontend**: Vercel, Netlify, or GitHub Pages
- Set environment variables in cloud dashboard

## Performance Tips

- Pre-load SBERT model before demo
- Have test resume and JD ready
- Test end-to-end before demo day
- Monitor token usage with Claude API
- Run both servers 30 mins before demo to warm up

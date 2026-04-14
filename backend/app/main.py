from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, optimize, download
from app.core.config import settings
from sentence_transformers import SentenceTransformer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="OptiResume AI",
    version="1.0.0",
    description="Real-time ATS Simulator & Resume Optimizer"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load SBERT model once at startup
@app.on_event("startup")
async def load_models():
    try:
        logger.info("Loading SBERT model...")
        app.state.sbert_model = SentenceTransformer('all-MiniLM-L6-v2')
        logger.info("✅ SBERT model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load SBERT model: {e}")
        raise

# Register routers
app.include_router(upload.router, prefix="/api/v1", tags=["Resume Operations"])
app.include_router(optimize.router, prefix="/api/v1", tags=["Optimization"])
app.include_router(download.router, prefix="/api/v1", tags=["Download"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "OptiResume AI API v1.0.0 - Hackathon MVP"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

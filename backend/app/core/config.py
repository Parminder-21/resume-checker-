import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
backend_dir = Path(__file__).parent.parent.parent
env_path = backend_dir / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "mixtral-8x7b-32768")
    SBERT_MODEL: str = os.getenv("SBERT_MODEL", "all-MiniLM-L6-v2")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "2000"))
    ALLOWED_ORIGINS: list = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    MAX_FILE_SIZE_MB: int = 5
    MAX_RESUME_CHARS: int = 8000   # truncate before LLM call
    MIN_SCORE_FLOOR: float = 10.0

settings = Settings()
# AI Engine - Embedding module
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity(text_a: str, text_b: str, model) -> float:
    """
    Compute semantic similarity between two texts using SBERT.
    Returns score 0-100.
    """
    try:
        emb_a = model.encode([text_a])
        emb_b = model.encode([text_b])
        raw = cosine_similarity(emb_a, emb_b)[0][0]
        
        # Normalize from [0.2, 0.9] range to [0, 100]
        normalized = (raw - 0.2) / (0.9 - 0.2)
        score = max(10.0, min(100.0, normalized * 100))
        return round(score, 1)
    except Exception:
        return 50.0

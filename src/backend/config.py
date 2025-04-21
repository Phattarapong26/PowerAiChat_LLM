
import os
from typing import Dict, List

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/AI")
MONGODB_DB = os.getenv("MONGODB_DB", "AI")

# Language model configuration
MODEL_CONFIG = {
    'language_model': 'google/flan-t5-base',
    'embedding_model': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
}

# Available language options
LANGUAGE_OPTIONS = ["th", "en"]

# Consultation styles
CONSULTATION_STYLES = {
    "formal": "ทางการ", 
    "casual": "ทั่วไป", 
    "friendly": "เป็นกันเอง", 
    "professional": "มืออาชีพ"
}

# Vector search configuration
VECTOR_SIMILARITY_THRESHOLD = 0.8
MAX_RESULTS = 3


# File upload limits
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

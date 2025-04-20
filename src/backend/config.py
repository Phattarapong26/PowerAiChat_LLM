
import os
from typing import Dict, List

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/AI")
MONGODB_DB = os.getenv("MONGODB_DB", "AI")

# Language model configuration
MODEL_CONFIG = {
    'language_model': 'google/flan-t5-base',
    'embedding_model': 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2',
    'translation_model': 'Helsinki-NLP/opus-mt-th-en'
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
VECTOR_SIMILARITY_THRESHOLD = 0.1
MAX_RESULTS = 5

# API security
API_KEY_NAME = "X-API-Key"
API_KEY = os.getenv("API_KEY", "test_api_key")  # Default for development

# File upload limits
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB

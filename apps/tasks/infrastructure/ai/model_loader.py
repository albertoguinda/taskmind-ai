"""
Model Loader - Singleton pattern.

Loads Hugging Face models once and caches them in memory.
This prevents loading models on every request (expensive operation).
"""

import os
from typing import Dict, Any
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Singleton class to load and cache Hugging Face models.
    
    Models are loaded once at startup and kept in memory.
    This significantly improves performance.
    """
    
    _instance = None
    _models: Dict[str, Any] = {}
    
    def __new__(cls):
        """Singleton pattern - only one instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize (only once due to singleton)."""
        if not self._models:
            logger.info("🤖 Loading Hugging Face models...")
            self._load_models()
    
    def _load_models(self):
        """Load all required models."""
        try:
            # Set cache directory
            cache_dir = os.getenv('TRANSFORMERS_CACHE', '/app/.cache/huggingface')
            
            # 1. Zero-shot classification (for urgency)
            logger.info("📦 Loading zero-shot classifier...")
            self._models['classifier'] = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                cache_dir=cache_dir,
                device=-1,  # CPU (-1), GPU (0)
            )
            logger.info("✅ Zero-shot classifier loaded")
            
            # 2. Sentiment analysis
            logger.info("📦 Loading sentiment analyzer...")
            self._models['sentiment'] = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                cache_dir=cache_dir,
                device=-1,
            )
            logger.info("✅ Sentiment analyzer loaded")
            
            # 3. Named Entity Recognition (for keyword extraction)
            logger.info("📦 Loading NER model...")
            self._models['ner'] = pipeline(
                "ner",
                model="dslim/bert-base-NER",
                device=-1,
                aggregation_strategy="simple",
            )
            logger.info("✅ NER model loaded")
            
            logger.info("🎉 All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading models: {e}")
            logger.warning("⚠️  Falling back to Mock AI")
            raise
    
    @property
    def classifier(self):
        """Get zero-shot classifier."""
        return self._models.get('classifier')
    
    @property
    def sentiment(self):
        """Get sentiment analyzer."""
        return self._models.get('sentiment')
    
    @property
    def ner(self):
        """Get NER model."""
        return self._models.get('ner')
    
    def is_loaded(self) -> bool:
        """Check if models are loaded."""
        return len(self._models) > 0


# Global instance
model_loader = ModelLoader()
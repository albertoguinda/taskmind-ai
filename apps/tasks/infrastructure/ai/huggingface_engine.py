"""
Hugging Face AI Engine.

Real AI implementation using Hugging Face Transformers.
Provides intelligent task analysis using state-of-the-art NLP models.
"""

from typing import List, Set
import logging

from apps.tasks.domain import Analysis, UrgencyScore
from .ai_service import AIService
from .model_loader import model_loader

logger = logging.getLogger(__name__)


class HuggingFaceEngine(AIService):
    """
    Real AI engine using Hugging Face models.
    
    Features:
    - Zero-shot classification for urgency detection
    - Sentiment analysis for emotional context
    - Named Entity Recognition for keyword extraction
    - Multi-model ensemble for better accuracy
    """
    
    # Candidate labels for urgency classification
    URGENCY_LABELS = [
        "extremely urgent and critical",
        "high priority and important",
        "normal priority",
        "low priority and not urgent",
    ]
    
    # Keywords that boost urgency
    URGENT_KEYWORDS = {
        'urgent', 'critical', 'emergency', 'asap', 'immediately',
        'production', 'down', 'outage', 'broken', 'crash',
        'security', 'vulnerability', 'breach', 'hack',
        'bug', 'error', 'failure', 'issue', 'problem',
        'client', 'customer', 'deadline', 'today', 'now',
    }
    
    def __init__(self):
        """Initialize engine with models."""
        if not model_loader.is_loaded():
            raise RuntimeError("Hugging Face models not loaded")
        
        self.classifier = model_loader.classifier
        self.sentiment_analyzer = model_loader.sentiment
        self.ner = model_loader.ner
    
    def analyze_task_text(self, text: str) -> Analysis:
        """
        Analyze task text using AI.
        
        Args:
            text: Combined title + description
            
        Returns:
            Analysis with urgency score, keywords, confidence, sentiment
        """
        if not text or not text.strip():
            return Analysis.create_default()
        
        try:
            # 1. Zero-shot classification for urgency
            urgency_score, confidence = self._classify_urgency(text)
            
            # 2. Extract keywords (NER + custom logic)
            keywords = self._extract_keywords(text)
            
            # 3. Sentiment analysis
            sentiment = self._analyze_sentiment(text)
            
            # 4. Boost urgency if critical keywords present
            urgency_score = self._apply_keyword_boost(text, urgency_score)
            
            logger.info(f"✅ AI Analysis: urgency={urgency_score:.2f}, keywords={len(keywords)}")
            
            return Analysis(
                urgency_score=UrgencyScore(value=urgency_score),
                keywords=keywords,
                confidence=confidence,
                sentiment=sentiment,
            )
            
        except Exception as e:
            logger.error(f"❌ AI analysis failed: {e}")
            # Fallback to default
            return Analysis.create_default()
    
    def _classify_urgency(self, text: str) -> tuple[float, float]:
        """
        Classify text urgency using zero-shot classification.
        
        Returns:
            (urgency_score, confidence)
        """
        result = self.classifier(
            text,
            candidate_labels=self.URGENCY_LABELS,
            multi_label=False,
        )
        
        # Map labels to urgency scores
        label_scores = {
            "extremely urgent and critical": 1.0,
            "high priority and important": 0.75,
            "normal priority": 0.5,
            "low priority and not urgent": 0.2,
        }
        
        top_label = result['labels'][0]
        top_score = result['scores'][0]
        
        urgency = label_scores.get(top_label, 0.5)
        
        logger.debug(f"Urgency classification: {top_label} (confidence: {top_score:.2f})")
        
        return urgency, top_score
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract keywords using NER + custom logic.
        
        Returns:
            List of important keywords
        """
        keywords: Set[str] = set()
        
        # 1. Named Entity Recognition
        try:
            entities = self.ner(text)
            for entity in entities:
                word = entity['word'].replace('##', '').strip()
                if len(word) > 2:  # Skip very short tokens
                    keywords.add(word.lower())
        except Exception as e:
            logger.warning(f"NER extraction failed: {e}")
        
        # 2. Check for urgent keywords
        text_lower = text.lower()
        for keyword in self.URGENT_KEYWORDS:
            if keyword in text_lower:
                keywords.add(keyword)
        
        # 3. Extract capitalized words (likely important)
        words = text.split()
        for word in words:
            if word and word[0].isupper() and len(word) > 3:
                clean_word = ''.join(c for c in word if c.isalnum())
                if clean_word:
                    keywords.add(clean_word.lower())
        
        # Return top 10 keywords
        return sorted(list(keywords))[:10]
    
    def _analyze_sentiment(self, text: str) -> float:
        """
        Analyze sentiment of text.
        
        Returns:
            Sentiment score (-1 to 1)
        """
        try:
            result = self.sentiment_analyzer(text)[0]
            
            # Convert to -1 to 1 scale
            label = result['label']  # 'POSITIVE' or 'NEGATIVE'
            score = result['score']  # 0 to 1
            
            if label == 'NEGATIVE':
                return -score
            else:
                return score
                
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {e}")
            return 0.0
    
    def _apply_keyword_boost(self, text: str, base_score: float) -> float:
        """
        Boost urgency if critical keywords are present.
        
        Args:
            text: Task text
            base_score: Base urgency from classification
            
        Returns:
            Adjusted urgency score
        """
        text_lower = text.lower()
        
        # Count critical keywords
        critical_count = sum(
            1 for keyword in ['critical', 'urgent', 'emergency', 'production', 'down']
            if keyword in text_lower
        )
        
        # Boost by 0.1 per critical keyword (max +0.3)
        boost = min(critical_count * 0.1, 0.3)
        
        # Cap at 1.0
        return min(base_score + boost, 1.0)
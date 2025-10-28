"""
Motor de IA con Hugging Face.

Implementación real de IA usando modelos Transformers.
"""

from typing import List, Set, Tuple
import logging

from apps.tasks.domain import Analysis, UrgencyScore
from .ai_service import AIService
from .model_loader import model_loader

logger = logging.getLogger(__name__)


class HuggingFaceEngine(AIService):
    """Motor de IA usando modelos de Hugging Face."""
    
    # Etiquetas para clasificación de urgencia
    URGENCY_LABELS = [
        "extremely urgent and critical",
        "high priority and important",
        "normal priority",
        "low priority and not urgent",
    ]
    
    # Keywords que incrementan urgencia
    URGENT_KEYWORDS = {
        'urgent', 'critical', 'emergency', 'asap', 'immediately',
        'production', 'down', 'outage', 'broken', 'crash',
        'security', 'vulnerability', 'breach', 'hack',
        'bug', 'error', 'failure', 'issue', 'problem',
        'client', 'customer', 'deadline', 'today', 'now',
    }
    
    # Mapeo de etiquetas a scores
    LABEL_TO_SCORE = {
        "extremely urgent and critical": 1.0,
        "high priority and important": 0.75,
        "normal priority": 0.5,
        "low priority and not urgent": 0.2,
    }
    
    def __init__(self):
        """Inicializa el motor verificando modelos cargados."""
        if not model_loader.is_loaded():
            raise RuntimeError("Modelos de Hugging Face no cargados")
        
        self.classifier = model_loader.classifier
        self.sentiment_analyzer = model_loader.sentiment
        self.ner = model_loader.ner
        
        logger.info("✅ HuggingFaceEngine inicializado")
    
    def analyze_task_text(self, text: str) -> Analysis:
        """Analiza el texto de una tarea usando IA."""
        if not text or not text.strip():
            logger.warning("⚠️ Texto vacío")
            return Analysis.create_default()
        
        try:
            # Clasificar urgencia
            urgency_score, confidence = self._classify_urgency(text)
            
            # Extraer keywords
            keywords = self._extract_keywords(text)
            
            # Analizar sentimiento
            sentiment = self._analyze_sentiment(text)
            
            # Aplicar boost por keywords críticos
            urgency_score = self._apply_keyword_boost(text, urgency_score)
            
            logger.info(
                f"✅ Análisis: urgencia={urgency_score:.2f}, "
                f"keywords={len(keywords)}, sentimiento={sentiment:.2f}"
            )
            
            return Analysis(
                urgency_score=UrgencyScore(value=urgency_score),
                keywords=keywords,
                confidence=confidence,
                sentiment=sentiment,
            )
            
        except Exception as e:
            logger.error(f"❌ Error en análisis: {e}", exc_info=True)
            return Analysis.create_default()
    
    def _classify_urgency(self, text: str) -> Tuple[float, float]:
        """Clasifica urgencia usando zero-shot classification."""
        try:
            result = self.classifier(
                text,
                candidate_labels=self.URGENCY_LABELS,
                multi_label=False,
            )
            
            top_label = result['labels'][0]
            top_confidence = result['scores'][0]
            urgency_score = self.LABEL_TO_SCORE.get(top_label, 0.5)
            
            logger.debug(f"Clasificación: '{top_label}' (urgencia={urgency_score:.2f})")
            
            return urgency_score, top_confidence
            
        except Exception as e:
            logger.error(f"❌ Error en clasificación: {e}")
            return 0.5, 0.5
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrae keywords usando NER + lógica personalizada."""
        keywords: Set[str] = set()
        
        # 1. Named Entity Recognition
        try:
            entities = self.ner(text)
            for entity in entities:
                word = entity['word'].replace('##', '').strip()
                if len(word) > 2:
                    keywords.add(word.lower())
        except Exception as e:
            logger.warning(f"⚠️ NER falló: {e}")
        
        # 2. Keywords urgentes predefinidos
        text_lower = text.lower()
        for keyword in self.URGENT_KEYWORDS:
            if keyword in text_lower:
                keywords.add(keyword)
        
        # 3. Palabras capitalizadas (nombres propios, tecnologías)
        words = text.split()
        for word in words:
            if word and word[0].isupper() and len(word) > 3:
                clean_word = ''.join(c for c in word if c.isalnum())
                if clean_word:
                    keywords.add(clean_word.lower())
        
        return sorted(list(keywords))[:10]
    
    def _analyze_sentiment(self, text: str) -> float:
        """Analiza sentimiento emocional del texto."""
        try:
            result = self.sentiment_analyzer(text)[0]
            label = result['label']
            score = result['score']
            
            # Convertir a escala -1 a 1
            return -score if label == 'NEGATIVE' else score
                
        except Exception as e:
            logger.warning(f"⚠️ Sentimiento falló: {e}")
            return 0.0
    
    def _apply_keyword_boost(self, text: str, base_score: float) -> float:
        """Incrementa urgencia si hay keywords críticos."""
        text_lower = text.lower()
        critical_keywords = ['critical', 'urgent', 'emergency', 'production', 'down']
        
        # Contar keywords críticos
        critical_count = sum(1 for kw in critical_keywords if kw in text_lower)
        
        # Boost: +0.1 por keyword, máximo +0.3
        boost = min(critical_count * 0.1, 0.3)
        adjusted_score = min(base_score + boost, 1.0)
        
        if boost > 0:
            logger.debug(f"Boost: +{boost:.2f} ({base_score:.2f} → {adjusted_score:.2f})")
        
        return adjusted_score
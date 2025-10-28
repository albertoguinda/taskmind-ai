"""
Entidad Analysis del Dominio.

Representa el resultado del análisis de IA sobre una tarea.
"""

from dataclasses import dataclass, field
from typing import List

from ..value_objects import UrgencyScore


@dataclass
class Analysis:
    """
    Resultado del análisis de IA sobre una tarea.
    
    Esta entidad encapsula toda la información que el motor de IA
    extrae del texto de una tarea: urgencia, keywords, confianza y sentimiento.
    
    Es inmutable por diseño (dataclass sin métodos mutadores) y representa
    un snapshot del análisis en un momento específico.
    
    Atributos:
        urgency_score: Puntuación de urgencia calculada (0.0-1.0)
        keywords: Lista de keywords extraídos del texto (máx. 10)
        confidence: Nivel de confianza del modelo en el análisis (0.0-1.0)
        sentiment: Puntuación de sentimiento emocional (-1.0 a 1.0)
                -1.0 = muy negativo, 0.0 = neutral, 1.0 = muy positivo
    
    Invariantes:
        - urgency_score debe estar en el rango válido (validado por UrgencyScore)
        - confidence debe estar entre 0.0 y 1.0
        - sentiment debe estar entre -1.0 y 1.0
        - keywords debe ser una lista (puede estar vacía)
    
    Ejemplo:
        >>> analysis = Analysis(
        ...     urgency_score=UrgencyScore(0.85),
        ...     keywords=["bug", "production", "urgent"],
        ...     confidence=0.92,
        ...     sentiment=-0.3
        ... )
        >>> assert analysis.is_high_confidence()
        >>> assert analysis.is_negative_sentiment()
    """
    
    # Campo obligatorio: resultado principal del análisis
    urgency_score: UrgencyScore
    
    # Campos opcionales con valores por defecto
    keywords: List[str] = field(default_factory=list)
    confidence: float = 1.0  # 1.0 = confianza máxima por defecto
    sentiment: float = 0.0   # 0.0 = neutral por defecto
    
    def __post_init__(self):
        """
        Validación automática después de inicialización.
        Garantiza que los invariantes se cumplan siempre.
        
        Raises:
            ValueError: Si algún valor está fuera de rango válido
        """
        # Validar rango de confidence
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                f"Confidence debe estar entre 0.0 y 1.0, "
                f"se recibió: {self.confidence}"
            )
        
        # Validar rango de sentiment
        if not -1.0 <= self.sentiment <= 1.0:
            raise ValueError(
                f"Sentiment debe estar entre -1.0 y 1.0, "
                f"se recibió: {self.sentiment}"
            )
        
        # Limpiar keywords: eliminar vacíos y duplicados
        if self.keywords:
            self.keywords = list(set(k.strip() for k in self.keywords if k.strip()))
    
    # ==========================================
    # Factory Methods
    # ==========================================
    
    @classmethod
    def create_default(cls) -> "Analysis":
        """
        Crea un análisis por defecto (fallback cuando la IA falla).
        
        Usado cuando:
        - El motor de IA no está disponible
        - Ocurre un error durante el análisis
        - El texto de entrada está vacío
        
        Returns:
            Analysis con urgencia media, sin keywords y baja confianza
        
        Ejemplo:
            >>> fallback = Analysis.create_default()
            >>> assert fallback.urgency_score.value == 0.5
            >>> assert not fallback.is_high_confidence()
        """
        return cls(
            urgency_score=UrgencyScore.default(),
            keywords=[],
            confidence=0.5,  # Baja confianza indica que es fallback
            sentiment=0.0,    # Neutral
        )
    
    @classmethod
    def from_mock(cls, urgency: float = 0.5) -> "Analysis":
        """
        Crea un análisis mock para testing.
        
        Args:
            urgency: Valor de urgencia a simular (default: 0.5)
        
        Returns:
            Analysis con valores de prueba
        
        Ejemplo:
            >>> mock = Analysis.from_mock(urgency=0.9)
            >>> assert mock.urgency_score.value == 0.9
        """
        return cls(
            urgency_score=UrgencyScore(urgency),
            keywords=["test", "mock", "keyword"],
            confidence=0.8,
            sentiment=0.0,
        )
    
    # ==========================================
    # Query Methods (Métodos de Consulta)
    # ==========================================
    
    def is_high_confidence(self) -> bool:
        """
        Verifica si el análisis tiene alta confianza (> 0.8).
        
        Análisis con alta confianza pueden usarse directamente.
        Análisis con baja confianza deberían revisarse manualmente.
        
        Returns:
            True si confidence > 0.8
        """
        return self.confidence > 0.8
    
    def is_low_confidence(self) -> bool:
        """
        Verifica si el análisis tiene baja confianza (< 0.6).
        
        Returns:
            True si confidence < 0.6
        """
        return self.confidence < 0.6
    
    def is_positive_sentiment(self) -> bool:
        """
        Verifica si el sentimiento es positivo (> 0.2).
        
        Sentimiento positivo indica texto constructivo, optimista.
        
        Returns:
            True si sentiment > 0.2
        """
        return self.sentiment > 0.2
    
    def is_negative_sentiment(self) -> bool:
        """
        Verifica si el sentimiento es negativo (< -0.2).
        
        Sentimiento negativo indica frustración, urgencia, problema.
        
        Returns:
            True si sentiment < -0.2
        """
        return self.sentiment < -0.2
    
    def is_neutral_sentiment(self) -> bool:
        """
        Verifica si el sentimiento es neutral (-0.2 <= sentiment <= 0.2).
        
        Returns:
            True si sentiment está en rango neutral
        """
        return -0.2 <= self.sentiment <= 0.2
    
    def has_keywords(self) -> bool:
        """
        Verifica si se extrajeron keywords del análisis.
        
        Returns:
            True si hay al menos un keyword
        """
        return len(self.keywords) > 0
    
    def keyword_count(self) -> int:
        """
        Retorna el número de keywords extraídos.
        
        Returns:
            Cantidad de keywords
        """
        return len(self.keywords)
    
    # ==========================================
    # Métodos de Utilidad
    # ==========================================
    
    def get_sentiment_label(self) -> str:
        """
        Obtiene etiqueta descriptiva del sentimiento.
        
        Returns:
            String descriptivo: "positivo", "neutral" o "negativo"
        """
        if self.is_positive_sentiment():
            return "positivo"
        elif self.is_negative_sentiment():
            return "negativo"
        else:
            return "neutral"
    
    def get_confidence_label(self) -> str:
        """
        Obtiene etiqueta descriptiva de la confianza.
        
        Returns:
            String descriptivo: "alta", "media" o "baja"
        """
        if self.is_high_confidence():
            return "alta"
        elif self.is_low_confidence():
            return "baja"
        else:
            return "media"
    
    def to_dict(self) -> dict:
        """
        Convierte el análisis a diccionario (útil para serialización).
        
        Returns:
            Dict con todos los campos del análisis
        """
        return {
            'urgency_score': float(self.urgency_score),
            'keywords': self.keywords,
            'confidence': self.confidence,
            'sentiment': self.sentiment,
        }
    
    # ==========================================
    # Métodos Dunder (Representación)
    # ==========================================
    
    def __str__(self) -> str:
        """
        Representación legible para humanos.
        Muestra información resumida del análisis.
        """
        return (
            f"Analysis(urgencia={float(self.urgency_score):.2f}, "
            f"confianza={self.confidence:.2f}, "
            f"keywords={len(self.keywords)}, "
            f"sentimiento={self.get_sentiment_label()})"
        )
    
    def __repr__(self) -> str:
        """
        Representación completa para desarrolladores.
        Muestra todos los campos con valores exactos.
        """
        return (
            f"Analysis("
            f"urgency_score={float(self.urgency_score):.2f}, "
            f"keywords={self.keywords}, "
            f"confidence={self.confidence:.2f}, "
            f"sentiment={self.sentiment:.2f})"
        )
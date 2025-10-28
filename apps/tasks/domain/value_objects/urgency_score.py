"""
Value Object UrgencyScore.

Representa la puntuación de urgencia de una tarea calculada por IA (0.0-1.0).
Implementa un value object inmutable con validación automática.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class UrgencyScore:
    """
    Puntuación de urgencia calculada por IA.
    
    Value object inmutable que garantiza que el score esté siempre
    en el rango válido [0.0, 1.0]. La inmutabilidad (frozen=True)
    previene modificaciones accidentales después de la creación.
    
    Umbrales de Urgencia:
        - 0.0 - 0.3:  Baja urgencia
        - 0.3 - 0.7:  Urgencia media
        - 0.7 - 0.85: Alta urgencia
        - 0.85 - 1.0: Crítico
    
    Atributos:
        value: Float entre 0.0 (nada urgente) y 1.0 (extremadamente urgente)
    
    Ejemplos:
        >>> score = UrgencyScore(0.85)
        >>> assert score.is_critical()
        >>> assert float(score) == 0.85
        
        >>> score.value = 0.5  # TypeError: frozen instance
    """
    
    value: float
    
    def __post_init__(self):
        """
        Validación automática después de inicialización.
        Garantiza que el score esté siempre en rango válido.
        
        Raises:
            ValueError: Si el valor no es numérico o está fuera de rango
        """
        # Validar tipo de dato
        if not isinstance(self.value, (int, float)):
            raise ValueError(
                f"UrgencyScore debe ser un número, "
                f"se recibió: {type(self.value).__name__}"
            )
        
        # Validar rango [0.0, 1.0]
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(
                f"UrgencyScore debe estar entre 0.0 y 1.0, "
                f"se recibió: {self.value}"
            )
    
    # ==========================================
    # Factory Methods
    # ==========================================
    
    @classmethod
    def from_raw(cls, score: float) -> "UrgencyScore":
        """
        Crea un UrgencyScore desde un score sin validar.
        
        Clampea automáticamente valores fuera de rango a [0.0, 1.0].
        Útil cuando el score viene de fuentes externas no confiables.
        
        Args:
            score: Score sin validar (será clampeado)
        
        Returns:
            UrgencyScore con valor clampeado
        
        Ejemplos:
            >>> UrgencyScore.from_raw(1.5).value
            1.0
            >>> UrgencyScore.from_raw(-0.2).value
            0.0
            >>> UrgencyScore.from_raw(0.75).value
            0.75
        """
        clamped = max(0.0, min(1.0, float(score)))
        return cls(value=clamped)
    
    @classmethod
    def default(cls) -> "UrgencyScore":
        """
        Crea un UrgencyScore por defecto (urgencia media: 0.5).
        
        Usado como fallback cuando:
        - No hay análisis de IA disponible
        - Ocurre un error durante el análisis
        - El texto está vacío
        
        Returns:
            UrgencyScore con valor 0.5
        """
        return cls(value=0.5)
    
    @classmethod
    def low(cls) -> "UrgencyScore":
        """Crea un UrgencyScore de baja urgencia (0.2)."""
        return cls(value=0.2)
    
    @classmethod
    def medium(cls) -> "UrgencyScore":
        """Crea un UrgencyScore de urgencia media (0.5)."""
        return cls(value=0.5)
    
    @classmethod
    def high(cls) -> "UrgencyScore":
        """Crea un UrgencyScore de alta urgencia (0.75)."""
        return cls(value=0.75)
    
    @classmethod
    def critical(cls) -> "UrgencyScore":
        """Crea un UrgencyScore crítico (0.95)."""
        return cls(value=0.95)
    
    # ==========================================
    # Query Methods (Clasificación por Umbrales)
    # ==========================================
    
    def is_low(self) -> bool:
        """
        Verifica si la urgencia es baja (< 0.3).
        
        Returns:
            True si value < 0.3
        """
        return self.value < 0.3
    
    def is_medium(self) -> bool:
        """
        Verifica si la urgencia es media (0.3 <= value < 0.7).
        
        Returns:
            True si está en rango medio
        """
        return 0.3 <= self.value < 0.7
    
    def is_urgent(self) -> bool:
        """
        Verifica si la tarea es urgente (value >= 0.7).
        
        Umbral: 0.7 es el punto donde requiere atención inmediata.
        
        Returns:
            True si value >= 0.7
        """
        return self.value >= 0.7
    
    def is_critical(self) -> bool:
        """
        Verifica si la tarea es crítica (value >= 0.85).
        
        Umbral: 0.85 indica máxima prioridad, atención inmediata obligatoria.
        
        Returns:
            True si value >= 0.85
        """
        return self.value >= 0.85
    
    # ==========================================
    # Métodos de Utilidad
    # ==========================================
    
    def get_level(self) -> Literal["low", "medium", "high", "critical"]:
        """
        Obtiene el nivel de urgencia como string.
        
        Útil para categorización y filtrado.
        
        Returns:
            "critical" si >= 0.85
            "high" si >= 0.7
            "medium" si >= 0.3
            "low" si < 0.3
        
        Ejemplo:
            >>> UrgencyScore(0.9).get_level()
            'critical'
        """
        if self.is_critical():
            return "critical"
        elif self.is_urgent():
            return "high"
        elif self.is_medium():
            return "medium"
        else:
            return "low"
    
    def get_label(self) -> str:
        """
        Obtiene etiqueta descriptiva en español.
        
        Returns:
            String descriptivo del nivel de urgencia
        
        Ejemplo:
            >>> UrgencyScore(0.9).get_label()
            'Crítico'
        """
        level_labels = {
            "critical": "Crítico",
            "high": "Alta",
            "medium": "Media",
            "low": "Baja"
        }
        return level_labels[self.get_level()]
    
    def to_percentage(self) -> int:
        """
        Convierte el score a porcentaje (0-100).
        
        Returns:
            Entero entre 0 y 100
        
        Ejemplo:
            >>> UrgencyScore(0.75).to_percentage()
            75
        """
        return int(self.value * 100)
    
    # ==========================================
    # Operadores de Comparación
    # ==========================================
    
    def __lt__(self, other: "UrgencyScore") -> bool:
        """Menor que: permite comparar scores."""
        if not isinstance(other, UrgencyScore):
            return NotImplemented
        return self.value < other.value
    
    def __le__(self, other: "UrgencyScore") -> bool:
        """Menor o igual que."""
        if not isinstance(other, UrgencyScore):
            return NotImplemented
        return self.value <= other.value
    
    def __gt__(self, other: "UrgencyScore") -> bool:
        """Mayor que."""
        if not isinstance(other, UrgencyScore):
            return NotImplemented
        return self.value > other.value
    
    def __ge__(self, other: "UrgencyScore") -> bool:
        """Mayor o igual que."""
        if not isinstance(other, UrgencyScore):
            return NotImplemented
        return self.value >= other.value
    
    # ==========================================
    # Conversión de Tipos
    # ==========================================
    
    def __float__(self) -> float:
        """
        Convierte a float para cálculos matemáticos.
        
        Permite usar UrgencyScore en operaciones numéricas:
        >>> score = UrgencyScore(0.75)
        >>> result = float(score) * 2  # 1.5
        """
        return self.value
    
    def __int__(self) -> int:
        """
        Convierte a int (porcentaje sin decimales).
        
        Ejemplo:
            >>> int(UrgencyScore(0.753))
            75
        """
        return self.to_percentage()
    
    # ==========================================
    # Representación
    # ==========================================
    
    def __str__(self) -> str:
        """
        Representación legible para humanos.
        Formato: dos decimales.
        """
        return f"{self.value:.2f}"
    
    def __repr__(self) -> str:
        """
        Representación para desarrolladores.
        Muestra el constructor completo.
        """
        return f"UrgencyScore(value={self.value:.2f})"
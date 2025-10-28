"""
Value Object Priority.

Representa el nivel de prioridad de una tarea.
Enum inmutable ordenado de menor a mayor prioridad.
"""

from enum import Enum


class Priority(str, Enum):
    """
    Niveles de prioridad de tareas.
    
    Ordenados de menor a mayor: LOW < MEDIUM < HIGH < CRITICAL
    """
    
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    
    @classmethod
    def from_urgency_score(cls, score: float) -> "Priority":
        """
        Calcula la prioridad desde un urgency_score (0.0-1.0).
        
        Reglas de negocio:
        - 0.0 - 0.3:  LOW
        - 0.3 - 0.6:  MEDIUM
        - 0.6 - 0.85: HIGH
        - 0.85 - 1.0: CRITICAL
        
        Args:
            score: Puntuación de urgencia [0.0, 1.0]
        
        Returns:
            Priority correspondiente
        """
        if score < 0.3:
            return cls.LOW
        elif score < 0.6:
            return cls.MEDIUM
        elif score < 0.85:
            return cls.HIGH
        else:
            return cls.CRITICAL
    
    def to_label(self) -> str:
        """Retorna etiqueta en español."""
        labels = {
            Priority.LOW: "Baja",
            Priority.MEDIUM: "Media",
            Priority.HIGH: "Alta",
            Priority.CRITICAL: "Crítica"
        }
        return labels[self]
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"<Priority.{self.name}>"
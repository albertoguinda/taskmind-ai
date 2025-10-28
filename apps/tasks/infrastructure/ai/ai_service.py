"""
Interfaz de Servicio de IA.

Define el contrato que deben cumplir todos los servicios de análisis con IA.
Permite intercambiar implementaciones (Hugging Face, OpenAI, Mock, etc).
"""

from abc import ABC, abstractmethod
from typing import Protocol

from apps.tasks.domain import Analysis


class AIService(ABC):
    """
    Servicio abstracto de IA para análisis de tareas.
    
    Esta interfaz define el contrato que cualquier implementación de IA
    debe cumplir. Permite intercambiar motores de IA sin cambiar el código
    del dominio o aplicación (Dependency Inversion Principle).
    
    Implementaciones disponibles:
    - HuggingFaceEngine: IA real con modelos Transformers
    - MockAIService: IA simulada para testing
    - OpenAIService: (futuro) Integración con GPT
    
    Ejemplo:
        >>> ai_service: AIService = HuggingFaceEngine()
        >>> analysis = ai_service.analyze_task_text("Fix critical bug in production")
        >>> print(analysis.urgency_score.value)  # 0.95
    """
    
    @abstractmethod
    def analyze_task_text(self, text: str) -> Analysis:
        """
        Analiza el texto de una tarea y retorna insights de IA.
        
        Este método debe ser thread-safe y idempotente (misma entrada = misma salida).
        
        Args:
            text: Texto combinado de título + descripción de la tarea.
                Puede estar vacío (retornar análisis por defecto).
        
        Returns:
            Analysis: Objeto con urgency_score, keywords, confidence y sentiment.
                Nunca debe retornar None (usar Analysis.create_default() en caso de error).
        
        Raises:
            RuntimeError: Si el servicio de IA no está disponible o inicializado.
            ValueError: Si el texto tiene formato inválido (raramente usado).
        
        Performance:
            - Debe completarse en < 2 segundos para mantener buena UX
            - Considerar caché si el mismo texto se analiza múltiples veces
        
        Ejemplo:
            >>> text = "URGENT: Production server down, customers affected"
            >>> analysis = service.analyze_task_text(text)
            >>> assert analysis.urgency_score.value > 0.8
            >>> assert 'urgent' in analysis.keywords
        """
        pass


# Type alias para claridad en type hints
AIServiceProtocol = AIService
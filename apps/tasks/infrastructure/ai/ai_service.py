"""
AI Service Interface.

Defines the contract for AI analysis services.
"""

from abc import ABC, abstractmethod

from apps.tasks.domain import Analysis


class AIService(ABC):
    """
    Abstract AI service.
    
    This interface defines how to interact with AI for task analysis.
    Implementations can use Hugging Face, OpenAI, etc.
    """
    
    @abstractmethod
    def analyze_task_text(self, text: str) -> Analysis:
        """
        Analyze task text and return AI insights.
        
        Args:
            text: Combined title and description
            
        Returns:
            Analysis with urgency score and keywords
        """
        pass
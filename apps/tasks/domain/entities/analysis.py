"""
Analysis Entity.

Represents the result of AI analysis on a task.
"""

from dataclasses import dataclass, field
from typing import List

from ..value_objects import UrgencyScore


@dataclass
class Analysis:
    """
    AI Analysis result.
    
    Represents the output of AI analysis on task text.
    This is what the AI engine returns.
    
    Attributes:
        urgency_score: Calculated urgency (0-1)
        keywords: Extracted keywords
        confidence: AI confidence in the analysis (0-1)
        sentiment: Optional sentiment score (-1 to 1)
    """
    
    urgency_score: UrgencyScore
    keywords: List[str] = field(default_factory=list)
    confidence: float = 1.0
    sentiment: float = 0.0
    
    def __post_init__(self):
        """Validate analysis on creation."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0 and 1, got {self.confidence}")
        
        if not -1.0 <= self.sentiment <= 1.0:
            raise ValueError(f"Sentiment must be between -1 and 1, got {self.sentiment}")
    
    @classmethod
    def create_default(cls) -> "Analysis":
        """
        Create a default analysis (fallback when AI fails).
        
        Returns:
            Analysis with medium urgency and low confidence
        """
        return cls(
            urgency_score=UrgencyScore.default(),
            keywords=[],
            confidence=0.5,
            sentiment=0.0,
        )
    
    def is_high_confidence(self) -> bool:
        """Check if analysis has high confidence (>0.8)."""
        return self.confidence > 0.8
    
    def is_positive_sentiment(self) -> bool:
        """Check if sentiment is positive."""
        return self.sentiment > 0.2
    
    def is_negative_sentiment(self) -> bool:
        """Check if sentiment is negative."""
        return self.sentiment < -0.2
    
    def __str__(self) -> str:
        """Human-readable representation."""
        return (
            f"Analysis(urgency={self.urgency_score}, "
            f"confidence={self.confidence:.2f}, "
            f"keywords={len(self.keywords)})"
        )
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"Analysis(urgency_score={self.urgency_score}, "
            f"keywords={self.keywords}, "
            f"confidence={self.confidence:.2f}, "
            f"sentiment={self.sentiment:.2f})"
        )
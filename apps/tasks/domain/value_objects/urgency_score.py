"""
Urgency Score Value Object.

Represents the AI-calculated urgency of a task (0-1).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class UrgencyScore:
    """
    Urgency score calculated by AI.
    
    Immutable value object that ensures score is always valid (0-1).
    
    Attributes:
        value: Float between 0.0 (not urgent) and 1.0 (extremely urgent)
    """
    value: float
    
    def __post_init__(self):
        """Validate urgency score on creation."""
        if not isinstance(self.value, (int, float)):
            raise ValueError(f"Urgency score must be a number, got {type(self.value)}")
        
        if not 0.0 <= self.value <= 1.0:
            raise ValueError(f"Urgency score must be between 0 and 1, got {self.value}")
    
    @classmethod
    def from_raw(cls, score: float) -> "UrgencyScore":
        """
        Create from raw score, clamping to valid range.
        
        Args:
            score: Raw score (will be clamped to 0-1)
            
        Returns:
            UrgencyScore instance
            
        Examples:
            >>> UrgencyScore.from_raw(1.5)
            UrgencyScore(value=1.0)
            >>> UrgencyScore.from_raw(-0.2)
            UrgencyScore(value=0.0)
        """
        clamped = max(0.0, min(1.0, score))
        return cls(value=clamped)
    
    @classmethod
    def default(cls) -> "UrgencyScore":
        """Default urgency score (medium)."""
        return cls(value=0.5)
    
    def is_urgent(self) -> bool:
        """Check if task is urgent (threshold: 0.7)."""
        return self.value >= 0.7
    
    def is_critical(self) -> bool:
        """Check if task is critical (threshold: 0.85)."""
        return self.value >= 0.85
    
    def __float__(self) -> float:
        """Convert to float for calculations."""
        return self.value
    
    def __str__(self) -> str:
        return f"{self.value:.2f}"
    
    def __repr__(self) -> str:
        return f"UrgencyScore(value={self.value:.2f})"
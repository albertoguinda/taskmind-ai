"""
Priority Value Object.

Represents the priority level of a task.
This is a value object - immutable and defined by its value.
"""

from enum import Enum


class Priority(str, Enum):
    """
    Task priority levels.
    
    Ordered from lowest to highest priority.
    """
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    
    @classmethod
    def from_urgency_score(cls, score: float) -> "Priority":
        """
        Calculate priority from urgency score (0-1).
        
        Business rule:
        - 0.0 - 0.3: LOW
        - 0.3 - 0.6: MEDIUM
        - 0.6 - 0.85: HIGH
        - 0.85 - 1.0: CRITICAL
        
        Args:
            score: Urgency score between 0 and 1
            
        Returns:
            Priority level
            
        Examples:
            >>> Priority.from_urgency_score(0.2)
            <Priority.LOW: 'LOW'>
            >>> Priority.from_urgency_score(0.9)
            <Priority.CRITICAL: 'CRITICAL'>
        """
        if score < 0.3:
            return cls.LOW
        elif score < 0.6:
            return cls.MEDIUM
        elif score < 0.85:
            return cls.HIGH
        else:
            return cls.CRITICAL
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"<Priority.{self.name}: '{self.value}'>"
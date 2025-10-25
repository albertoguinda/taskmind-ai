"""
Task Entity.

Core domain entity representing a task in the system.
This is framework-agnostic - pure Python, no Django dependencies.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from ..value_objects import Priority, Status, UrgencyScore


@dataclass
class Task:
    """
    Task domain entity.
    
    Represents a task with all its business logic.
    This class is framework-agnostic and contains only domain logic.
    
    Attributes:
        id: Unique identifier
        title: Task title (required)
        description: Task description
        priority: Priority level (LOW, MEDIUM, HIGH, CRITICAL)
        status: Current status (TODO, IN_PROGRESS, DONE, CANCELLED)
        urgency_score: AI-calculated urgency (0-1)
        ai_keywords: Keywords extracted by AI
        created_at: When the task was created
        updated_at: When the task was last updated
    """
    
    # Required fields
    title: str
    description: str = ""
    
    # Value objects with defaults
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    urgency_score: UrgencyScore = field(default_factory=UrgencyScore.default)
    
    # Optional fields
    id: UUID = field(default_factory=uuid4)
    ai_keywords: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    
    def __post_init__(self):
        """Validate task on creation."""
        self._validate()
    
    def _validate(self):
        """
        Validate task business rules.
        
        Raises:
            ValueError: If validation fails
        """
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        
        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")
    
    # Business Logic Methods
    
    def update_urgency(self, score: UrgencyScore) -> None:
        """
        Update urgency score and recalculate priority.
        
        Business rule: Priority is automatically derived from urgency score.
        
        Args:
            score: New urgency score
        """
        self.urgency_score = score
        self.priority = Priority.from_urgency_score(float(score))
        self._mark_as_updated()
    
    def change_status(self, new_status: Status) -> None:
        """
        Change task status with validation.
        
        Business rule: Status transitions must be valid.
        
        Args:
            new_status: Target status
            
        Raises:
            ValueError: If transition is invalid
        """
        if not self.status.can_transition_to(new_status):
            raise ValueError(
                f"Cannot transition from {self.status} to {new_status}"
            )
        
        self.status = new_status
        self._mark_as_updated()
    
    def start_work(self) -> None:
        """
        Start working on the task.
        
        Business shortcut for: TODO -> IN_PROGRESS
        """
        self.change_status(Status.IN_PROGRESS)
    
    def complete(self) -> None:
        """
        Mark task as completed.
        
        Business shortcut for: IN_PROGRESS -> DONE
        """
        self.change_status(Status.DONE)
    
    def cancel(self) -> None:
        """
        Cancel the task.
        
        Can be called from any non-terminal state.
        """
        self.change_status(Status.CANCELLED)
    
    def add_keywords(self, keywords: List[str]) -> None:
        """
        Add AI-extracted keywords to the task.
        
        Args:
            keywords: List of keywords from AI analysis
        """
        # Remove duplicates and empty strings
        unique_keywords = list(set(k.strip() for k in keywords if k.strip()))
        self.ai_keywords = unique_keywords
        self._mark_as_updated()
    
    def is_urgent(self) -> bool:
        """Check if task is urgent based on urgency score."""
        return self.urgency_score.is_urgent()
    
    def is_critical(self) -> bool:
        """Check if task is critical based on urgency score."""
        return self.urgency_score.is_critical()
    
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == Status.DONE
    
    def is_in_progress(self) -> bool:
        """Check if task is being worked on."""
        return self.status == Status.IN_PROGRESS
    
    def _mark_as_updated(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()
    
    # Comparison and representation
    
    def __eq__(self, other: object) -> bool:
        """Two tasks are equal if they have the same ID."""
        if not isinstance(other, Task):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on ID for use in sets/dicts."""
        return hash(self.id)
    
    def __str__(self) -> str:
        """Human-readable representation."""
        return f"Task('{self.title}', {self.priority}, {self.status})"
    
    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"Task(id={self.id}, title='{self.title}', "
            f"priority={self.priority}, status={self.status}, "
            f"urgency_score={self.urgency_score})"
        )
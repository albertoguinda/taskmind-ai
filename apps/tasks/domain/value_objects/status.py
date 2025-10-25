"""
Status Value Object.

Represents the current state of a task in its lifecycle.
"""

from enum import Enum


class Status(str, Enum):
    """
    Task status states.
    
    Represents the workflow: TODO -> IN_PROGRESS -> DONE
    """
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    
    def can_transition_to(self, new_status: "Status") -> bool:
        """
        Check if transition to new status is valid.
        
        Business rules:
        - TODO can go to IN_PROGRESS or CANCELLED
        - IN_PROGRESS can go to DONE or CANCELLED
        - DONE is terminal (cannot change)
        - CANCELLED is terminal (cannot change)
        
        Args:
            new_status: Target status
            
        Returns:
            True if transition is valid
            
        Examples:
            >>> Status.TODO.can_transition_to(Status.IN_PROGRESS)
            True
            >>> Status.DONE.can_transition_to(Status.TODO)
            False
        """
        valid_transitions = {
            Status.TODO: {Status.IN_PROGRESS, Status.CANCELLED},
            Status.IN_PROGRESS: {Status.DONE, Status.CANCELLED},
            Status.DONE: set(),  # Terminal state
            Status.CANCELLED: set(),  # Terminal state
        }
        
        return new_status in valid_transitions.get(self, set())
    
    def is_terminal(self) -> bool:
        """Check if this is a terminal state (cannot transition)."""
        return self in {Status.DONE, Status.CANCELLED}
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"<Status.{self.name}: '{self.value}'>"
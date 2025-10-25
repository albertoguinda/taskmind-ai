"""
Command DTOs for Use Cases.

Commands represent the intent to perform an action.
They are immutable and validate input data.
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass(frozen=True)
class CreateTaskCommand:
    """
    Command to create a new task.
    
    This is the input for CreateTaskUseCase.
    """
    title: str
    description: str = ""
    
    def __post_init__(self):
        """Validate command."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")


@dataclass(frozen=True)
class UpdateTaskCommand:
    """
    Command to update an existing task.
    
    All fields except task_id are optional.
    """
    task_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    
    def __post_init__(self):
        """Validate command."""
        if self.title is not None:
            if not self.title.strip():
                raise ValueError("Title cannot be empty")
            if len(self.title) > 200:
                raise ValueError("Title cannot exceed 200 characters")


@dataclass(frozen=True)
class DeleteTaskCommand:
    """Command to delete a task."""
    task_id: UUID


@dataclass(frozen=True)
class GetTaskCommand:
    """Command to get a single task by ID."""
    task_id: UUID


@dataclass(frozen=True)
class GetTasksCommand:
    """
    Command to get multiple tasks with filters.
    
    All fields are optional for filtering.
    """
    status: Optional[str] = None
    priority: Optional[str] = None
    urgent_only: bool = False
    limit: Optional[int] = None
    offset: int = 0


@dataclass(frozen=True)
class AnalyzeTaskCommand:
    """Command to analyze a task with AI."""
    task_id: UUID
    force_reanalysis: bool = False
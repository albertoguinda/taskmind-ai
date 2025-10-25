"""
Response DTOs for Use Cases.

Responses represent the result of an action.
They are simple data containers for returning data to the interface layer.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class TaskResponse:
    """
    Response DTO for a single task.
    
    This is what the Use Cases return to the interface layer.
    It's a simple DTO, not a domain entity.
    """
    id: UUID
    title: str
    description: str
    priority: str
    status: str
    urgency_score: float
    ai_keywords: List[str]
    created_at: datetime
    updated_at: datetime
    
    @classmethod
    def from_entity(cls, task) -> "TaskResponse":
        """
        Create response from domain entity.
        
        Args:
            task: Task domain entity
            
        Returns:
            TaskResponse DTO
        """
        return cls(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority.value,
            status=task.status.value,
            urgency_score=float(task.urgency_score),
            ai_keywords=task.ai_keywords,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )


@dataclass
class TaskListResponse:
    """
    Response DTO for a list of tasks.
    
    Includes pagination metadata.
    """
    tasks: List[TaskResponse]
    total: int
    limit: Optional[int]
    offset: int
    
    @property
    def count(self) -> int:
        """Number of tasks in this response."""
        return len(self.tasks)


@dataclass
class AnalysisResponse:
    """
    Response DTO for AI analysis.
    
    This is what the AI analysis returns.
    """
    urgency_score: float
    keywords: List[str]
    confidence: float
    sentiment: float
    
    @classmethod
    def from_entity(cls, analysis) -> "AnalysisResponse":
        """
        Create response from Analysis entity.
        
        Args:
            analysis: Analysis domain entity
            
        Returns:
            AnalysisResponse DTO
        """
        return cls(
            urgency_score=float(analysis.urgency_score),
            keywords=analysis.keywords,
            confidence=analysis.confidence,
            sentiment=analysis.sentiment,
        )


@dataclass
class DeleteTaskResponse:
    """Response for task deletion."""
    success: bool
    task_id: UUID
    message: str = "Task deleted successfully"
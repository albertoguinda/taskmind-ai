"""
DTOs de Respuesta (Output).

Representan los datos que se devuelven al cliente.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from apps.tasks.domain import Task


@dataclass
class TaskResponse:
    """DTO de respuesta para una tarea individual."""
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
    def from_entity(cls, task: Task) -> "TaskResponse":
        """Crea TaskResponse desde entidad de dominio."""
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
    """DTO de respuesta para lista de tareas con metadata."""
    tasks: List[TaskResponse]
    total: int
    limit: Optional[int] = None
    offset: int = 0


@dataclass
class DeleteTaskResponse:
    """DTO de respuesta para operación de eliminación."""
    success: bool
    task_id: UUID
    message: str
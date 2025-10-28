"""
DTOs de Comandos (Input).

Representan las intenciones del usuario (commands/queries).
"""

from dataclasses import dataclass
from typing import Optional
from uuid import UUID


@dataclass
class CreateTaskCommand:
    """Comando para crear una nueva tarea."""
    title: str
    description: str = ""


@dataclass
class UpdateTaskCommand:
    """Comando para actualizar una tarea existente (partial update)."""
    task_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None


@dataclass
class GetTasksCommand:
    """Query para obtener tareas con filtros opcionales."""
    status: Optional[str] = None
    priority: Optional[str] = None
    urgent_only: bool = False
    limit: Optional[int] = None
    offset: int = 0
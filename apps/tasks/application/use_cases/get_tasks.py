"""
Caso de Uso: Obtener Tareas.

Recupera tareas del repositorio con filtros opcionales.
"""

import logging
from typing import List

from apps.tasks.domain import Task, TaskRepository, Priority, Status, TaskNotFoundException
from ..dtos import GetTasksCommand, TaskListResponse, TaskResponse

logger = logging.getLogger(__name__)


class GetTasksUseCase:
    """
    Caso de uso para obtener múltiples tareas con filtros.
    
    Soporta filtrado por:
    - Status
    - Priority
    - Solo urgentes
    - Paginación (limit/offset)
    """
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, command: GetTasksCommand) -> TaskListResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            command: Parámetros de consulta y filtros
        
        Returns:
            TaskListResponse con tareas y metadata
        """
        # Aplicar filtros
        if command.urgent_only:
            tasks = self.task_repository.find_urgent_tasks()
        elif command.status:
            status = Status(command.status)
            tasks = self.task_repository.find_by_status(status)
        elif command.priority:
            priority = Priority(command.priority)
            tasks = self.task_repository.find_by_priority(priority)
        else:
            tasks = self.task_repository.find_all()
        
        # Total antes de paginar
        total = len(tasks)
        
        # Aplicar paginación
        if command.limit:
            start = command.offset
            end = start + command.limit
            tasks = tasks[start:end]
        
        logger.info(f"Tareas obtenidas: {len(tasks)} de {total}")
        
        # Convertir a DTOs de respuesta
        task_responses = [TaskResponse.from_entity(t) for t in tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            limit=command.limit,
            offset=command.offset,
        )


class GetTaskByIdUseCase:
    """Caso de uso para obtener una tarea por ID."""
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id) -> TaskResponse:
        """
        Obtiene una tarea por su ID.
        
        Args:
            task_id: UUID de la tarea
        
        Returns:
            TaskResponse
        
        Raises:
            TaskNotFoundException: Si la tarea no existe
        """
        task = self.task_repository.find_by_id(task_id)
        
        if not task:
            raise TaskNotFoundException(task_id)
        
        return TaskResponse.from_entity(task)
"""
Caso de Uso: Actualizar Tarea.

Actualiza una tarea existente con nuevos datos (soporte para updates parciales).
"""

import logging
from apps.tasks.domain import (
    Task,
    TaskRepository,
    TaskNotFoundException,
    Priority,
    Status,
)
from ..dtos import UpdateTaskCommand, TaskResponse

logger = logging.getLogger(__name__)


class UpdateTaskUseCase:
    """
    Caso de uso para actualizar una tarea existente.
    Soporta updates parciales (solo los campos proporcionados se actualizan).
    """
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, command: UpdateTaskCommand) -> TaskResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            command: Comando con ID de tarea y datos a actualizar
        
        Returns:
            TaskResponse con la tarea actualizada
        
        Raises:
            TaskNotFoundException: Si la tarea no existe
            ValueError: Si la validación falla
        """
        # 1. Buscar tarea existente
        task = self.task_repository.find_by_id(command.task_id)
        
        if not task:
            raise TaskNotFoundException(command.task_id)
        
        # 2. Aplicar updates (solo campos proporcionados)
        if command.title is not None:
            task.title = command.title
        
        if command.description is not None:
            task.description = command.description
        
        if command.priority is not None:
            task.priority = Priority(command.priority)
        
        if command.status is not None:
            new_status = Status(command.status)
            task.change_status(new_status)  # Validación de dominio
        
        # 3. Marcar como actualizado
        task._mark_as_updated()
        
        # 4. Persistir
        updated_task = self.task_repository.save(task)
        
        logger.info(f"Tarea actualizada: {updated_task.id}")
        
        # 5. Retornar respuesta
        return TaskResponse.from_entity(updated_task)
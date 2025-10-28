"""
Caso de Uso: Eliminar Tarea.

Elimina una tarea del sistema.
"""

import logging
from uuid import UUID

from apps.tasks.domain import TaskRepository
from ..dtos import DeleteTaskResponse

logger = logging.getLogger(__name__)


class DeleteTaskUseCase:
    """
    Caso de uso para eliminar una tarea.
    Actualmente es hard delete, pero podría implementarse soft delete.
    """
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: UUID) -> DeleteTaskResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            task_id: UUID de la tarea a eliminar
        
        Returns:
            DeleteTaskResponse con el estado de la operación
        """
        success = self.task_repository.delete(task_id)
        
        if success:
            logger.info(f"Tarea eliminada: {task_id}")
            return DeleteTaskResponse(
                success=True,
                task_id=task_id,
                message="Tarea eliminada exitosamente"
            )
        else:
            logger.warning(f"Tarea no encontrada: {task_id}")
            return DeleteTaskResponse(
                success=False,
                task_id=task_id,
                message="Tarea no encontrada"
            )
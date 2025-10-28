"""
Caso de Uso: Priorizar Tareas.

Ordena tareas por urgencia calculada por IA.
"""

import logging
from typing import List

from apps.tasks.domain import Task, TaskRepository, TaskService
from ..dtos import TaskListResponse, TaskResponse

logger = logging.getLogger(__name__)


class PrioritizeTasksUseCase:
    """
    Caso de uso para obtener tareas ordenadas por urgencia de IA.
    
    Regla de negocio: Mayor urgency_score = más urgente = debe hacerse primero.
    """
    
    def __init__(
        self,
        task_repository: TaskRepository,
        task_service: TaskService = None,
    ):
        self.task_repository = task_repository
        self.task_service = task_service or TaskService()
    
    def execute(self, include_completed: bool = False) -> TaskListResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            include_completed: Si incluir tareas DONE/CANCELLED
        
        Returns:
            TaskListResponse con tareas ordenadas por urgencia (mayor primero)
        """
        # 1. Obtener todas las tareas
        all_tasks = self.task_repository.find_all()
        
        # 2. Filtrar completadas si es necesario
        if not include_completed:
            tasks = self.task_service.filter_actionable_tasks(all_tasks)
        else:
            tasks = all_tasks
        
        # 3. Ordenar por prioridad y urgencia (servicio de dominio)
        sorted_tasks = self.task_service.sort_by_priority(tasks)
        
        logger.info(f"Tareas priorizadas: {len(sorted_tasks)}")
        
        # 4. Convertir a DTOs de respuesta
        task_responses = [TaskResponse.from_entity(t) for t in sorted_tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=len(task_responses),
            limit=None,
            offset=0,
        )


class GetUrgentTasksUseCase:
    """
    Caso de uso para obtener solo tareas urgentes (urgency_score >= 0.7).
    """
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self) -> TaskListResponse:
        """
        Ejecuta el caso de uso.
        
        Returns:
            TaskListResponse con solo tareas urgentes
        """
        # Obtener tareas urgentes (consulta optimizada en repositorio)
        urgent_tasks = self.task_repository.find_urgent_tasks()
        
        logger.info(f"Tareas urgentes encontradas: {len(urgent_tasks)}")
        
        # Convertir a DTOs de respuesta
        task_responses = [TaskResponse.from_entity(t) for t in urgent_tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=len(task_responses),
            limit=None,
            offset=0,
        )
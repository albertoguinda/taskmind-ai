"""
Caso de Uso: Crear Tarea.

Orquesta la creación de una nueva tarea con análisis de IA.
"""

import logging
from typing import Optional

from apps.tasks.domain import Task, TaskRepository, TaskService
from apps.tasks.infrastructure.ai import AIService
from ..dtos import CreateTaskCommand, TaskResponse

logger = logging.getLogger(__name__)


class CreateTaskUseCase:
    """
    Caso de uso para crear una tarea con análisis de IA.
    
    Flujo:
    1. Crear entidad de dominio (Task)
    2. Validar reglas de negocio
    3. Analizar con IA (urgencia + keywords)
    4. Aplicar análisis a la tarea
    5. Persistir en repositorio
    6. Retornar DTO de respuesta
    """
    
    def __init__(
        self,
        task_repository: TaskRepository,
        ai_service: AIService,
        task_service: Optional[TaskService] = None,
    ):
        """
        Inicializa el caso de uso con sus dependencias.
        
        Args:
            task_repository: Repositorio para persistencia
            ai_service: Servicio de IA para análisis
            task_service: Servicio de dominio (opcional)
        """
        self.task_repository = task_repository
        self.ai_service = ai_service
        self.task_service = task_service or TaskService()
    
    def execute(self, command: CreateTaskCommand) -> TaskResponse:
        """
        Ejecuta el caso de uso.
        
        Args:
            command: Comando con los datos de la tarea
        
        Returns:
            TaskResponse con la tarea creada
        
        Raises:
            ValueError: Si la validación falla
        """
        # 1. Crear entidad de dominio
        task = Task(
            title=command.title,
            description=command.description,
        )
        
        # 2. Validar con servicio de dominio
        self.task_service.validate_task(task)
        
        # 3. Analizar con IA
        text_to_analyze = f"{task.title} {task.description}"
        
        try:
            analysis = self.ai_service.analyze_task_text(text_to_analyze)
            
            # 4. Aplicar análisis a la tarea
            self.task_service.apply_analysis_to_task(task, analysis)
            
            logger.info(
                f"Tarea analizada: urgencia={float(task.urgency_score):.2f}, "
                f"keywords={len(task.ai_keywords)}"
            )
            
        except Exception as e:
            # Resiliencia: si falla IA, usar valores por defecto
            logger.warning(f"Análisis IA falló: {e}. Usando valores por defecto.")
            # La tarea mantiene urgency_score y priority por defecto
        
        # 5. Persistir en repositorio
        saved_task = self.task_repository.save(task)
        
        logger.info(f"Tarea creada: {saved_task.id}")
        
        # 6. Retornar DTO de respuesta
        return TaskResponse.from_entity(saved_task)
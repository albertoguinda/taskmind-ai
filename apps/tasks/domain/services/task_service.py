"""
Servicio de Dominio para Task.

Contiene lógica de negocio que no encaja naturalmente en una sola entidad.
"""

from typing import List

from ..entities import Task, Analysis
from ..value_objects import Priority, Status, UrgencyScore


class TaskService:
    """
    Servicio de dominio para lógica de negocio relacionada con tareas.
    
    Casos de uso:
    - Lógica que involucra múltiples entidades
    - Reglas de negocio que no pertenecen a una sola entidad
    - Validaciones complejas
    """
    
    @staticmethod
    def calculate_priority_from_analysis(analysis: Analysis) -> Priority:
        """
        Calcula la prioridad desde un análisis de IA.
        
        Regla: La prioridad se deriva del urgency_score.
        """
        return Priority.from_urgency_score(float(analysis.urgency_score))
    
    @staticmethod
    def apply_analysis_to_task(task: Task, analysis: Analysis) -> None:
        """
        Aplica los resultados del análisis de IA a una tarea.
        
        Coordina entre las entidades Task y Analysis.
        """
        task.update_urgency(analysis.urgency_score)
        task.add_keywords(analysis.keywords)
    
    @staticmethod
    def validate_task(task: Task) -> None:
        """
        Valida reglas de negocio de una tarea.
        
        Raises:
            ValueError: Si la validación falla
        """
        if not task.title or not task.title.strip():
            raise ValueError("El título no puede estar vacío")
        
        if len(task.title) > 200:
            raise ValueError("El título no puede exceder 200 caracteres")
        
        if task.description and len(task.description) > 5000:
            raise ValueError("La descripción no puede exceder 5000 caracteres")
    
    @staticmethod
    def sort_by_priority(tasks: List[Task]) -> List[Task]:
        """
        Ordena tareas por prioridad y urgencia.
        
        Criterios:
        1. Prioridad (CRITICAL > HIGH > MEDIUM > LOW)
        2. Urgency score (mayor primero)
        3. Fecha de creación (más reciente primero)
        """
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3,
        }
        
        return sorted(
            tasks,
            key=lambda t: (
                priority_order[t.priority],
                -float(t.urgency_score),
                -t.created_at.timestamp(),
            ),
        )
    
    @staticmethod
    def filter_actionable_tasks(tasks: List[Task]) -> List[Task]:
        """
        Filtra tareas accionables (TODO o IN_PROGRESS).
        """
        return [
            task for task in tasks
            if task.status in {Status.TODO, Status.IN_PROGRESS}
        ]
    
    @staticmethod
    def get_urgent_and_incomplete(tasks: List[Task]) -> List[Task]:
        """
        Obtiene tareas urgentes e incompletas.
        
        Urgente: urgency_score >= 0.7
        Incompleta: no DONE ni CANCELLED
        """
        return [
            task for task in tasks
            if task.is_urgent() and not task.status.is_terminal()
        ]
    
    @staticmethod
    def can_start_task(task: Task) -> bool:
        """Verifica si una tarea puede iniciarse (status == TODO)."""
        return task.status == Status.TODO
    
    @staticmethod
    def can_complete_task(task: Task) -> bool:
        """Verifica si una tarea puede completarse (status == IN_PROGRESS)."""
        return task.status == Status.IN_PROGRESS
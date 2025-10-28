"""
Implementación del Repositorio con Django ORM.

Adapta Django ORM a la interfaz de dominio TaskRepository.
Convierte entre entidades de dominio (Task) y modelos ORM (TaskModel).
"""

from typing import List, Optional
from uuid import UUID
from django.db.models import Q

from apps.tasks.domain import Task, Priority, Status, UrgencyScore, TaskRepository
from .models import TaskModel


class DjangoTaskRepository(TaskRepository):
    """Implementación del repositorio usando Django ORM."""
    
    def save(self, task: Task) -> Task:
        """Guarda una tarea (create o update)."""
        task_model, created = TaskModel.objects.update_or_create(
            id=task.id,
            defaults={
                'title': task.title,
                'description': task.description,
                'priority': task.priority.value,
                'status': task.status.value,
                'urgency_score': float(task.urgency_score),
                'ai_keywords': task.ai_keywords,
            }
        )
        
        return self._to_domain(task_model)
    
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """Busca tarea por ID."""
        try:
            task_model = TaskModel.objects.get(id=task_id)
            return self._to_domain(task_model)
        except TaskModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[Task]:
        """Obtiene todas las tareas."""
        task_models = TaskModel.objects.all()
        return [self._to_domain(tm) for tm in task_models]
    
    def find_by_status(self, status: Status) -> List[Task]:
        """Busca tareas por estado."""
        task_models = TaskModel.objects.filter(status=status.value)
        return [self._to_domain(tm) for tm in task_models]
    
    def find_by_priority(self, priority: Priority) -> List[Task]:
        """Busca tareas por prioridad."""
        task_models = TaskModel.objects.filter(priority=priority.value)
        return [self._to_domain(tm) for tm in task_models]
    
    def find_urgent_tasks(self) -> List[Task]:
        """Busca tareas urgentes (urgency >= 0.7), ordenadas por urgencia."""
        task_models = TaskModel.objects.filter(
            urgency_score__gte=0.7
        ).order_by('-urgency_score')
        return [self._to_domain(tm) for tm in task_models]
    
    def find_by_keyword(self, keyword: str) -> List[Task]:
        """Busca tareas por keyword en título, descripción o keywords de IA."""
        task_models = TaskModel.objects.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(ai_keywords__contains=[keyword])
        )
        return [self._to_domain(tm) for tm in task_models]
    
    def delete(self, task_id: UUID) -> bool:
        """Elimina una tarea. Retorna True si existía."""
        deleted_count, _ = TaskModel.objects.filter(id=task_id).delete()
        return deleted_count > 0
    
    def exists(self, task_id: UUID) -> bool:
        """Verifica si una tarea existe."""
        return TaskModel.objects.filter(id=task_id).exists()
    
    def count(self) -> int:
        """Cuenta el total de tareas."""
        return TaskModel.objects.count()
    
    @staticmethod
    def _to_domain(task_model: TaskModel) -> Task:
        """Convierte modelo ORM a entidad de dominio."""
        return Task(
            id=task_model.id,
            title=task_model.title,
            description=task_model.description,
            priority=Priority(task_model.priority),
            status=Status(task_model.status),
            urgency_score=UrgencyScore(value=task_model.urgency_score),
            ai_keywords=task_model.ai_keywords or [],
            created_at=task_model.created_at,
            updated_at=task_model.updated_at,
        )
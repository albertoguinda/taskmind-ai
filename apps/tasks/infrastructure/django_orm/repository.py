"""
Django ORM Repository Implementation.

Implements TaskRepository interface using Django ORM.
This is where domain entities are converted to/from database models.
"""

from typing import List, Optional
from uuid import UUID

from apps.tasks.domain import Task, Priority, Status, UrgencyScore, TaskRepository
from .models import TaskModel


class DjangoTaskRepository(TaskRepository):
    """
    Django ORM implementation of TaskRepository.
    
    This class adapts Django ORM to our domain interface.
    It converts between domain entities (Task) and ORM models (TaskModel).
    
    This follows the Adapter pattern and Repository pattern.
    """
    
    def save(self, task: Task) -> Task:
        """
        Save a task (create or update).
        
        Args:
            task: Domain task entity
            
        Returns:
            Saved task entity
        """
        # Convert domain entity to ORM model
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
        
        # Convert back to domain entity with updated timestamps
        return self._to_domain(task_model)
    
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """Find task by ID."""
        try:
            task_model = TaskModel.objects.get(id=task_id)
            return self._to_domain(task_model)
        except TaskModel.DoesNotExist:
            return None
    
    def find_all(self) -> List[Task]:
        """Get all tasks."""
        task_models = TaskModel.objects.all()
        return [self._to_domain(tm) for tm in task_models]
    
    def find_by_status(self, status: Status) -> List[Task]:
        """Find tasks by status."""
        task_models = TaskModel.objects.filter(status=status.value)
        return [self._to_domain(tm) for tm in task_models]
    
    def find_by_priority(self, priority: Priority) -> List[Task]:
        """Find tasks by priority."""
        task_models = TaskModel.objects.filter(priority=priority.value)
        return [self._to_domain(tm) for tm in task_models]
    
    def find_urgent_tasks(self) -> List[Task]:
        """Find urgent tasks (urgency >= 0.7), sorted by urgency."""
        task_models = TaskModel.objects.filter(
            urgency_score__gte=0.7
        ).order_by('-urgency_score')
        return [self._to_domain(tm) for tm in task_models]
    
    def find_by_keyword(self, keyword: str) -> List[Task]:
        """Find tasks containing a keyword in title, description, or AI keywords."""
        from django.db.models import Q
        
        task_models = TaskModel.objects.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(ai_keywords__contains=[keyword])
        )
        return [self._to_domain(tm) for tm in task_models]
    
    def delete(self, task_id: UUID) -> bool:
        """Delete a task."""
        deleted_count, _ = TaskModel.objects.filter(id=task_id).delete()
        return deleted_count > 0
    
    def exists(self, task_id: UUID) -> bool:
        """Check if task exists."""
        return TaskModel.objects.filter(id=task_id).exists()
    
    def count(self) -> int:
        """Count total tasks."""
        return TaskModel.objects.count()
    
    # Private helper methods
    
    @staticmethod
    def _to_domain(task_model: TaskModel) -> Task:
        """
        Convert Django ORM model to domain entity.
        
        This is the mapping layer between infrastructure and domain.
        
        Args:
            task_model: Django ORM model
            
        Returns:
            Domain Task entity
        """
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
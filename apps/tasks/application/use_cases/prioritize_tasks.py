"""
Prioritize Tasks Use Case.

Orders tasks by AI-calculated urgency score.
"""

from typing import List

from apps.tasks.domain import Task, TaskRepository, TaskService
from ..dtos import TaskListResponse, TaskResponse


class PrioritizeTasksUseCase:
    """
    Use Case: Get tasks ordered by AI urgency.
    
    This is a specialized query that demonstrates the value of AI:
    Tasks are sorted by urgency_score (0-1) rather than manual priority.
    
    Business rule: Higher urgency_score = more urgent = should be done first.
    """
    
    def __init__(
        self,
        task_repository: TaskRepository,
        task_service: TaskService = None,
    ):
        """
        Initialize use case.
        
        Args:
            task_repository: Repository for task persistence
            task_service: Domain service for sorting logic
        """
        self.task_repository = task_repository
        self.task_service = task_service or TaskService()
    
    def execute(self, include_completed: bool = False) -> TaskListResponse:
        """
        Execute the use case.
        
        Args:
            include_completed: Whether to include DONE/CANCELLED tasks
            
        Returns:
            TaskListResponse with tasks sorted by urgency (highest first)
            
        Example:
            >>> response = use_case.execute(include_completed=False)
            >>> print(response.tasks[0].urgency_score)  # Highest
            0.95
            >>> print(response.tasks[-1].urgency_score)  # Lowest
            0.12
        """
        # 1. Get all tasks
        all_tasks = self.task_repository.find_all()
        
        # 2. Filter out completed if needed
        if not include_completed:
            tasks = self.task_service.filter_actionable_tasks(all_tasks)
        else:
            tasks = all_tasks
        
        # 3. Sort by priority and urgency (domain service)
        sorted_tasks = self.task_service.sort_by_priority(tasks)
        
        # 4. Convert to response DTOs
        task_responses = [TaskResponse.from_entity(t) for t in sorted_tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=len(task_responses),
            limit=None,
            offset=0,
        )


class GetUrgentTasksUseCase:
    """
    Use Case: Get only urgent tasks (urgency_score >= 0.7).
    
    This is a convenience use case for the most critical tasks.
    """
    
    def __init__(self, task_repository: TaskRepository):
        """
        Initialize use case.
        
        Args:
            task_repository: Repository for task persistence
        """
        self.task_repository = task_repository
    
    def execute(self) -> TaskListResponse:
        """
        Execute the use case.
        
        Returns:
            TaskListResponse with urgent tasks only
        """
        # Get urgent tasks (repository has this query optimized)
        urgent_tasks = self.task_repository.find_urgent_tasks()
        
        # Convert to response DTOs
        task_responses = [TaskResponse.from_entity(t) for t in urgent_tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=len(task_responses),
            limit=None,
            offset=0,
        )
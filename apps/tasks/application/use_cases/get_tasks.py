"""
Get Tasks Use Case.

Retrieves tasks from repository with optional filters.
"""

from typing import List

from apps.tasks.domain import Task, TaskRepository, Priority, Status
from ..dtos import GetTasksCommand, TaskListResponse, TaskResponse


class GetTasksUseCase:
    """
    Use Case: Get multiple tasks with filters.
    
    Supports filtering by:
    - Status
    - Priority
    - Urgent only
    - Pagination (limit/offset)
    """
    
    def __init__(self, task_repository: TaskRepository):
        """
        Initialize use case.
        
        Args:
            task_repository: Repository for task persistence
        """
        self.task_repository = task_repository
    
    def execute(self, command: GetTasksCommand) -> TaskListResponse:
        """
        Execute the use case.
        
        Args:
            command: Query parameters
            
        Returns:
            TaskListResponse with tasks and metadata
        """
        # Start with all tasks
        tasks: List[Task] = []
        
        # Apply filters
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
        
        # Get total before pagination
        total = len(tasks)
        
        # Apply pagination
        if command.limit:
            start = command.offset
            end = start + command.limit
            tasks = tasks[start:end]
        
        # Convert to response DTOs
        task_responses = [TaskResponse.from_entity(t) for t in tasks]
        
        return TaskListResponse(
            tasks=task_responses,
            total=total,
            limit=command.limit,
            offset=command.offset,
        )


class GetTaskByIdUseCase:
    """
    Use Case: Get a single task by ID.
    """
    
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id) -> TaskResponse:
        """
        Get task by ID.
        
        Args:
            task_id: UUID of the task
            
        Returns:
            TaskResponse
            
        Raises:
            TaskNotFoundException: If task not found
        """
        from apps.tasks.domain import TaskNotFoundException
        
        task = self.task_repository.find_by_id(task_id)
        
        if not task:
            raise TaskNotFoundException(task_id)
        
        return TaskResponse.from_entity(task)
"""
Update Task Use Case.

Updates an existing task with new data.
"""

from apps.tasks.domain import (
    Task,
    TaskRepository,
    TaskNotFoundException,
    Priority,
    Status,
)
from ..dtos import UpdateTaskCommand, TaskResponse


class UpdateTaskUseCase:
    """
    Use Case: Update an existing task.
    
    Supports partial updates (only provided fields are updated).
    """
    
    def __init__(self, task_repository: TaskRepository):
        """
        Initialize use case.
        
        Args:
            task_repository: Repository for task persistence
        """
        self.task_repository = task_repository
    
    def execute(self, command: UpdateTaskCommand) -> TaskResponse:
        """
        Execute the use case.
        
        Args:
            command: Update command with task ID and new data
            
        Returns:
            TaskResponse with updated task data
            
        Raises:
            TaskNotFoundException: If task not found
            ValueError: If validation fails
        """
        # 1. Find existing task
        task = self.task_repository.find_by_id(command.task_id)
        
        if not task:
            raise TaskNotFoundException(command.task_id)
        
        # 2. Apply updates (only provided fields)
        if command.title is not None:
            task.title = command.title
        
        if command.description is not None:
            task.description = command.description
        
        if command.priority is not None:
            task.priority = Priority(command.priority)
        
        if command.status is not None:
            new_status = Status(command.status)
            task.change_status(new_status)  # Uses domain validation
        
        # 3. Mark as updated
        task._mark_as_updated()
        
        # 4. Save
        updated_task = self.task_repository.save(task)
        
        # 5. Return response
        return TaskResponse.from_entity(updated_task)
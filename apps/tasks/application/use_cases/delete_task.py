"""
Delete Task Use Case.

Deletes a task from the system.
"""

from uuid import UUID

from apps.tasks.domain import TaskRepository
from ..dtos import DeleteTaskResponse


class DeleteTaskUseCase:
    """
    Use Case: Delete a task.
    
    Soft delete could be implemented here if needed.
    """
    
    def __init__(self, task_repository: TaskRepository):
        """
        Initialize use case.
        
        Args:
            task_repository: Repository for task persistence
        """
        self.task_repository = task_repository
    
    def execute(self, task_id: UUID) -> DeleteTaskResponse:
        """
        Execute the use case.
        
        Args:
            task_id: UUID of task to delete
            
        Returns:
            DeleteTaskResponse with success status
        """
        # Delete from repository
        success = self.task_repository.delete(task_id)
        
        if success:
            return DeleteTaskResponse(
                success=True,
                task_id=task_id,
                message="Task deleted successfully"
            )
        else:
            return DeleteTaskResponse(
                success=False,
                task_id=task_id,
                message="Task not found"
            )
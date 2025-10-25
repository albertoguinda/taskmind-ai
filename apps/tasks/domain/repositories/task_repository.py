"""
Task Repository Interface.

Defines the contract for task persistence.
This is an abstraction (port) that will be implemented by infrastructure layer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities import Task
from ..value_objects import Priority, Status


class TaskRepository(ABC):
    """
    Abstract repository for Task persistence.
    
    This interface defines what operations can be performed on tasks,
    but NOT how they are implemented.
    
    Implementations will be in the infrastructure layer (e.g., DjangoORMRepository).
    
    This follows the Dependency Inversion Principle:
    - High-level modules (use cases) depend on this abstraction
    - Low-level modules (Django ORM) implement this abstraction
    """
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Save a task (create or update).
        
        Args:
            task: Task entity to save
            
        Returns:
            Saved task (may have updated fields like timestamps)
        """
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """
        Find task by ID.
        
        Args:
            task_id: Task identifier
            
        Returns:
            Task if found, None otherwise
        """
        pass
    
    @abstractmethod
    def find_all(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        pass
    
    @abstractmethod
    def find_by_status(self, status: Status) -> List[Task]:
        """
        Find tasks by status.
        
        Args:
            status: Task status to filter by
            
        Returns:
            List of tasks with given status
        """
        pass
    
    @abstractmethod
    def find_by_priority(self, priority: Priority) -> List[Task]:
        """
        Find tasks by priority.
        
        Args:
            priority: Priority level to filter by
            
        Returns:
            List of tasks with given priority
        """
        pass
    
    @abstractmethod
    def find_urgent_tasks(self) -> List[Task]:
        """
        Find all urgent tasks (urgency_score >= 0.7).
        
        Returns:
            List of urgent tasks, sorted by urgency descending
        """
        pass
    
    @abstractmethod
    def find_by_keyword(self, keyword: str) -> List[Task]:
        """
        Find tasks containing a keyword.
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List of matching tasks
        """
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass
    
    @abstractmethod
    def exists(self, task_id: UUID) -> bool:
        """
        Check if task exists.
        
        Args:
            task_id: Task identifier
            
        Returns:
            True if exists, False otherwise
        """
        pass
    
    @abstractmethod
    def count(self) -> int:
        """
        Count total tasks.
        
        Returns:
            Number of tasks
        """
        pass
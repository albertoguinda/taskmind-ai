"""
Task Domain Service.

Contains business logic that doesn't naturally fit in a single entity.
"""

from typing import List

from ..entities import Task, Analysis
from ..value_objects import Priority, Status, UrgencyScore


class TaskService:
    """
    Domain service for task-related business logic.
    
    Use cases for domain services:
    - Logic that involves multiple entities
    - Business rules that don't belong to a single entity
    - Complex validations
    """
    
    @staticmethod
    def calculate_priority_from_analysis(analysis: Analysis) -> Priority:
        """
        Calculate task priority from AI analysis.
        
        Business rule: Priority is derived from urgency score.
        
        Args:
            analysis: AI analysis result
            
        Returns:
            Calculated priority level
        """
        return Priority.from_urgency_score(float(analysis.urgency_score))
    
    @staticmethod
    def apply_analysis_to_task(task: Task, analysis: Analysis) -> None:
        """
        Apply AI analysis results to a task.
        
        This is a domain service because it coordinates between
        Task and Analysis entities.
        
        Args:
            task: Task to update
            analysis: Analysis results to apply
        """
        task.update_urgency(analysis.urgency_score)
        task.add_keywords(analysis.keywords)
    
    @staticmethod
    def validate_task(task: Task) -> None:
        """
        Validate task business rules.
        
        Args:
            task: Task to validate
            
        Raises:
            ValueError: If validation fails
        """
        # Title validation
        if not task.title or not task.title.strip():
            raise ValueError("Task title cannot be empty")
        
        if len(task.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")
        
        # Description validation (optional but limited)
        if task.description and len(task.description) > 5000:
            raise ValueError("Task description cannot exceed 5000 characters")
    
    @staticmethod
    def sort_by_priority(tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by priority and urgency.
        
        Business rule:
        1. First by priority (CRITICAL > HIGH > MEDIUM > LOW)
        2. Then by urgency score (highest first)
        3. Then by creation date (newest first)
        
        Args:
            tasks: List of tasks to sort
            
        Returns:
            Sorted list of tasks
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
                -float(t.urgency_score),  # Negative for descending
                -t.created_at.timestamp(),  # Negative for newest first
            ),
        )
    
    @staticmethod
    def filter_actionable_tasks(tasks: List[Task]) -> List[Task]:
        """
        Filter tasks that can be acted upon.
        
        Business rule: Actionable = TODO or IN_PROGRESS
        
        Args:
            tasks: List of tasks to filter
            
        Returns:
            List of actionable tasks
        """
        return [
            task for task in tasks
            if task.status in {Status.TODO, Status.IN_PROGRESS}
        ]
    
    @staticmethod
    def get_urgent_and_incomplete(tasks: List[Task]) -> List[Task]:
        """
        Get tasks that are both urgent AND incomplete.
        
        Business rule: Urgent = urgency_score >= 0.7
                       Incomplete = not DONE or CANCELLED
        
        Args:
            tasks: List of tasks to filter
            
        Returns:
            List of urgent incomplete tasks
        """
        return [
            task for task in tasks
            if task.is_urgent() and not task.status.is_terminal()
        ]
    
    @staticmethod
    def can_start_task(task: Task) -> bool:
        """
        Check if a task can be started.
        
        Business rule: Can only start tasks in TODO status.
        
        Args:
            task: Task to check
            
        Returns:
            True if task can be started
        """
        return task.status == Status.TODO
    
    @staticmethod
    def can_complete_task(task: Task) -> bool:
        """
        Check if a task can be completed.
        
        Business rule: Can only complete tasks in IN_PROGRESS status.
        
        Args:
            task: Task to check
            
        Returns:
            True if task can be completed
        """
        return task.status == Status.IN_PROGRESS
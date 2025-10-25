"""
Domain Exceptions.

Custom exceptions for domain-specific errors.
"""


class DomainException(Exception):
    """Base exception for all domain errors."""
    pass


class TaskNotFoundException(DomainException):
    """Raised when a task is not found."""
    
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class InvalidTaskStateException(DomainException):
    """Raised when an operation is invalid for the current task state."""
    
    def __init__(self, message: str):
        super().__init__(message)


class InvalidPriorityException(DomainException):
    """Raised when an invalid priority is provided."""
    
    def __init__(self, priority: str):
        super().__init__(f"Invalid priority: {priority}")


class InvalidStatusException(DomainException):
    """Raised when an invalid status is provided."""
    
    def __init__(self, status: str):
        super().__init__(f"Invalid status: {status}")


class InvalidStatusTransitionException(DomainException):
    """Raised when a status transition is not allowed."""
    
    def __init__(self, from_status: str, to_status: str):
        super().__init__(
            f"Cannot transition from {from_status} to {to_status}"
        )


class ValidationException(DomainException):
    """Raised when domain validation fails."""
    
    def __init__(self, message: str):
        super().__init__(message)
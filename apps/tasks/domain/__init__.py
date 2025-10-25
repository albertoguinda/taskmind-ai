"""
Task Domain.

This package contains the core business logic of the application.
It is framework-agnostic and has no dependencies on Django or other infrastructure.

Architecture:
- entities: Domain objects with identity (Task, Analysis)
- value_objects: Immutable objects defined by their values (Priority, Status)
- repositories: Interfaces for data persistence (ports)
- services: Business logic that doesn't fit in entities
- exceptions: Domain-specific errors
"""

from .entities import Task, Analysis
from .value_objects import Priority, Status, UrgencyScore
from .repositories import TaskRepository
from .services import TaskService
from .exceptions import (
    DomainException,
    TaskNotFoundException,
    InvalidTaskStateException,
    ValidationException,
)

__all__ = [
    # Entities
    "Task",
    "Analysis",
    # Value Objects
    "Priority",
    "Status",
    "UrgencyScore",
    # Repositories
    "TaskRepository",
    # Services
    "TaskService",
    # Exceptions
    "DomainException",
    "TaskNotFoundException",
    "InvalidTaskStateException",
    "ValidationException",
]
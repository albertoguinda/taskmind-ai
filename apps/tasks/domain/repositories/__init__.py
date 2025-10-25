"""
Repository Interfaces (Ports).

Repositories define the contract for data persistence.
"""

from .task_repository import TaskRepository

__all__ = ["TaskRepository"]
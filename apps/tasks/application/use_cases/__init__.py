"""
Use Cases (Application Layer).

Use Cases orchestrate the flow of data to and from entities,
and direct those entities to use their business logic to achieve
the goals of the use case.

Each use case is a single, specific business operation.
"""

from .create_task import CreateTaskUseCase
from .get_tasks import GetTasksUseCase, GetTaskByIdUseCase
from .update_task import UpdateTaskUseCase
from .delete_task import DeleteTaskUseCase
from .prioritize_tasks import PrioritizeTasksUseCase, GetUrgentTasksUseCase

__all__ = [
    # CRUD
    "CreateTaskUseCase",
    "GetTasksUseCase",
    "GetTaskByIdUseCase",
    "UpdateTaskUseCase",
    "DeleteTaskUseCase",
    # AI-powered
    "PrioritizeTasksUseCase",
    "GetUrgentTasksUseCase",
]
"""
Application Layer.

This layer contains use cases that orchestrate the flow of data
between the domain layer and the infrastructure layer.

Use cases:
- Are framework-agnostic (no Django dependencies)
- Depend on domain abstractions (repositories, services)
- Return DTOs (not domain entities directly)
- Contain application-specific business logic

Architecture:
- use_cases/: Business operations
- dtos/: Data transfer objects (commands and responses)
"""

from .use_cases import (
    CreateTaskUseCase,
    GetTasksUseCase,
    GetTaskByIdUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
    PrioritizeTasksUseCase,
    GetUrgentTasksUseCase,
)

from .dtos import (
    CreateTaskCommand,
    UpdateTaskCommand,
    DeleteTaskCommand,
    GetTaskCommand,
    GetTasksCommand,
    TaskResponse,
    TaskListResponse,
    AnalysisResponse,
    DeleteTaskResponse,
)

__all__ = [
    # Use Cases
    "CreateTaskUseCase",
    "GetTasksUseCase",
    "GetTaskByIdUseCase",
    "UpdateTaskUseCase",
    "DeleteTaskUseCase",
    "PrioritizeTasksUseCase",
    "GetUrgentTasksUseCase",
    # DTOs - Commands
    "CreateTaskCommand",
    "UpdateTaskCommand",
    "DeleteTaskCommand",
    "GetTaskCommand",
    "GetTasksCommand",
    # DTOs - Responses
    "TaskResponse",
    "TaskListResponse",
    "AnalysisResponse",
    "DeleteTaskResponse",
]
"""
Data Transfer Objects (DTOs).

DTOs are simple data containers used to transfer data between layers.
They are immutable and contain no business logic.
"""

from .commands import (
    CreateTaskCommand,
    UpdateTaskCommand,
    DeleteTaskCommand,
    GetTaskCommand,
    GetTasksCommand,
    AnalyzeTaskCommand,
)

from .responses import (
    TaskResponse,
    TaskListResponse,
    AnalysisResponse,
    DeleteTaskResponse,
)

__all__ = [
    # Commands
    "CreateTaskCommand",
    "UpdateTaskCommand",
    "DeleteTaskCommand",
    "GetTaskCommand",
    "GetTasksCommand",
    "AnalyzeTaskCommand",
    # Responses
    "TaskResponse",
    "TaskListResponse",
    "AnalysisResponse",
    "DeleteTaskResponse",
]
"""
Create Task Use Case.

Orchestrates the creation of a new task with AI analysis.
"""

from typing import Optional

from apps.tasks.domain import Task, TaskRepository, TaskService
from apps.tasks.infrastructure.ai import AIService
from ..dtos import CreateTaskCommand, TaskResponse


class CreateTaskUseCase:
    """
    Use Case: Create a new task with AI analysis.
    
    Flow:
    1. Validate input (command)
    2. Create domain entity (Task)
    3. Analyze with AI (urgency score + keywords)
    4. Apply business rules (priority calculation)
    5. Save to repository
    6. Return response DTO
    
    This follows the Dependency Inversion Principle:
    - Depends on abstractions (TaskRepository, AIService)
    - Not on concrete implementations
    """
    
    def __init__(
        self,
        task_repository: TaskRepository,
        ai_service: AIService,
        task_service: Optional[TaskService] = None,
    ):
        """
        Initialize use case with dependencies.
        
        Args:
            task_repository: Repository for task persistence
            ai_service: Service for AI analysis
            task_service: Domain service for business logic (optional)
        """
        self.task_repository = task_repository
        self.ai_service = ai_service
        self.task_service = task_service or TaskService()
    
    def execute(self, command: CreateTaskCommand) -> TaskResponse:
        """
        Execute the use case.
        
        Args:
            command: Input command with task data
            
        Returns:
            TaskResponse with created task data
            
        Raises:
            ValueError: If validation fails
            
        Example:
            >>> command = CreateTaskCommand(
            ...     title="Fix production bug",
            ...     description="Server is down"
            ... )
            >>> response = use_case.execute(command)
            >>> print(response.urgency_score)
            0.95
        """
        # 1. Create domain entity
        task = Task(
            title=command.title,
            description=command.description,
        )
        
        # 2. Validate with domain service
        self.task_service.validate_task(task)
        
        # 3. Analyze with AI
        text_to_analyze = f"{task.title} {task.description}"
        
        try:
            analysis = self.ai_service.analyze_task_text(text_to_analyze)
            
            # 4. Apply analysis to task (domain service)
            self.task_service.apply_analysis_to_task(task, analysis)
            
        except Exception as e:
            # If AI fails, use default values (resilience)
            print(f"AI analysis failed: {e}. Using default values.")
            # Task keeps default urgency_score and priority
        
        # 5. Save to repository
        saved_task = self.task_repository.save(task)
        
        # 6. Return response DTO
        return TaskResponse.from_entity(saved_task)
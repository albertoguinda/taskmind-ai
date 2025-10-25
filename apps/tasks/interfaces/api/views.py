"""
API ViewSets.

ViewSets handle HTTP requests and delegate to Use Cases.
They are the entry point of the API.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.tasks.application import (
    CreateTaskUseCase,
    CreateTaskCommand,
    GetTasksUseCase,
    GetTasksCommand,
    GetTaskByIdUseCase,
    UpdateTaskUseCase,
    UpdateTaskCommand,
    DeleteTaskUseCase,
    PrioritizeTasksUseCase,
)
from apps.tasks.infrastructure.django_orm import DjangoTaskRepository
from apps.tasks.infrastructure.ai import HuggingFaceEngine  # ← CAMBIADO
from apps.tasks.domain import TaskNotFoundException

from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskListResponseSerializer,
)


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet for Task CRUD operations.
    
    Endpoints:
    - GET    /api/tasks/              - List all tasks
    - POST   /api/tasks/              - Create a new task
    - GET    /api/tasks/{id}/         - Get task detail
    - PATCH  /api/tasks/{id}/         - Update task
    - DELETE /api/tasks/{id}/         - Delete task
    - GET    /api/tasks/prioritized/  - Get tasks sorted by AI urgency
    """
    
    def __init__(self, **kwargs):
        """Initialize with dependencies."""
        super().__init__(**kwargs)
        # Dependency Injection (simple version)
        self.repository = DjangoTaskRepository()
        self.ai_service = HuggingFaceEngine()  # ← CAMBIADO
    
    @extend_schema(
        summary="List all tasks",
        parameters=[
            OpenApiParameter(name='status', description='Filter by status'),
            OpenApiParameter(name='priority', description='Filter by priority'),
            OpenApiParameter(name='urgent_only', description='Only urgent tasks', type=bool),
        ],
        responses={200: TaskListResponseSerializer}
    )
    def list(self, request):
        """
        List all tasks with optional filters.
        
        Query parameters:
        - status: Filter by status (TODO, IN_PROGRESS, DONE, CANCELLED)
        - priority: Filter by priority (LOW, MEDIUM, HIGH, CRITICAL)
        - urgent_only: Only show urgent tasks (true/false)
        """
        # Parse query parameters
        status_filter = request.query_params.get('status')
        priority_filter = request.query_params.get('priority')
        urgent_only = request.query_params.get('urgent_only', 'false').lower() == 'true'
        
        # Create command
        command = GetTasksCommand(
            status=status_filter,
            priority=priority_filter,
            urgent_only=urgent_only,
        )
        
        # Execute use case
        use_case = GetTasksUseCase(self.repository)
        result = use_case.execute(command)
        
        # Serialize response
        serializer = TaskListResponseSerializer({
            'tasks': [task.__dict__ for task in result.tasks],
            'total': result.total,
            'count': result.count,
        })
        
        return Response(serializer.data)
    
    @extend_schema(
        summary="Create a new task",
        request=TaskCreateSerializer,
        responses={201: TaskSerializer}
    )
    def create(self, request):
        """
        Create a new task with AI analysis.
        
        The AI will automatically:
        - Calculate urgency score (0-1)
        - Assign priority level
        - Extract keywords
        """
        # Validate input
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create command
        command = CreateTaskCommand(
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
        )
        
        # Execute use case
        use_case = CreateTaskUseCase(self.repository, self.ai_service)
        result = use_case.execute(command)
        
        # Serialize response
        response_serializer = TaskSerializer(result.__dict__)
        
        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
    
    @extend_schema(
        summary="Get task detail",
        responses={200: TaskSerializer, 404: None}
    )
    def retrieve(self, request, pk=None):
        """Get a single task by ID."""
        try:
            use_case = GetTaskByIdUseCase(self.repository)
            result = use_case.execute(pk)
            
            serializer = TaskSerializer(result.__dict__)
            return Response(serializer.data)
            
        except TaskNotFoundException:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Update a task",
        request=TaskUpdateSerializer,
        responses={200: TaskSerializer, 404: None}
    )
    def partial_update(self, request, pk=None):
        """
        Update a task (partial update).
        
        Only provided fields will be updated.
        """
        # Validate input
        serializer = TaskUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create command
        command = UpdateTaskCommand(
            task_id=pk,
            **serializer.validated_data
        )
        
        try:
            # Execute use case
            use_case = UpdateTaskUseCase(self.repository)
            result = use_case.execute(command)
            
            # Serialize response
            response_serializer = TaskSerializer(result.__dict__)
            return Response(response_serializer.data)
            
        except TaskNotFoundException:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Delete a task",
        responses={204: None, 404: None}
    )
    def destroy(self, request, pk=None):
        """Delete a task."""
        use_case = DeleteTaskUseCase(self.repository)
        result = use_case.execute(pk)
        
        if result.success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'error': 'Task not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Get tasks prioritized by AI",
        responses={200: TaskListResponseSerializer}
    )
    @action(detail=False, methods=['get'])
    def prioritized(self, request):
        """
        Get tasks sorted by AI urgency score.
        
        Tasks with higher urgency_score appear first.
        This is the AI-powered smart prioritization feature.
        """
        # Execute use case
        use_case = PrioritizeTasksUseCase(self.repository)
        result = use_case.execute(include_completed=False)
        
        # Serialize response
        serializer = TaskListResponseSerializer({
            'tasks': [task.__dict__ for task in result.tasks],
            'total': result.total,
            'count': len(result.tasks),
        })
        
        return Response(serializer.data)
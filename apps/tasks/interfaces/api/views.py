"""
ViewSets de la API.

Manejan peticiones HTTP y delegan a los Casos de Uso.
"""

from uuid import UUID
from dataclasses import asdict
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
import logging

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
from apps.tasks.infrastructure.ai import HuggingFaceEngine
from apps.tasks.domain import TaskNotFoundException

from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskListResponseSerializer,
)

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ViewSet):
    """
    ViewSet para operaciones CRUD de tareas.

    Endpoints:
    - GET    /api/tasks/              - Listar tareas
    - POST   /api/tasks/              - Crear tarea
    - GET    /api/tasks/{id}/         - Detalle de tarea
    - PATCH  /api/tasks/{id}/         - Actualizar tarea
    - DELETE /api/tasks/{id}/         - Eliminar tarea
    - GET    /api/tasks/prioritized/  - Tareas priorizadas por IA
    """

    def get_repository(self):
        """Obtiene repositorio (cached)."""
        if not hasattr(self, '_repository'):
            self._repository = DjangoTaskRepository()
        return self._repository

    def get_ai_service(self):
        """Obtiene servicio de IA (singleton, modelos pre-cargados)."""
        if not hasattr(self, '_ai_service'):
            self._ai_service = HuggingFaceEngine()
        return self._ai_service

    def _validate_uuid(self, pk: str) -> UUID:
        """Valida y convierte string a UUID."""
        try:
            return UUID(pk)
        except (ValueError, TypeError):
            raise ValueError("Formato de UUID inválido")

    def _serialize_task(self, task_response):
        """Serializa TaskResponse a JSON."""
        return TaskSerializer(asdict(task_response)).data

    def _serialize_task_list(self, list_response):
        """Serializa TaskListResponse a JSON."""
        return TaskListResponseSerializer({
            'tasks': [asdict(task) for task in list_response.tasks],
            'total': list_response.total,
            'limit': list_response.limit,
            'offset': list_response.offset,
        }).data

    @extend_schema(
        summary="Listar tareas",
        parameters=[
            OpenApiParameter(name='status', description='Filtrar por estado'),
            OpenApiParameter(name='priority', description='Filtrar por prioridad'),
            OpenApiParameter(name='urgent_only', description='Solo urgentes', type=bool),
        ],
        responses={200: TaskListResponseSerializer}
    )
    def list(self, request):
        """Lista tareas con filtros opcionales."""
        command = GetTasksCommand(
            status=request.query_params.get('status'),
            priority=request.query_params.get('priority'),
            urgent_only=request.query_params.get('urgent_only', 'false').lower() == 'true',
        )

        use_case = GetTasksUseCase(self.get_repository())
        result = use_case.execute(command)

        return Response(self._serialize_task_list(result))

    @extend_schema(
        summary="Crear tarea",
        request=TaskCreateSerializer,
        responses={201: TaskSerializer}
    )
    def create(self, request):
        """Crea una nueva tarea con análisis de IA automático."""
        serializer = TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = CreateTaskCommand(
            title=serializer.validated_data['title'],
            description=serializer.validated_data.get('description', ''),
        )

        try:
            use_case = CreateTaskUseCase(self.get_repository(), self.get_ai_service())
            result = use_case.execute(command)

            return Response(
                self._serialize_task(result),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.error(f"Error creando tarea: {e}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Obtener detalle de tarea",
        responses={200: TaskSerializer, 404: None}
    )
    def retrieve(self, request, pk=None):
        """Obtiene una tarea por ID."""
        try:
            task_id = self._validate_uuid(pk)
            use_case = GetTaskByIdUseCase(self.get_repository())
            result = use_case.execute(task_id)

            return Response(self._serialize_task(result))

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except TaskNotFoundException:
            return Response({'error': 'Tarea no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Actualizar tarea",
        request=TaskUpdateSerializer,
        responses={200: TaskSerializer, 404: None}
    )
    def partial_update(self, request, pk=None):
        """Actualiza una tarea (actualización parcial)."""
        try:
            task_id = self._validate_uuid(pk)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        command = UpdateTaskCommand(
            task_id=task_id,
            **serializer.validated_data
        )

        try:
            use_case = UpdateTaskUseCase(self.get_repository())
            result = use_case.execute(command)

            return Response(self._serialize_task(result))

        except TaskNotFoundException:
            return Response({'error': 'Tarea no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Eliminar tarea",
        responses={204: None, 404: None}
    )
    def destroy(self, request, pk=None):
        """Elimina una tarea."""
        try:
            task_id = self._validate_uuid(pk)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        use_case = DeleteTaskUseCase(self.get_repository())
        result = use_case.execute(task_id)

        if result.success:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Tarea no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        summary="Tareas priorizadas por IA",
        responses={200: TaskListResponseSerializer}
    )
    @action(detail=False, methods=['get'])
    def prioritized(self, request):
        """Obtiene tareas ordenadas por urgencia (IA)."""
        use_case = PrioritizeTasksUseCase(self.get_repository())
        result = use_case.execute(include_completed=False)

        return Response(self._serialize_task_list(result))
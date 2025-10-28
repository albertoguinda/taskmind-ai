"""
Serializadores de API.

Manejan serialización/deserialización JSON entre HTTP y DTOs.
"""

from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    """Serializer para respuestas de Task (GET)."""
    
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.CharField()
    status = serializers.CharField()
    urgency_score = serializers.FloatField(min_value=0.0, max_value=1.0)
    ai_keywords = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class TaskCreateSerializer(serializers.Serializer):
    """Serializer para crear tareas (POST)."""
    
    title = serializers.CharField(
        max_length=200,
        help_text="Título de la tarea (máx 200 caracteres)"
    )
    description = serializers.CharField(
        allow_blank=True,
        default="",
        help_text="Descripción detallada"
    )
    
    def validate_title(self, value):
        """Valida que el título no esté vacío."""
        if not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value.strip()


class TaskUpdateSerializer(serializers.Serializer):
    """Serializer para actualizar tareas (PATCH). Todos los campos opcionales."""
    
    title = serializers.CharField(
        max_length=200,
        required=False
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True
    )
    priority = serializers.ChoiceField(
        choices=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        required=False
    )
    status = serializers.ChoiceField(
        choices=['TODO', 'IN_PROGRESS', 'DONE', 'CANCELLED'],
        required=False
    )
    
    def validate_title(self, value):
        """Valida título si se proporciona."""
        if value is not None and not value.strip():
            raise serializers.ValidationError("El título no puede estar vacío")
        return value.strip() if value else value


class TaskListResponseSerializer(serializers.Serializer):
    """Serializer para lista paginada de tareas."""
    
    tasks = TaskSerializer(many=True)
    total = serializers.IntegerField()
    limit = serializers.IntegerField(required=False, allow_null=True)
    offset = serializers.IntegerField(default=0)
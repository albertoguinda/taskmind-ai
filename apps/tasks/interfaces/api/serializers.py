"""
API Serializers.

Serializers handle JSON serialization/deserialization.
They convert between HTTP requests/responses and DTOs.
"""

from rest_framework import serializers
from uuid import UUID


class TaskSerializer(serializers.Serializer):
    """
    Serializer for Task output.
    
    This is used for GET responses.
    """
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    priority = serializers.CharField()
    status = serializers.CharField()
    urgency_score = serializers.FloatField()
    ai_keywords = serializers.ListField(child=serializers.CharField())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class TaskCreateSerializer(serializers.Serializer):
    """
    Serializer for creating a task.
    
    This is used for POST requests.
    Only requires title and description.
    """
    title = serializers.CharField(
        max_length=200,
        help_text="Task title (max 200 characters)"
    )
    description = serializers.CharField(
        allow_blank=True,
        default="",
        help_text="Detailed task description"
    )
    
    def validate_title(self, value):
        """Validate title is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value


class TaskUpdateSerializer(serializers.Serializer):
    """
    Serializer for updating a task.
    
    This is used for PATCH requests.
    All fields are optional.
    """
    title = serializers.CharField(
        max_length=200,
        required=False,
        help_text="Task title"
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Task description"
    )
    priority = serializers.ChoiceField(
        choices=['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'],
        required=False,
        help_text="Task priority level"
    )
    status = serializers.ChoiceField(
        choices=['TODO', 'IN_PROGRESS', 'DONE', 'CANCELLED'],
        required=False,
        help_text="Task status"
    )


class AnalysisSerializer(serializers.Serializer):
    """Serializer for AI analysis results."""
    urgency_score = serializers.FloatField()
    keywords = serializers.ListField(child=serializers.CharField())
    confidence = serializers.FloatField()
    sentiment = serializers.FloatField()


class TaskListResponseSerializer(serializers.Serializer):
    """Serializer for paginated task list."""
    tasks = TaskSerializer(many=True)
    total = serializers.IntegerField()
    count = serializers.IntegerField()
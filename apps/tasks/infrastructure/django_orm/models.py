"""
Django ORM Models for Task.

Maps domain entities to database tables.
This is infrastructure layer - depends on Django.
"""

import uuid
from django.db import models

from apps.tasks.domain import Priority, Status


class TaskModel(models.Model):
    """
    Django ORM model for Task persistence.
    
    This is the infrastructure implementation - it depends on Django.
    The domain layer doesn't know this exists (Dependency Inversion).
    """
    
    # Primary Key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    
    # Basic fields
    title = models.CharField(
        max_length=200,
        help_text="Task title",
    )
    
    description = models.TextField(
        blank=True,
        default="",
        help_text="Detailed task description",
    )
    
    # Enums stored as strings
    priority = models.CharField(
        max_length=20,
        choices=[(p.value, p.value) for p in Priority],
        default=Priority.MEDIUM.value,
        help_text="Task priority level",
    )
    
    status = models.CharField(
        max_length=20,
        choices=[(s.value, s.value) for s in Status],
        default=Status.TODO.value,
        help_text="Current task status",
    )
    
    # AI-generated fields
    urgency_score = models.FloatField(
        default=0.5,
        help_text="AI-calculated urgency score (0-1)",
    )
    
    ai_keywords = models.JSONField(
        default=list,
        blank=True,
        help_text="Keywords extracted by AI",
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the task was created",
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the task was last updated",
    )
    
    class Meta:
        db_table = 'tasks'
        ordering = ['-urgency_score', '-created_at']
        indexes = [
            models.Index(fields=['-urgency_score'], name='idx_urgency'),
            models.Index(fields=['priority'], name='idx_priority'),
            models.Index(fields=['status'], name='idx_status'),
            models.Index(fields=['-created_at'], name='idx_created'),
        ]
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return f"{self.title} ({self.priority})"
    
    def __repr__(self):
        return f"<TaskModel: {self.title} [{self.status}]>"
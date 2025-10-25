"""
Django ORM Infrastructure.

Implements domain repositories using Django ORM.
"""

from .models import TaskModel
from .repository import DjangoTaskRepository

__all__ = ["TaskModel", "DjangoTaskRepository"]
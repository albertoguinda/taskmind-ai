"""
Django models for tasks app.

This module follows Django's convention of having models in <app>/models.py.
However, to maintain Clean Architecture, the actual models are defined in
the infrastructure layer and imported here.

This is a bridge between Django conventions and Clean Architecture.
"""

# Import from infrastructure layer
from apps.tasks.infrastructure.django_orm.models import TaskModel

# Export for Django
__all__ = ['TaskModel']

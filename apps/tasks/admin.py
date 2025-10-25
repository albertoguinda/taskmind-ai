"""
Django admin configuration for tasks app.

This module follows Django's convention of having admin in <app>/admin.py.
The actual admin configuration is in the infrastructure layer.
"""

# Import and register from infrastructure layer
from apps.tasks.infrastructure.django_orm.admin import *  # noqa

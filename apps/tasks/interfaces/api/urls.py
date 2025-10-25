"""
API URL Configuration.

Maps URLs to ViewSets.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet

# Create router
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
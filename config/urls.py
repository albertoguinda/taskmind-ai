"""
Main URL Configuration.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request):
    """API root endpoint."""
    return Response({
        'message': 'TaskMind AI API',
        'version': '0.1.0',
        'endpoints': {
            'tasks': request.build_absolute_uri('/api/tasks/'),
            'prioritized': request.build_absolute_uri('/api/tasks/prioritized/'),
            'docs': request.build_absolute_uri('/api/schema/swagger-ui/'),
            'admin': request.build_absolute_uri('/admin/'),
        }
    })


urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # API Root
    path('api/', api_root, name='api-root'),
    
    # Tasks API
    path('api/', include('apps.tasks.interfaces.api.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
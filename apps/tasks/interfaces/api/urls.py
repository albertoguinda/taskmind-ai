"""
API URL Configuration for Tasks app.
Will be populated in Phase 4.
"""

from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request):
    """Temporary API root endpoint"""
    return Response({
        'message': 'TaskMind AI API',
        'version': '0.1.0',
        'status': 'under development',
    })


urlpatterns = [
    path('', api_root, name='api-root'),
]
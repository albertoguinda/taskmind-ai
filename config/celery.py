"""
Celery configuration for TaskMind AI.
"""

import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Create Celery app
app = Celery('taskmind')

# Load config from Django settings (namespace='CELERY')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    """Debug task for testing Celery"""
    print(f'Request: {self.request!r}')
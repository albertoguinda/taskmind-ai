"""
Django test settings for TaskMind AI.
"""

from .base import *

# Use in-memory SQLite for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for tests (faster)
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Password hashers: Use fast hasher for tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Celery: Execute tasks synchronously in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Email: Use memory backend
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Disable logging in tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}

# Cache: Use dummy cache for tests
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
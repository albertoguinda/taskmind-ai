"""
Django production settings for TaskMind AI.
"""

from .base import *

# SECURITY
DEBUG = False

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Production-only apps
INSTALLED_APPS += [
    'gunicorn',
]

# Logging: Use file logging in production
LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': BASE_DIR / 'logs' / 'django.log',
    'formatter': 'verbose',
}
LOGGING['loggers']['django']['handlers'] = ['console', 'file']
LOGGING['loggers']['apps']['handlers'] = ['console', 'file']

# Static files: Use WhiteNoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
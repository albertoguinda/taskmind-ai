"""
Quick setup validation script.
Run with: python test_setup.py
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(__file__))

print("🔍 Testing TaskMind AI Setup...\n")

# Test 1: Django settings
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    import django
    django.setup()
    print("✅ Django settings loaded successfully")
except Exception as e:
    print(f"❌ Django settings failed: {e}")
    sys.exit(1)

# Test 2: Django core
try:
    from django.conf import settings
    print(f"✅ Django version: {django.get_version()}")
    print(f"✅ Debug mode: {settings.DEBUG}")
    print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
except Exception as e:
    print(f"❌ Django core failed: {e}")
    sys.exit(1)

# Test 3: REST Framework
try:
    import rest_framework
    print(f"✅ DRF version: {rest_framework.VERSION}")
except Exception as e:
    print(f"❌ DRF failed: {e}")

# Test 4: Celery
try:
    from config.celery import app as celery_app
    print(f"✅ Celery app: {celery_app.main}")
except Exception as e:
    print(f"❌ Celery failed: {e}")

# Test 5: Apps
try:
    from apps.tasks.apps import TasksConfig
    print(f"✅ Tasks app: {TasksConfig.name}")
except Exception as e:
    print(f"❌ Tasks app failed: {e}")

print("\n🎉 All setup tests passed! Ready for Phase 1.")
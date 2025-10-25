"""
Django management command to test Use Cases integration.

Run with: python manage.py test_integration
"""

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.tasks.application import (
    CreateTaskUseCase,
    CreateTaskCommand,
    GetTasksUseCase,
    GetTasksCommand,
    PrioritizeTasksUseCase,
)
from apps.tasks.infrastructure.django_orm import DjangoTaskRepository
from apps.tasks.infrastructure.ai import HuggingFaceEngine  # ← CAMBIADO


class Command(BaseCommand):
    help = 'Test Application Layer integration with Real AI'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n🧪 Testing Application Layer with HuggingFace AI\n'))
        
        # Setup
        repo = DjangoTaskRepository()
        ai = HuggingFaceEngine()  # ← CAMBIADO
        
        with transaction.atomic():
            # Test 1: Create Task
            self.stdout.write('1️⃣ Testing CreateTaskUseCase with Real AI...')
            create_use_case = CreateTaskUseCase(repo, ai)
            
            command = CreateTaskCommand(
                title='URGENT: Production server down!',
                description='Critical bug affecting all users. Need immediate fix.'
            )
            
            response = create_use_case.execute(command)
            
            self.stdout.write(self.style.SUCCESS(f'   ✅ Task created: {response.title}'))
            self.stdout.write(f'   📊 Urgency: {response.urgency_score}')
            self.stdout.write(f'   🎯 Priority: {response.priority}')
            self.stdout.write(f'   🔑 Keywords: {response.ai_keywords}\n')
            
            # Test 2: Get Tasks
            self.stdout.write('2️⃣ Testing GetTasksUseCase...')
            get_use_case = GetTasksUseCase(repo)
            
            get_command = GetTasksCommand()
            list_response = get_use_case.execute(get_command)
            
            self.stdout.write(self.style.SUCCESS(f'   ✅ Found {list_response.total} tasks\n'))
            
            # Test 3: Prioritize Tasks
            self.stdout.write('3️⃣ Testing PrioritizeTasksUseCase...')
            prioritize_use_case = PrioritizeTasksUseCase(repo)
            
            prioritized = prioritize_use_case.execute()
            
            self.stdout.write(self.style.SUCCESS(f'   ✅ Prioritized {len(prioritized.tasks)} tasks'))
            
            if prioritized.tasks:
                top_task = prioritized.tasks[0]
                self.stdout.write(f'   🥇 Top priority: {top_task.title}')
                self.stdout.write(f'      Urgency: {top_task.urgency_score}\n')
            
            # Rollback (para no llenar la DB)
            self.stdout.write(self.style.WARNING('🔄 Rolling back test data...\n'))
            transaction.set_rollback(True)
        
        self.stdout.write(self.style.SUCCESS('✅ All tests passed with Real AI!\n'))
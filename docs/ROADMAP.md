# TaskMind AI - Development Roadmap

## 🎯 Mission

Build production-quality Django app with AI in 1 weekend to demonstrate senior-level capabilities.

## 📅 Timeline: Weekend Sprint

### **Phase 0: Setup** (Friday Night, 2-3h)

**Goal:** Environment ready, foundation solid

**Tasks:**

- [ ] Create GitHub repository
- [ ] Initialize project structure
- [ ] Setup Docker Compose (PostgreSQL + Redis + RabbitMQ)
- [ ] Configure Django settings (base/dev/prod)
- [ ] Setup pre-commit hooks (black, flake8, mypy)
- [ ] Create all documentation files
- [ ] First commit: "Initial project structure"

**Deliverables:**

- ✅ `docker-compose up` works
- ✅ Django admin accessible
- ✅ All docs in `/docs` folder

**Validation:**

````bash
docker-compose up -d
docker-compose exec web python manage.py check
docker-compose exec web python manage.py test

---

### **Phase 1: Domain Layer** (Saturday Morning, 3-4h)
**Goal:** Core business logic, framework-agnostic

**Tasks:**
- [ ] **Entities:** `Task`, `Analysis`
- [ ] **Value Objects:** `Priority`, `Status`, `UrgencyScore`
- [ ] **Repository Interfaces:** `TaskRepository`, `AIEnginePort`
- [ ] **Domain Services:** `TaskService`, `PriorityCalculator`
- [ ] **Domain Exceptions:** `TaskNotFoundError`, `InvalidPriorityError`
- [ ] **Unit Tests:** 100% coverage on domain

**File Structure:**apps/tasks/domain/
├── entities/
│   ├── task.py              # Task(title, description, priority)
│   └── analysis.py          # Analysis(urgency_score, keywords)
├── value_objects/
│   ├── priority.py          # Enum: LOW, MEDIUM, HIGH, CRITICAL
│   ├── status.py            # Enum: TODO, IN_PROGRESS, DONE
│   └── urgency_score.py     # Float 0-1 with validation
├── repositories/
│   └── task_repository.py   # ABC with abstract methods
├── services/
│   └── task_service.py      # Business rules
└── exceptions.py            # Domain-specific errors

**Key Code Example:**
```pythonapps/tasks/domain/entities/task.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4
from ..value_objects import Priority, Status@dataclass
class Task:
"""Core Task entity - framework agnostic"""
title: str
description: str
priority: Priority = Priority.MEDIUM
status: Status = Status.TODO
id: UUID = None
urgency_score: float = 0.5
ai_keywords: list[str] = None
created_at: datetime = None
updated_at: datetime = Nonedef __post_init__(self):
    if self.id is None:
        self.id = uuid4()
    if self.ai_keywords is None:
        self.ai_keywords = []
    if self.created_at is None:
        self.created_at = datetime.utcnow()
    self.updated_at = datetime.utcnow()def mark_as_high_priority(self):
    """Business rule: High urgency = HIGH priority"""
    if self.urgency_score >= 0.8:
        self.priority = Priority.HIGHdef is_urgent(self) -> bool:
    return self.urgency_score > 0.7

**Tests Example:**
```pythontests/unit/domain/test_task_entity.py
def test_task_creation():
task = Task(title="Test", description="Desc")
assert task.id is not None
assert task.priority == Priority.MEDIUMdef test_high_urgency_sets_priority():
task = Task(title="Urgent", description="Server down")
task.urgency_score = 0.9
task.mark_as_high_priority()
assert task.priority == Priority.HIGH

**Deliverables:**
- ✅ Domain layer complete
- ✅ Zero Django dependencies in domain/
- ✅ All tests green

---

### **Phase 2: Infrastructure Layer** (Saturday Afternoon, 3-4h)
**Goal:** Connect domain to Django and external services

**Tasks:**
- [ ] Django models (map entities to ORM)
- [ ] Repository implementations (DjangoORMRepository)
- [ ] Hugging Face AI engine setup
- [ ] Celery tasks configuration
- [ ] Redis caching layer
- [ ] Database migrations

**File Structure:**apps/tasks/infrastructure/
├── django_orm/
│   ├── models.py                    # Django ORM models
│   ├── repository.py                # DjangoTaskRepository
│   └── migrations/
├── ai/
│   ├── huggingface_engine.py       # AI implementation
│   ├── model_loader.py             # Singleton for models
│   └── prompts.py                  # Prompt templates
└── cache/
└── redis_cache.py              # Caching logic

**Key Code Example:**
```pythonapps/tasks/infrastructure/django_orm/models.py
from django.db import models
import uuidclass TaskModel(models.Model):
"""Django ORM model - infrastructure detail"""
id = models.UUIDField(primary_key=True, default=uuid.uuid4)
title = models.CharField(max_length=200)
description = models.TextField(blank=True)
priority = models.CharField(
max_length=20,
choices=[
('LOW', 'Low'),
('MEDIUM', 'Medium'),
('HIGH', 'High'),
('CRITICAL', 'Critical'),
],
default='MEDIUM'
)
status = models.CharField(max_length=20, default='TODO')
urgency_score = models.FloatField(default=0.5)
ai_keywords = models.JSONField(default=list)
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)class Meta:
    db_table = 'tasks'
    ordering = ['-urgency_score', '-created_at']
    indexes = [
        models.Index(fields=['-urgency_score']),
        models.Index(fields=['priority']),
    ]def to_domain(self) -> Task:
    """Convert ORM model to domain entity"""
    return Task(
        id=self.id,
        title=self.title,
        description=self.description,
        priority=Priority[self.priority],
        status=Status[self.status],
        urgency_score=self.urgency_score,
        ai_keywords=self.ai_keywords,
        created_at=self.created_at,
        updated_at=self.updated_at,
    )
```pythonapps/tasks/infrastructure/ai/huggingface_engine.py
from transformers import pipeline
from ...domain.repositories import AIEnginePort
from ...domain.entities import Analysisclass HuggingFaceEngine(AIEnginePort):
"""AI implementation using Hugging Face"""def __init__(self):
    # Load models once at startup
    self.classifier = pipeline(
        "zero-shot-classification",
        model="facebook/bart-large-mnli"
    )
    self.sentiment = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )def analyze_urgency(self, text: str) -> Analysis:
    """Analyze text and return urgency score"""
    # Zero-shot classification
    candidate_labels = ["urgent", "normal", "low priority", "critical"]
    result = self.classifier(text, candidate_labels)    # Sentiment analysis
    sentiment = self.sentiment(text)[0]    # Calculate urgency score (0-1)
    urgency_map = {"urgent": 0.9, "critical": 1.0, "normal": 0.5, "low priority": 0.2}
    urgency_score = urgency_map.get(result['labels'][0], 0.5)    # Extract keywords (simple version)
    keywords = self._extract_keywords(text)    return Analysis(
        urgency_score=urgency_score,
        keywords=keywords,
        confidence=result['scores'][0]
    )def _extract_keywords(self, text: str) -> list[str]:
    # Simplified: split and filter
    words = text.lower().split()
    important_words = ["bug", "error", "urgent", "critical", "production", "down"]
    return [w for w in words if w in important_words]

**Deliverables:**
- ✅ Django models created
- ✅ Migrations applied
- ✅ AI engine working (test with sample text)
- ✅ Celery tasks running

**Validation:**
```bashpython manage.py makemigrations
python manage.py migrate
python manage.py shell



from apps.tasks.infrastructure.ai import HuggingFaceEngine
engine = HuggingFaceEngine()
analysis = engine.analyze_urgency("URGENT: Production server is down!")
print(analysis.urgency_score)  # Should be > 0.8




---

### **Phase 3: Application Layer** (Saturday Evening, 2-3h)
**Goal:** Use cases that orchestrate domain and infrastructure

**Tasks:**
- [ ] **Use Cases:** CreateTask, GetTasks, UpdateTask, DeleteTask, PrioritizeTasks
- [ ] Dependency injection setup
- [ ] DTOs (Data Transfer Objects)
- [ ] Use case tests with mocks

**File Structure:**apps/tasks/application/
├── use_cases/
│   ├── create_task.py           # CreateTaskUseCase
│   ├── get_tasks.py             # GetTasksUseCase
│   ├── prioritize_tasks.py      # PrioritizeTasksUseCase (with AI)
│   └── update_task.py           # UpdateTaskUseCase
├── dtos/
│   ├── task_dto.py              # Input/Output DTOs
│   └── analysis_dto.py
└── ports/
└── ai_service.py            # Abstract AI port

**Key Code Example:**
```pythonapps/tasks/application/use_cases/create_task.py
from dataclasses import dataclass
from ...domain.entities import Task
from ...domain.repositories import TaskRepository
from ...domain.services import TaskService
from ..ports import AIService@dataclass
class CreateTaskCommand:
"""Input DTO"""
title: str
description: strclass CreateTaskUseCase:
"""Use case: Create task with AI analysis"""def __init__(
    self,
    task_repository: TaskRepository,
    ai_service: AIService,
    task_service: TaskService
):
    self.task_repository = task_repository
    self.ai_service = ai_service
    self.task_service = task_servicedef execute(self, command: CreateTaskCommand) -> Task:
    # 1. Create domain entity
    task = Task(
        title=command.title,
        description=command.description
    )    # 2. Analyze with AI (could be async in prod)
    analysis = self.ai_service.analyze_urgency(
        f"{task.title} {task.description}"
    )    # 3. Apply analysis to task
    task.urgency_score = analysis.urgency_score
    task.ai_keywords = analysis.keywords    # 4. Apply business rules
    task.mark_as_high_priority()    # 5. Validate with domain service
    self.task_service.validate_task(task)    # 6. Persist
    saved_task = self.task_repository.save(task)    # 7. Fire domain event (future: send notification)
    # event_bus.publish(TaskCreatedEvent(task.id))    return saved_task

**Tests Example:**
```pythontests/unit/application/test_create_task_use_case.py
from unittest.mock import Mock
import pytestdef test_create_task_with_high_urgency():
# Arrange
mock_repo = Mock(spec=TaskRepository)
mock_ai = Mock(spec=AIService)
mock_ai.analyze_urgency.return_value = Analysis(
urgency_score=0.95,
keywords=["urgent", "critical"]
)use_case = CreateTaskUseCase(
    task_repository=mock_repo,
    ai_service=mock_ai,
    task_service=TaskService()
)command = CreateTaskCommand(
    title="Critical bug",
    description="Production is down"
)# Act
task = use_case.execute(command)# Assert
assert task.urgency_score == 0.95
assert task.priority == Priority.HIGH
assert "urgent" in task.ai_keywords
mock_repo.save.assert_called_once()

**Deliverables:**
- ✅ All use cases implemented
- ✅ 100% unit test coverage (with mocks)
- ✅ No Django dependencies

---

### **Phase 4: Interface Layer** (Sunday Morning, 3-4h)
**Goal:** REST API with Django REST Framework

**Tasks:**
- [ ] DRF serializers
- [ ] ViewSets (API endpoints)
- [ ] URL routing
- [ ] Pagination, filtering, searching
- [ ] API documentation (drf-spectacular)
- [ ] Integration tests

**File Structure:**apps/tasks/interfaces/api/
├── serializers.py           # DRF serializers
├── views.py                 # ViewSets
├── urls.py                  # URL routing
├── filters.py               # Django Filter Backend
├── permissions.py           # (future: JWT auth)
└── pagination.py            # Custom pagination

**Key Code Example:**
```pythonapps/tasks/interfaces/api/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ...application.use_cases import CreateTaskUseCase, PrioritizeTasksUseCase
from .serializers import TaskSerializer, TaskCreateSerializerclass TaskViewSet(viewsets.ModelViewSet):
"""
API endpoints for Task managementlist: GET /api/tasks/
create: POST /api/tasks/
retrieve: GET /api/tasks/{id}/
update: PATCH /api/tasks/{id}/
destroy: DELETE /api/tasks/{id}/
prioritized: GET /api/tasks/prioritized/  (custom action)
"""queryset = TaskModel.objects.all()
serializer_class = TaskSerializerdef get_serializer_class(self):
    if self.action == 'create':
        return TaskCreateSerializer
    return TaskSerializerdef create(self, request):
    """Create task with AI analysis"""
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)    # Use case (with DI)
    use_case = get_create_task_use_case()
    command = CreateTaskCommand(**serializer.validated_data)    try:
        task = use_case.execute(command)
        output_serializer = TaskSerializer(
            TaskModel.objects.get(id=task.id)
        )
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED
        )
    except DomainException as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )@action(detail=False, methods=['get'])
def prioritized(self, request):
    """Get tasks sorted by AI urgency score"""
    use_case = get_prioritize_tasks_use_case()
    tasks = use_case.execute()    serializer = self.get_serializer(
        [TaskModel.objects.get(id=t.id) for t in tasks],
        many=True
    )
    return Response(serializer.data)

**Deliverables:**
- ✅ Full CRUD API working
- ✅ Custom action for AI prioritization
- ✅ OpenAPI docs at `/api/schema/`
- ✅ Postman collection generated

**Validation:**
```bashTest API endpoints
curl -X POST http://localhost:8000/api/tasks/
-H "Content-Type: application/json"
-d '{"title": "Test task", "description": "Description"}'curl http://localhost:8000/api/tasks/prioritized/

---

### **Phase 5: Celery Integration** (Sunday Afternoon, 2h)
**Goal:** Async processing for AI tasks

**Tasks:**
- [ ] Celery configuration
- [ ] Async tasks (analyze_task_async)
- [ ] Periodic tasks (re-prioritize daily)
- [ ] Task monitoring

**Key Code:**
```pythonapps/tasks/tasks.py (Celery tasks)
from celery import shared_task
from .application.use_cases import AnalyzeTaskUseCase@shared_task(bind=True, max_retries=3)
def analyze_task_async(self, task_id: str):
"""Analyze task urgency asynchronously"""
try:
use_case = get_analyze_task_use_case()
use_case.execute(task_id)
except Exception as exc:
# Retry with exponential backoff
raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))@shared_task
def reprioritize_all_tasks():
"""Periodic task: re-analyze all tasks daily"""
use_case = get_prioritize_tasks_use_case()
use_case.execute()

---

### **Phase 6: Testing & Documentation** (Sunday Evening, 2-3h)
**Goal:** Polish and documentation

**Tasks:**
- [ ] Achieve >80% test coverage
- [ ] Write comprehensive README
- [ ] API documentation
- [ ] Architecture diagrams
- [ ] SOLID examples documented
- [ ] Video demo (optional)

**Deliverables:**
- ✅ All tests passing
- ✅ Coverage report >80%
- ✅ README with quickstart
- ✅ Architecture docs
- ✅ Demo video or GIF

---

## 🎯 Definition of Done

### Per Phase:
- [ ] All code committed with descriptive messages
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Docker builds successfully

### Project Complete:
- [ ] All API endpoints working
- [ ] AI integration functional
- [ ] Celery processing tasks
- [ ] >80% test coverage
- [ ] README impressive
- [ ] Architecture documented
- [ ] SOLID principles demonstrated
- [ ] Can run: `docker-compose up -d` → works immediately

---

## 📊 Progress TrackingPhase 0: Setup              [████████████████████] 100%
Phase 1: Domain             [░░░░░░░░░░░░░░░░░░░░]   0%
Phase 2: Infrastructure     [░░░░░░░░░░░░░░░░░░░░]   0%
Phase 3: Application        [░░░░░░░░░░░░░░░░░░░░]   0%
Phase 4: Interface          [░░░░░░░░░░░░░░░░░░░░]   0%
Phase 5: Celery             [░░░░░░░░░░░░░░░░░░░░]   0%
Phase 6: Polish             [░░░░░░░░░░░░░░░░░░░░]   0%Overall: 14% complete

---

## 🚨 Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Hugging Face models too slow | Medium | High | Pre-load at startup, use DistilBERT (faster) |
| Running out of time | High | Medium | MVP first, bonus features later |
| Docker issues on laptop | Low | High | Test docker-compose FIRST |
| AI analysis not impressive | Medium | Medium | Fallback: rule-based system + AI |

---

## 🎁 Bonus Features (If Time Permits)

**Priority 1 (Nice to have):**
- [ ] Simple React frontend
- [ ] WebSocket for real-time updates
- [ ] Export tasks to CSV/PDF

**Priority 2 (Impressive but optional):**
- [ ] Multi-language support (i18n)
- [ ] Task dependencies (blocked by)
- [ ] AI-generated task suggestions

**Priority 3 (If you're superhuman):**
- [ ] GraphQL endpoint
- [ ] Mobile-responsive UI
- [ ] OAuth2 authentication

---

## 🎤 Demo Script (for interview)

1. **Show architecture diagram** (2 min)
   - "This is Clean Architecture with SOLID principles"

2. **Live API demo** (3 min)
   - Create task via Postman
   - Show AI analysis in response
   - Show prioritized endpoint

3. **Code walkthrough** (5 min)
   - Domain layer (framework-agnostic)
   - Use case with DI
   - Repository pattern

4. **SOLID examples** (3 min)
   - Point to specific code

5. **Testing** (2 min)
   - Run pytest
   - Show coverage report

Total: 15 minutes, leaves 15 for questions

---

## 📝 Commit Message Conventionfeat: Add CreateTaskUseCase with AI analysis
fix: Resolve N+1 query in task list endpoint
docs: Add SOLID principles examples to ARCHITECTURE.md
test: Add unit tests for domain entities
refactor: Extract AI logic to separate service
chore: Update dependencies

Follow [Conventional Commits](https://www.conventionalcommits.org/)
````

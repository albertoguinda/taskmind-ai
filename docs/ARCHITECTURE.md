# TaskMind AI - Software Architecture

## Architecture Decision Records (ADRs)

### ADR-001: Monolito modular con Clean Architecture

**Contexto:** Proyecto demo que debe demostrar capacidad arquitectónica
**Decisión:** Clean Architecture + DDD light
**Consecuencias:** Mayor complejidad inicial, mejor mantenibilidad
**Alternativas rechazadas:** Django vanilla, microservicios

### ADR-002: Hugging Face para IA (no OpenAI)

**Contexto:** Necesitamos IA gratis y rápida
**Decisión:** Transformers con modelos pre-entrenados
**Consecuencias:** Más control, sin costos, latencia aceptable
**Alternativas rechazadas:** OpenAI GPT (de pago), RAG local (lento)

### ADR-003: Celery + RabbitMQ para async

**Contexto:** Análisis IA tarda 2-4 segundos
**Decisión:** Queue asíncrona con Celery
**Consecuencias:** Mejor UX, complejidad operativa
**Alternativas rechazadas:** Django Channels, procesamiento síncrono

## Architectural Layers

┌───────────────────────────────────────┐
│ INTERFACE LAYER │
│ (API REST, Admin, CLI Commands) │
│ │
│ - Django REST Framework Views │
│ - URL Routing │
│ - Serializers (I/O validation) │
└───────────────┬───────────────────────┘
│
┌───────────────▼───────────────────────┐
│ APPLICATION LAYER │
│ (Use Cases / Orchestration) │
│ │
│ - CreateTaskUseCase │
│ - PrioritizeTasksUseCase │
│ - AnalyzeContextUseCase │
│ - Pure Python (no Django) │
└───────────────┬───────────────────────┘
│
┌───────────────▼───────────────────────┐
│ DOMAIN LAYER │
│ (Business Logic / Entities) │
│ │
│ - Task (Entity) │
│ - Priority (Value Object) │
│ - TaskService (Domain Service) │
│ - Repository Interfaces │
│ - 100% framework-agnostic │
└───────────────┬───────────────────────┘
│
┌───────────────▼───────────────────────┐
│ INFRASTRUCTURE LAYER │
│ (External Dependencies / Adapters) │
│ │
│ - Django ORM (Persistence) │
│ - Hugging Face (AI Engine) │
│ - Redis (Caching) │
│ - RabbitMQ (Messaging) │
└───────────────────────────────────────┘

## Component Diagram

┌─────────────────────────────────────────────────────┐
│ Client (REST) │
└────────────────────────┬────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────┐
│ TaskViewSet (DRF) │
│ POST /tasks/ GET /tasks/ PATCH /tasks/{id}/ │
└────────────────────────┬────────────────────────────┘
│
┌─────────────┴─────────────┐
▼ ▼
┌──────────────────────┐ ┌──────────────────────┐
│ CreateTaskUseCase │ │ PrioritizeUseCase │
│ │ │ │
│ 1. Validate │ │ 1. Get tasks │
│ 2. Analyze with AI │────┤ 2. Batch analyze │
│ 3. Save to DB │ │ 3. Sort by score │
└──────────────────────┘ └──────────────────────┘
│ │
▼ ▼
┌──────────────────────┐ ┌──────────────────────┐
│ TaskRepository │ │ AIService │
│ (Interface) │ │ (Interface) │
└──────────────────────┘ └──────────────────────┘
│ │
▼ ▼
┌──────────────────────┐ ┌──────────────────────┐
│ DjangoORMRepo │ │ HuggingFaceEngine │
│ (Implementation) │ │ (Implementation) │
└──────────────────────┘ └──────────────────────┘
│ │
▼ ▼
[PostgreSQL] [Transformers]

## Data Flow: Create Task with AI Priority

POST /api/tasks/ {"title": "Fix prod bug", "description": "Server down"}
TaskViewSet validates input
CreateTaskUseCase.execute()
AIService.analyze_urgency("Server down") → Priority.CRITICAL
Task entity created with priority
TaskRepository.save(task)
Celery task queued: notify_team(task.id)
Return 201 Created
[Async] Celery worker processes notification

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)

````python✅ Each class has ONE reason to changeclass Task:
"""Entity: Only domain logic"""
passclass TaskRepository:
"""Persistence: Only DB operations"""
passclass TaskSerializer:
"""I/O: Only serialization"""
passclass AIService:
"""Analysis: Only AI logic"""
pass

### Open/Closed Principle (OCP)
```python✅ Open for extension, closed for modificationclass AIEngine(ABC):
@abstractmethod
def analyze(self, text: str) -> Analysis:
passAdd new implementation WITHOUT modifying existing code
class HuggingFaceEngine(AIEngine): ...
class OpenAIEngine(AIEngine): ...
class ClaudeEngine(AIEngine): ...

### Liskov Substitution Principle (LSP)
```python✅ Subtypes must be substitutabledef process_task(repo: TaskRepository):  # Abstract
task = repo.find_by_id(1)Works with ANY implementation:
process_task(DjangoORMRepository())
process_task(MongoDBRepository())
process_task(InMemoryRepository())  # for testing

### Interface Segregation Principle (ISP)
```python✅ Clients shouldn't depend on interfaces they don't useclass Readable(Protocol):
def find_by_id(self, id: int) -> Task: ...class Writable(Protocol):
def save(self, task: Task) -> Task: ...class Searchable(Protocol):
def search(self, query: str) -> List[Task]: ...Use only what you need
class ReadOnlyTaskService:
def init(self, repo: Readable):  # Not full repository
self.repo = repo

### Dependency Inversion Principle (DIP)
```python✅ Depend on abstractions, not concretions❌ BAD: High-level depends on low-level
class TaskService:
def init(self):
self.repo = DjangoTaskRepository()  # Concrete!✅ GOOD: Both depend on abstraction
class TaskService:
def init(self, repo: TaskRepository):  # Abstract!
self.repo = repoDependency Injection
service = TaskService(repo=DjangoTaskRepository())

## Testing StrategyUnit Tests (70%)
├── Domain layer: Pure Python, no DB
├── Use cases: Mocked dependencies
└── Services: Isolated logicIntegration Tests (20%)
├── API endpoints: Real DB (test DB)
├── Repository: Real PostgreSQL
└── Full flow: Request → ResponseE2E Tests (10%)
└── Critical paths only

## Performance Targets

- API response: <100ms (without AI)
- AI analysis: <3s (acceptable for async)
- Database queries: N+1 eliminated
- Redis cache hit rate: >80%
````

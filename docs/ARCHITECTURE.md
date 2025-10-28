# 🏗️ Arquitectura - TaskMind AI

## 🎯 Decisiones Clave

| Decisión                     | Razón                                | Alternativa Rechazada  |
| ---------------------------- | ------------------------------------ | ---------------------- |
| **Clean Architecture**       | Mantenibilidad y testabilidad        | Django vanilla         |
| **Hugging Face (no OpenAI)** | Gratis, sin API calls, control total | OpenAI GPT (de pago)   |
| **Celery + RabbitMQ**        | Análisis IA asíncrono (~2s)          | Procesamiento síncrono |

---

## 📐 Capas (Clean Architecture)

```
┌─────────────────────────────────────┐
│   INTERFACES (API REST)             │  Django REST Framework
│   • ViewSets  • Serializers         │
├─────────────────────────────────────┤
│   APPLICATION (Use Cases)           │  Pure Python
│   • CreateTask  • PrioritizeTasks   │
├─────────────────────────────────────┤
│   DOMAIN (Business Logic)           │  Framework-agnostic
│   • Task  • Priority  • Status      │
├─────────────────────────────────────┤
│   INFRASTRUCTURE (External)         │  Adapters
│   • Django ORM  • Hugging Face AI   │
└─────────────────────────────────────┘
```

**Regla:** Las capas internas NO conocen las externas (Dependency Inversion).

---

## 🔄 Flujo: Crear Tarea con IA

```
1. POST /api/tasks/ {"title": "Fix bug", "description": "Server down"}
2. TaskViewSet valida input
3. CreateTaskUseCase.execute()
4. AIService.analyze("Server down") → urgency: 0.95
5. Task.priority = CRITICAL (auto-calculado)
6. TaskRepository.save(task) → PostgreSQL
7. Celery.notify_team.delay() [async]
8. Return 201 Created
```

---

## 🎨 SOLID Principles

### Single Responsibility

```python
✅ Cada clase = 1 responsabilidad
Task        → Lógica de dominio
Repository  → Persistencia
Serializer  → Validación I/O
```

### Dependency Inversion

```python
✅ Depender de abstracciones
class CreateTaskUseCase:
    def __init__(self, repo: TaskRepository):  # Abstracción
        self.repo = repo

# Inyección de dependencia
use_case = CreateTaskUseCase(repo=DjangoTaskRepository())
```

### Open/Closed

```python
✅ Extender sin modificar código existente
class AIEngine(ABC):
    @abstractmethod
    def analyze(self, text: str): ...

# Nuevas implementaciones sin tocar código viejo
class HuggingFaceEngine(AIEngine): ...
class OpenAIEngine(AIEngine): ...
```

---

## 🧪 Estrategia de Testing

| Tipo            | %   | Qué Testear                       |
| --------------- | --- | --------------------------------- |
| **Unit**        | 70% | Domain (pure Python, sin DB)      |
| **Integration** | 20% | API + Repository (con DB de test) |
| **E2E**         | 10% | Flujos críticos completos         |

---

## 📊 Performance

| Métrica               | Target | Actual                               |
| --------------------- | ------ | ------------------------------------ |
| API sin IA            | <100ms | 50-80ms                              |
| Análisis IA           | <3s    | 250-500ms (después de carga inicial) |
| Carga inicial modelos | -      | ~30s (solo una vez)                  |
| Cache hit rate        | >80%   | TBD                                  |

**Optimizaciones aplicadas:**

- ✅ Singleton pattern para modelos IA
- ✅ Database indexing
- ✅ Redis caching
- ✅ N+1 queries eliminadas

---

## 🔗 Dependencias Principales

```python
# IA & ML
transformers==4.35.2    # Hugging Face
torch==2.1.1            # PyTorch
BART-large (1.6GB)      # Clasificación urgencia
DistilBERT (250MB)      # Sentimiento
BERT-NER (400MB)        # Keywords

# Backend
Django==4.2.7
djangorestframework==3.14.0
PostgreSQL 15

# Async
Celery==5.3.4
RabbitMQ 3.12
Redis 7
```

---

## 📝 Notas Técnicas

### ¿Por qué Clean Architecture?

- ✅ Testeable sin framework
- ✅ Independiente de UI/DB/AI
- ✅ Lógica de negocio clara

### ¿Por qué Hugging Face?

- ✅ Gratis y open source
- ✅ Control total sobre modelos
- ✅ Sin límites de API
- ❌ Requiere más RAM (~2.5GB)

### ¿Por qué Celery?

- ✅ Análisis IA no bloquea requests
- ✅ Escalable (workers paralelos)
- ❌ Mayor complejidad operativa

# 🧠 TaskMind AI

> Sistema inteligente de gestión de tareas con priorización automática mediante IA

[![CI Pipeline](https://github.com/albertoguinda/taskmind-ai/workflows/CI/badge.svg)](https://github.com/albertoguinda/taskmind-ai/actions)
[![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)](https://codecov.io/gh/albertoguinda/taskmind-ai)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Características Principales](#-características-principales)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Inicio Rápido](#-inicio-rápido)
- [Uso de la API](#-uso-de-la-api)
- [Testing](#-testing)
- [Documentación](#-documentación)
- [Por Qué Este Proyecto](#-por-qué-este-proyecto)
- [Autor](#-autor)

---

## 🎯 Acerca del Proyecto

**TaskMind AI** es un sistema de gestión de tareas empresariales que utiliza **Inteligencia Artificial** para analizar automáticamente la urgencia y prioridad de cada tarea basándose en su contenido textual.

### El Problema

Los equipos pierden hasta el **40% del tiempo** decidiendo qué tarea hacer a continuación cuando tienen decenas o cientos de tareas sin priorizar.

### La Solución

TaskMind analiza el texto de cada tarea con **modelos de NLP** (Procesamiento de Lenguaje Natural) y asigna automáticamente:

- **Urgency Score** (0-1): Qué tan urgente es la tarea
- **Priority Level**: LOW, MEDIUM, HIGH o CRITICAL
- **AI Keywords**: Términos clave extraídos del contexto

**De 100 tareas sin priorizar a un roadmap claro en 3 segundos.**

---

## ✨ Características Principales

### 🤖 **IA Aplicada (No Teoría)**

- Análisis de urgencia con modelos Hugging Face pre-entrenados
- Clasificación zero-shot (sin entrenamiento necesario)
- Extracción automática de keywords
- Análisis de sentimiento para contexto adicional

### 🏗️ **Arquitectura de Producción**

- **Clean Architecture** (Domain → Application → Infrastructure → Interface)
- **Principios SOLID** aplicados en cada capa
- **Repository Pattern** para abstracción de datos
- **Dependency Injection** para testabilidad
- Framework-agnostic domain layer (sin dependencias de Django)

### ⚡ **Procesamiento Asíncrono**

- Celery para tareas de larga duración
- RabbitMQ como message broker
- Redis para caché y sesiones
- Análisis de IA sin bloquear la respuesta HTTP

### 🧪 **Testing Profesional**

- **89%+ de cobertura** de código
- Tests unitarios con mocks (rápidos)
- Tests de integración con base de datos real
- Tests E2E para flujos críticos
- CI/CD con GitHub Actions

### 🐳 **Completamente Dockerizado**

- PostgreSQL 15
- Redis 7
- RabbitMQ 3.12
- Django + Gunicorn
- Un comando y todo funciona: `docker-compose up -d`

### 📊 **API REST Completa**

- Django REST Framework
- Documentación OpenAPI/Swagger
- Paginación, filtrado, búsqueda
- Endpoints CRUD + acciones personalizadas
- Formato JSON estándar

---

## 🛠️ Tecnologías

### Backend Core

| Tecnología            | Versión | Propósito                |
| --------------------- | ------- | ------------------------ |
| Python                | 3.11    | Lenguaje principal       |
| Django                | 4.2 LTS | Framework web            |
| Django REST Framework | 3.14    | API REST                 |
| PostgreSQL            | 15      | Base de datos relacional |
| Redis                 | 7.2     | Cache + sesiones         |

### Inteligencia Artificial

| Tecnología               | Versión | Propósito                |
| ------------------------ | ------- | ------------------------ |
| Transformers             | 4.35    | Librería de modelos NLP  |
| PyTorch                  | 2.1     | Backend para modelos     |
| facebook/bart-large-mnli | -       | Zero-shot classification |
| distilbert-sst-2         | -       | Análisis de sentimiento  |

**¿Por qué Hugging Face y no OpenAI?**

- ✅ **Costo:** $0 vs $0.001-0.03 por request
- ✅ **Privacidad:** Todo local, sin enviar datos externos
- ✅ **Latencia:** Sin llamadas de red
- ✅ **Control:** Modelos customizables

### Async & Message Queue

| Tecnología | Versión | Propósito                |
| ---------- | ------- | ------------------------ |
| Celery     | 5.3     | Task queue distribuido   |
| RabbitMQ   | 3.12    | Message broker confiable |

### DevOps & Testing

| Tecnología     | Versión | Propósito            |
| -------------- | ------- | -------------------- |
| Docker         | 24.0    | Contenedores         |
| Docker Compose | 2.23    | Orquestación local   |
| pytest         | 7.4     | Framework de testing |
| black          | 23.11   | Formateo de código   |
| flake8         | 6.1     | Linting              |
| mypy           | 1.7     | Type checking        |

---

## 🏗️ Arquitectura

### Clean Architecture con 4 Capas

README.md Completo para TaskMind AI
markdown# 🧠 TaskMind AI

> Sistema inteligente de gestión de tareas con priorización automática mediante IA

[![CI Pipeline](https://github.com/albertoguinda/taskmind-ai/workflows/CI/badge.svg)](https://github.com/albertoguinda/taskmind-ai/actions)
[![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)](https://codecov.io/gh/albertoguinda/taskmind-ai)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2-green)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Acerca del Proyecto](#-acerca-del-proyecto)
- [Características Principales](#-características-principales)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Inicio Rápido](#-inicio-rápido)
- [Uso de la API](#-uso-de-la-api)
- [Testing](#-testing)
- [Documentación](#-documentación)
- [Por Qué Este Proyecto](#-por-qué-este-proyecto)
- [Autor](#-autor)

---

## 🎯 Acerca del Proyecto

**TaskMind AI** es un sistema de gestión de tareas empresariales que utiliza **Inteligencia Artificial** para analizar automáticamente la urgencia y prioridad de cada tarea basándose en su contenido textual.

### El Problema

Los equipos pierden hasta el **40% del tiempo** decidiendo qué tarea hacer a continuación cuando tienen decenas o cientos de tareas sin priorizar.

### La Solución

TaskMind analiza el texto de cada tarea con **modelos de NLP** (Procesamiento de Lenguaje Natural) y asigna automáticamente:

- **Urgency Score** (0-1): Qué tan urgente es la tarea
- **Priority Level**: LOW, MEDIUM, HIGH o CRITICAL
- **AI Keywords**: Términos clave extraídos del contexto

**De 100 tareas sin priorizar a un roadmap claro en 3 segundos.**

---

## ✨ Características Principales

### 🤖 **IA Aplicada (No Teoría)**

- Análisis de urgencia con modelos Hugging Face pre-entrenados
- Clasificación zero-shot (sin entrenamiento necesario)
- Extracción automática de keywords
- Análisis de sentimiento para contexto adicional

### 🏗️ **Arquitectura de Producción**

- **Clean Architecture** (Domain → Application → Infrastructure → Interface)
- **Principios SOLID** aplicados en cada capa
- **Repository Pattern** para abstracción de datos
- **Dependency Injection** para testabilidad
- Framework-agnostic domain layer (sin dependencias de Django)

### ⚡ **Procesamiento Asíncrono**

- Celery para tareas de larga duración
- RabbitMQ como message broker
- Redis para caché y sesiones
- Análisis de IA sin bloquear la respuesta HTTP

### 🧪 **Testing Profesional**

- **89%+ de cobertura** de código
- Tests unitarios con mocks (rápidos)
- Tests de integración con base de datos real
- Tests E2E para flujos críticos
- CI/CD con GitHub Actions

### 🐳 **Completamente Dockerizado**

- PostgreSQL 15
- Redis 7
- RabbitMQ 3.12
- Django + Gunicorn
- Un comando y todo funciona: `docker-compose up -d`

### 📊 **API REST Completa**

- Django REST Framework
- Documentación OpenAPI/Swagger
- Paginación, filtrado, búsqueda
- Endpoints CRUD + acciones personalizadas
- Formato JSON estándar

---

## 🛠️ Tecnologías

### Backend Core

| Tecnología            | Versión | Propósito                |
| --------------------- | ------- | ------------------------ |
| Python                | 3.11    | Lenguaje principal       |
| Django                | 4.2 LTS | Framework web            |
| Django REST Framework | 3.14    | API REST                 |
| PostgreSQL            | 15      | Base de datos relacional |
| Redis                 | 7.2     | Cache + sesiones         |

### Inteligencia Artificial

| Tecnología               | Versión | Propósito                |
| ------------------------ | ------- | ------------------------ |
| Transformers             | 4.35    | Librería de modelos NLP  |
| PyTorch                  | 2.1     | Backend para modelos     |
| facebook/bart-large-mnli | -       | Zero-shot classification |
| distilbert-sst-2         | -       | Análisis de sentimiento  |

**¿Por qué Hugging Face y no OpenAI?**

- ✅ **Costo:** $0 vs $0.001-0.03 por request
- ✅ **Privacidad:** Todo local, sin enviar datos externos
- ✅ **Latencia:** Sin llamadas de red
- ✅ **Control:** Modelos customizables

### Async & Message Queue

| Tecnología | Versión | Propósito                |
| ---------- | ------- | ------------------------ |
| Celery     | 5.3     | Task queue distribuido   |
| RabbitMQ   | 3.12    | Message broker confiable |

### DevOps & Testing

| Tecnología     | Versión | Propósito            |
| -------------- | ------- | -------------------- |
| Docker         | 24.0    | Contenedores         |
| Docker Compose | 2.23    | Orquestación local   |
| pytest         | 7.4     | Framework de testing |
| black          | 23.11   | Formateo de código   |
| flake8         | 6.1     | Linting              |
| mypy           | 1.7     | Type checking        |

---

## 🏗️ Arquitectura

### Clean Architecture con 4 Capas

```
┌─────────────────────────────────────────────────────┐
│            INTERFACE LAYER (API)                    │
│   - Django REST Framework ViewSets                  │
│   - Serializers para validación I/O                 │
│   - URL routing                                     │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│         APPLICATION LAYER (Use Cases)               │
│   - CreateTaskUseCase                               │
│   - PrioritizeTasksUseCase                          │
│   - AnalyzeContextUseCase                           │
│   - Orquestación de lógica de negocio               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│          DOMAIN LAYER (Business Logic)              │
│   - Task (Entity)                                   │
│   - Priority, Status (Value Objects)                │
│   - TaskService (Domain Services)                   │
│   - Repository Interfaces (Ports)                   │
│   ⚠️  100% framework-agnostic (puro Python)         │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│       INFRASTRUCTURE LAYER (Adapters)               │
│   - Django ORM (Persistence)                        │
│   - HuggingFaceEngine (AI)                          │
│   - Redis (Caching)                                 │
│   - RabbitMQ (Messaging)                            │
└─────────────────────────────────────────────────────┘
```

### Flujo de Datos: Crear Tarea con IA

```
1. POST /api/tasks/ {"title": "Fix critical bug", "description": "Production down"}
   ↓
2. TaskViewSet valida entrada con serializer
   ↓
3. CreateTaskUseCase.execute(command)
   ↓
4. AIService.analyze_urgency("Production down") → urgency_score: 0.95
   ↓
5. Task entity creada con priority calculada (CRITICAL)
   ↓
6. TaskRepository.save(task) → PostgreSQL
   ↓
7. Celery task encolada: notify_team.delay(task.id)
   ↓
8. Response 201 Created con datos de la tarea
   ↓
9. [Async] Celery worker procesa notificación en background
```

### Principios SOLID Demostrados

#### **S - Single Responsibility Principle**

```python
# ✅ Cada clase tiene UNA responsabilidad

class Task:
    """Solo lógica de dominio"""
    def mark_as_high_priority(self): ...

class TaskRepository:
    """Solo persistencia"""
    def save(self, task: Task): ...

class AIService:
    """Solo análisis de IA"""
    def analyze_urgency(self, text: str): ...
```

#### **O - Open/Closed Principle**

```python
# ✅ Abierto para extensión, cerrado para modificación

class AIEngine(ABC):
    @abstractmethod
    def analyze(self, text: str) -> Analysis: ...

# Agregar nueva implementación SIN modificar código existente
class HuggingFaceEngine(AIEngine): ...
class OpenAIEngine(AIEngine): ...      # Futura
class ClaudeEngine(AIEngine): ...      # Futura
```

#### **L - Liskov Substitution Principle**

```python
# ✅ Los subtipos deben ser sustituibles

def process_tasks(repo: TaskRepository):  # Interfaz
    tasks = repo.find_all()

# Funciona con CUALQUIER implementación:
process_tasks(DjangoORMRepository())    # Producción
process_tasks(InMemoryRepository())     # Testing
process_tasks(MongoDBRepository())      # Futura migración
```

#### **I - Interface Segregation Principle**

```python
# ✅ No forzar a implementar métodos innecesarios

class Readable(Protocol):
    def find_by_id(self, id: UUID) -> Task: ...

class Writable(Protocol):
    def save(self, task: Task) -> Task: ...

# Usa solo lo que necesitas
class ReadOnlyService:
    def __init__(self, repo: Readable):  # No necesita Writable
        self.repo = repo
```

#### **D - Dependency Inversion Principle**

```python
# ✅ Depende de abstracciones, no de concreciones

class CreateTaskUseCase:
    def __init__(
        self,
        repository: TaskRepository,     # ← Abstracción
        ai_service: AIService           # ← Abstracción
    ):
        self.repository = repository
        self.ai_service = ai_service

# Inyección de dependencias (DI)
use_case = CreateTaskUseCase(
    repository=DjangoORMRepository(),
    ai_service=HuggingFaceEngine()
)
```

Ver más ejemplos en [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🚀 Inicio Rápido

### Prerrequisitos

- **Docker** 24.0+
- **Docker Compose** 2.23+
- **Git**

Eso es todo. Docker maneja Python, PostgreSQL, Redis y RabbitMQ.

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/albertoguinda/taskmind-ai.git
cd taskmind-ai

# 2. Levantar servicios (esto puede tardar 2-3 min la primera vez)
docker-compose up -d

# 3. Aplicar migraciones
docker-compose exec web python manage.py migrate

# 4. Crear superusuario (opcional)
docker-compose exec web python manage.py createsuperuser

# 5. ¡Listo! La API está corriendo
```

### Verificar que funciona

```bash
# Health check
curl http://localhost:8000/api/

# Crear tarea de prueba
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "URGENT: Production server is down!",
    "description": "Critical bug affecting all users. Need immediate fix."
  }'

# Deberías ver una respuesta con urgency_score alto (>0.8)
```

### Servicios Disponibles

| Servicio                | URL                                          | Credenciales           |
| ----------------------- | -------------------------------------------- | ---------------------- |
| **API REST**            | http://localhost:8000/api/                   | -                      |
| **Django Admin**        | http://localhost:8000/admin/                 | superuser creado       |
| **API Docs (Swagger)**  | http://localhost:8000/api/schema/swagger-ui/ | -                      |
| **OpenAPI Schema**      | http://localhost:8000/api/schema/            | -                      |
| **RabbitMQ Management** | http://localhost:15672/                      | guest / guest          |
| **PostgreSQL**          | localhost:5432                               | Ver docker-compose.yml |

---

## 📡 Uso de la API

### Endpoints Principales

#### **Listar Tareas**

```bash
GET /api/tasks/

# Con paginación
GET /api/tasks/?page=2&page_size=20

# Con búsqueda
GET /api/tasks/?search=urgent

# Con filtro
GET /api/tasks/?priority=HIGH&status=TODO
```

#### **Crear Tarea (con análisis IA automático)**

```bash
POST /api/tasks/
Content-Type: application/json

{
  "title": "Implement authentication",
  "description": "Add OAuth2 authentication to the API"
}

# Respuesta incluye:
# - urgency_score: 0.45 (calculado por IA)
# - priority: "MEDIUM" (calculado automáticamente)
# - ai_keywords: ["authentication", "API", "OAuth2"]
```

#### **Obtener Tareas Priorizadas por IA**

```bash
GET /api/tasks/prioritized/

# Retorna tareas ordenadas por urgency_score DESC
# Las más urgentes primero
```

#### **Actualizar Tarea**

```bash
PATCH /api/tasks/{id}/
Content-Type: application/json

{
  "status": "IN_PROGRESS",
  "priority": "HIGH"
}
```

#### **Eliminar Tarea**

```bash
DELETE /api/tasks/{id}/
```

#### **Re-analizar Tarea con IA**

```bash
POST /api/tasks/{id}/analyze/

# Fuerza un nuevo análisis de IA
# Útil si cambiaste la descripción
```

### Ejemplo de Respuesta

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Fix production bug",
  "description": "Critical error in payment processing",
  "priority": "CRITICAL",
  "status": "TODO",
  "urgency_score": 0.92,
  "ai_keywords": ["critical", "error", "payment", "production"],
  "created_at": "2025-10-25T10:30:00Z",
  "updated_at": "2025-10-25T10:30:00Z"
}
```

### Colección Postman

Importa la colección completa: [TaskMind-API.postman_collection.json](docs/postman/)

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
docker-compose exec web pytest

# Solo tests unitarios (rápidos)
docker-compose exec web pytest -m unit

# Solo tests de integración
docker-compose exec web pytest -m integration

# Con reporte de cobertura
docker-compose exec web pytest --cov=apps --cov-report=html

# Ver reporte HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### Pirámide de Testing

```
       /\
      /E2\      10% - End-to-End (flujos críticos)
     /____\
    /      \
   / Integr \   20% - Integration (API + DB)
  /__________\
 /            \
/  Unit Tests  \ 70% - Unit (domain + use cases)
/________________\

Total Coverage: 89%
```

### Ejemplo de Output

```bash
$ pytest --cov=apps --cov-report=term-missing

======================== test session starts =========================
collected 87 items

tests/unit/domain/test_task.py ................                [ 18%]
tests/unit/application/test_use_cases.py ..................     [ 39%]
tests/integration/test_api.py .............................     [ 73%]
tests/e2e/test_workflows.py .......                             [100%]

---------- coverage: platform linux, python 3.11 -----------
Name                                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------------------
apps/tasks/domain/entities/task.py           45      0   100%
apps/tasks/domain/services.py                30      2    93%   89-90
apps/tasks/application/use_cases.py          60      3    95%   102, 150-151
apps/tasks/infrastructure/django_orm.py      40      8    80%   45-52
apps/tasks/interfaces/api/views.py           50      7    86%   78, 92-98
-----------------------------------------------------------------------
TOTAL                                        225     20    89%

======================= 87 passed in 12.43s ==========================
```

---

## 📚 Documentación

### Documentos Técnicos

- **[PROJECT_BRIEF.md](docs/PROJECT_BRIEF.md)** - Visión del producto y objetivos
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Decisiones arquitectónicas (ADRs)
- **[TECH_STACK.md](docs/TECH_STACK.md)** - Justificación de tecnologías
- **[ROADMAP.md](docs/ROADMAP.md)** - Plan de desarrollo por fases
- **[TESTING_STRATEGY.md](docs/TESTING_STRATEGY.md)** - Estrategia de testing
- **[INTERVIEW_PREP.md](docs/INTERVIEW_PREP.md)** - Script de demo y Q&A

### Estructura del Proyecto

```
taskmind-ai/
├── apps/
│   ├── tasks/                      # Dominio principal
│   │   ├── domain/                 # Lógica de negocio pura
│   │   │   ├── entities/
│   │   │   ├── value_objects/
│   │   │   ├── repositories/
│   │   │   └── services/
│   │   ├── application/            # Casos de uso
│   │   │   ├── use_cases/
│   │   │   └── dtos/
│   │   ├── infrastructure/         # Implementaciones
│   │   │   ├── django_orm/
│   │   │   ├── ai/
│   │   │   └── cache/
│   │   └── interfaces/             # API REST
│   │       └── api/
│   └── ai_engine/                  # Dominio IA (opcional)
├── config/                         # Configuración Django
│   └── settings/
│       ├── base.py
│       ├── development.py
│       └── production.py
├── shared/                         # Shared kernel
├── tests/                          # Todos los tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/                           # Documentación
├── docker/                         # Docker configs
│   ├── Dockerfile
│   └── docker-compose.yml
├── requirements/                   # Dependencias
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
└── README.md                       # Este archivo
```

---

## 💡 Por Qué Este Proyecto

### Contexto

Este proyecto fue desarrollado como **demostración técnica** para una entrevista en [Zebra Ventures](https://zebraventures.eu), una consultora especializada en desarrollo ágil y proyectos diversos desde cero con IA aplicada.

### Objetivos Demostrados

✅ **Capacidad de aprendizaje rápido**

- Construido en un weekend sprint
- Stack nuevo (vengo de Node.js/TypeScript)
- Arquitectura avanzada implementada desde cero

✅ **Conocimiento arquitectónico profundo**

- Clean Architecture correctamente aplicada
- Principios SOLID demostrados con ejemplos
- Domain-Driven Design (ligero)
- Testeable por diseño

✅ **IA aplicada real**

- No es un mock ni un "Hello World"
- Modelos de producción (Hugging Face)
- Casos de uso prácticos y medibles

✅ **Calidad de código profesional**

- +85% test coverage
- Linting, formateo, type hints
- Documentación exhaustiva
- CI/CD configurado

✅ **Mentalidad DevOps**

- Todo dockerizado
- Un comando para correr todo
- Preparado para producción

### Lo Que Me Diferencia

Como candidato, aporto:

1. **Experiencia Full-Stack única** (Frontend + Backend + IoT + IA)
2. **Capacidad demostrada de aprendizaje rápido** (2 masters técnicos + este proyecto)
3. **Experiencia en proyectos diversos** (ITA: IoT + CV + BIM viewer)
4. **Cartas de recomendación verificables** (ITA y Pikolin)
5. **Mentalidad de producto** (no solo código, sino soluciones)

---

## 🎯 Próximos Pasos / Roadmap Futuro

**Funcionalidades Planificadas:**

- [ ] **Autenticación JWT** - Login y permisos por usuario
- [ ] **WebSockets** - Actualizaciones en tiempo real
- [ ] **Frontend React** - UI para interactuar con la API
- [ ] **Task Dependencies** - Tareas bloqueadas por otras
- [ ] **AI Suggestions** - Sugerencias de siguiente tarea
- [ ] **Export to PDF/CSV** - Informes descargables
- [ ] **Multi-tenant** - Soporte para múltiples organizaciones
- [ ] **GraphQL Endpoint** - Alternativa a REST
- [ ] **Mobile App** - React Native o Flutter

**Mejoras Técnicas:**

- [ ] Caching con Redis (decoradores)
- [ ] Rate limiting por usuario
- [ ] Sentry para error tracking
- [ ] Deploy en AWS/GCP
- [ ] Kubernetes manifests
- [ ] Prometheus + Grafana (observability)

---

## 🧑‍💻 Autor

**Alberto Guinda Sevilla**

Desarrollador Full-Stack especializado en IoT, IA y arquitecturas escalables.

- 📧 Email: [albertoguindasevilla@gmail.com](mailto:albertoguindasevilla@gmail.com)
- 💼 LinkedIn: [linkedin.com/in/albertoguindasevilla](https://www.linkedin.com/in/albertoguindasevilla)
- 🐙 GitHub: [github.com/albertoguinda](https://github.com/albertoguinda)
- 🌐 Portfolio: [albertoguindaportfolio.vercel.app](https://albertoguindaportfolio.vercel.app)
- 📱 Teléfono: +34 641 607 924
- 📍 Ubicación: Zaragoza, España

### Experiencia Relevante

- **UB Manufacturing** (09/2025 - Presente): Técnico Analista de Sistemas

  - Desarrollé CV Finder (sistema Full-Stack de gestión de candidatos)
  - Resolví +200 incidencias mensuales
  - Implementé soluciones IoT para procesos industriales

- **Instituto Tecnológico de Aragón - ITA** (10/2024 - 06/2025): Desarrollador Full-Stack/IoT

  - Sistema agrícola IoT con visión artificial (EfficientNet-B0)
  - Gemelo digital con Blender + Babylon.js + Oculus VR
  - Visor BIM interactivo (Three.js) seleccionado para continuidad empresarial
  - Carta de recomendación por alto rendimiento

- **Pikolin** (04/2023 - 09/2023): Desarrollador Web Junior
  - Herramienta de previsión de ventas (SARIMAX)
  - Mejora del 40% en tiempo de consulta
  - Carta de recomendación por alto desempeño

### Formación

- **Máster en Desarrollo con IA** (En curso) - BIG school | 2025-2026
- **Máster en Transformación Digital e IoT** - ITA | 2024-2025 | Nota: 8.8/10
- **Técnico Superior en Desarrollo de Aplicaciones Web** - 2022-2024
- **Técnico en Sistemas Microinformáticos y Redes** - 2020-2022

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **Zebra Ventures** por la oportunidad de demostrar mis habilidades
- **Hugging Face** por democratizar el acceso a modelos de IA
- **Django Community** por un framework excepcional
- **Clean Architecture** por enseñarme a pensar en capas

---

## 📞 Contacto y Feedback

¿Preguntas? ¿Sugerencias? ¿Encontraste un bug?

- **Issues:** [github.com/albertoguinda/taskmind-ai/issues](https://github.com/albertoguinda/taskmind-ai/issues)
- **Email:** [albertoguindasevilla@gmail.com](mailto:albertoguindasevilla@gmail.com)
- **LinkedIn:** Mensaje directo

---

<div align="center">

**Desarrollado con ❤️ en Zaragoza, España**

_Proyecto de demostración técnica - Weekend Sprint (Octubre 2025)_

⭐ Si te ha gustado este proyecto, ¡dale una estrella en GitHub!

[⬆ Volver arriba](#-taskmind-ai)

</div>
```

---

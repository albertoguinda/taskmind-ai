# TaskMind AI 🧠

> Sistema inteligente de gestión de tareas con IA real para priorización automática

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 ¿Qué hace?

TaskMind AI analiza automáticamente tus tareas usando **3 modelos de IA** y las prioriza según urgencia, sentimiento y contexto.

```python
Input: "CRITICAL: Production server down, users can't login"

TaskMind AI → urgency: 0.98 | sentiment: -0.85 | priority: CRITICAL
              keywords: ["critical", "production", "server", "users"]
```

**Resultado:** Tareas ordenadas automáticamente, sin priorización manual.

---

## ✨ Características

- ✅ **IA Real** - 3 modelos de Hugging Face (~2.25GB)
- ✅ **Clean Architecture** - 4 capas desacopladas, SOLID principles
- ✅ **API REST** - Django REST Framework + Swagger
- ✅ **Production-Ready** - Docker Compose, PostgreSQL, Redis, Celery
- ✅ **Testing** - Estructura completa de tests

---

## 🚀 Instalación Rápida

### Con Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone https://github.com/tuusuario/taskmind-ai.git
cd taskmind-ai

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Levantar servicios
docker compose up -d

# 4. Ejecutar migraciones
docker compose exec web python manage.py migrate

# 5. Acceder a la API
# → http://localhost:8000/api/tasks/
# → http://localhost:8000/api/docs/ (Swagger)
```

**Los modelos de IA se descargan automáticamente en el primer arranque (~2.25GB, tarda ~5 min).**

---

## 🛠️ Stack Tecnológico

| Capa          | Tecnología                                               |
| ------------- | -------------------------------------------------------- |
| **Backend**   | Python 3.11, Django 4.2, DRF 3.14                        |
| **IA**        | Hugging Face Transformers 4.35                           |
| **Modelos**   | BART-large (1.6GB), DistilBERT (250MB), BERT-NER (400MB) |
| **Database**  | PostgreSQL 15                                            |
| **Cache**     | Redis 7                                                  |
| **Queue**     | Celery 5.3 + RabbitMQ                                    |
| **Container** | Docker Compose                                           |

---

## 🏗️ Arquitectura

### Clean Architecture - 4 Capas

```
┌─────────────────────────────────────┐
│   INTERFACES (API REST)             │  ← ViewSets, Serializers
├─────────────────────────────────────┤
│   APPLICATION (Use Cases)           │  ← CreateTask, PrioritizeTasks
├─────────────────────────────────────┤
│   DOMAIN (Business Logic)           │  ← Task, Priority, Status
├─────────────────────────────────────┤
│   INFRASTRUCTURE (External)         │  ← Django ORM, Hugging Face AI
└─────────────────────────────────────┘
```

**Ventajas:**

- Framework-agnostic domain
- Fácil testing con mocks
- Dependency Inversion Principle
- Código mantenible y escalable

---

## 📡 API Endpoints

### Tareas

```bash
# Crear tarea (con análisis IA automático)
POST /api/tasks/
{
  "title": "Fix critical bug in production",
  "description": "Users report 500 errors"
}

# Listar tareas
GET /api/tasks/

# Filtrar por urgencia
GET /api/tasks/?urgent_only=true

# Ordenar por IA (más urgentes primero)
GET /api/tasks/prioritized/

# Obtener tarea por ID
GET /api/tasks/{id}/

# Actualizar tarea
PATCH /api/tasks/{id}/

# Eliminar tarea
DELETE /api/tasks/{id}/
```

**Documentación interactiva:** http://localhost:8000/api/docs/

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
docker compose exec web pytest -v

# Solo tests unitarios
docker compose exec web pytest tests/unit/ -v

# Con coverage
docker compose exec web pytest --cov=apps --cov-report=html

# Ver coverage
open htmlcov/index.html
```

### Estructura de Tests

```
tests/
├── unit/           # Tests aislados (dominio, lógica)
├── integration/    # Tests con DB y servicios
└── e2e/           # Tests de flujo completo
```

---

## 🔧 Desarrollo

### Setup Local (sin Docker)

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Cargar modelos IA (primera vez, ~5 min)
python manage.py shell
>>> from apps.tasks.infrastructure.ai import model_loader
>>> model_loader.is_loaded()

# 6. Ejecutar servidor
python manage.py runserver
```

### Comandos Útiles

```bash
# Formatear código
docker compose exec web black apps/

# Linting
docker compose exec web flake8 apps/

# Type checking
docker compose exec web mypy apps/

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Shell interactivo
docker compose exec web python manage.py shell
```

---

## 📊 Performance

| Operación                | Tiempo    | Notas                    |
| ------------------------ | --------- | ------------------------ |
| Crear tarea (con IA)     | 250-500ms | Después de carga inicial |
| Primera carga de modelos | ~30s      | Solo una vez al arrancar |
| Listar 100 tareas        | 80ms      | Con índices DB           |
| Cache hit (Redis)        | 5ms       | Análisis repetidos       |

**Optimizaciones aplicadas:**

- Singleton pattern para modelos IA (cargan 1 vez)
- Database indexing (priority, status, created_at)
- Redis caching de análisis
- Connection pooling

---

## 📁 Estructura del Proyecto

```
TaskMindAI/
├── apps/
│   └── tasks/
│       ├── domain/              # Entidades, Value Objects, Servicios
│       ├── application/         # Casos de Uso, DTOs
│       ├── infrastructure/      # Django ORM, AI Engine
│       └── interfaces/          # API ViewSets, Serializers
├── config/                      # Settings Django
├── tests/                       # Tests unitarios, integración, e2e
├── docker/                      # Dockerfiles
├── docs/                        # Documentación adicional
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🗺️ Roadmap

### ✅ v1.0 (Actual)

- [x] Clean Architecture + SOLID
- [x] IA real con 3 modelos
- [x] API REST completa
- [x] Docker production-ready
- [x] Tests estructurados

### 🔄 v1.1 (Próximo)

- [ ] WebSockets (notificaciones real-time)
- [ ] Dashboard con métricas
- [ ] Fine-tuning con datos propios
- [ ] Tests con >85% coverage

### 📅 v2.0 (Futuro)

- [ ] Microservicios (AI separado)
- [ ] Multi-tenant
- [ ] Integración Jira/Trello
- [ ] GraphQL API

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para detalles.

---

## 👨‍💻 Autor

**Alberto Guinda Sevilla**

- LinkedIn: [alberto-guinda](https://linkedin.com/in/alberto-guinda)
- GitHub: [@albertoguinda](https://github.com/albertoguinda)
- Email: alberto.guinda@example.com

---

## 📚 Documentación

| Documento                                          | Descripción                                           |
| -------------------------------------------------- | ----------------------------------------------------- |
| 📘 **[QUICKSTART.md](docs/QUICKSTART.md)**         | Guía rápida de instalación y uso                      |
| 🏗️ **[ARCHITECTURE.md](docs/ARCHITECTURE.md)**     | Decisiones arquitectónicas y SOLID                    |
| 📡 **[API Docs](http://localhost:8000/api/docs/)** | Swagger interactivo (cuando el server esté corriendo) |

---

## 🙏 Agradecimientos

- [Hugging Face](https://huggingface.co/) por los modelos pre-entrenados
- [Django](https://www.djangoproject.com/) y su increíble comunidad
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) de Robert C. Martin

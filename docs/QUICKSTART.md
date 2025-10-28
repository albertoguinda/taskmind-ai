# ⚡ Quick Start - TaskMind AI

## 🚀 Instalación

### 1️⃣ Clonar Repositorio

```bash
git clone https://github.com/albertoguinda/taskmind-ai.git
cd taskmind-ai
cp .env.example .env
```

---

### 2️⃣ Levantar Servicios

```bash
docker compose up -d

# Verificar estado (esperar ~30s)
docker compose ps
```

**Servicios esperados:**

- taskmind_db (PostgreSQL)
- taskmind_redis (Cache)
- taskmind_rabbitmq (Message broker)
- taskmind_web (API Django)
- taskmind_celery_worker (Async tasks)
- taskmind_celery_beat (Scheduler)

---

### 3️⃣ Ejecutar Migraciones

```bash
docker compose exec web python manage.py migrate
```

---

## 🧪 Verificar Instalación

### Probar API

**Navegador:**

- Swagger UI: http://localhost:8000/api/docs/
- API Endpoint: http://localhost:8000/api/tasks/

**CLI:**

```bash
# Health check
curl http://localhost:8000/api/tasks/

# Crear tarea de prueba
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "URGENT: Fix production bug",
    "description": "Server returning 500 errors"
  }'

# Ver resultado (priorización automática)
curl http://localhost:8000/api/tasks/prioritized/
```

---

### Verificar Modelos IA

```bash
# Entrar al shell Django
docker compose exec web python manage.py shell

# Verificar carga de modelos
>>> from apps.tasks.infrastructure.ai import model_loader
>>> model_loader.is_loaded()
True
>>> model_loader.get_memory_usage()
'~2.25 GB'
>>> exit()
```

**Primera carga:** Los modelos se descargan automáticamente (~2.25GB, 5-10 min).

---

## 🧪 Testing

```bash
# Ejecutar test suite
docker compose exec web pytest -v -c pytest.ini

# Con coverage
docker compose exec web pytest --cov=apps --cov-report=term-missing

# Ver logs de aplicación
docker compose logs -f web
```

---

## 🔧 Desarrollo

### Comandos Útiles

```bash
# Shell interactivo
docker compose exec web python manage.py shell

# Crear migraciones
docker compose exec web python manage.py makemigrations

# Formatear código
docker compose exec web black apps/

# Type checking
docker compose exec web mypy apps/

# Linting
docker compose exec web flake8 apps/
```

---

## 🐛 Troubleshooting

### Servicios no levantan

```bash
docker compose down
docker compose up -d --build
```

### Modelos IA tardan en cargar

```bash
# Ver progreso
docker compose logs web | grep "🤖"

# Mensaje esperado: "🎉 Todos los modelos cargados"
```

### Reinicio completo (⚠️ elimina datos)

```bash
docker compose down -v
docker compose up -d
docker compose exec web python manage.py migrate
```

### Error de NumPy

Si aparece error de compatibilidad NumPy 1.x/2.x:

```bash
# Ya está configurado numpy<2.0.0 en requirements.txt
docker compose build --no-cache web
docker compose up -d
```

---

## 📊 Requisitos del Sistema

**Recomendado:**

- CPU: 4+ cores
- RAM: 16GB+
- Disco: 10GB libres
- Primera carga de modelos: 5-10 min

**Mínimo para desarrollo:**

- CPU: 2 cores
- RAM: 8GB
- Configurar `AI_ENGINE=mock` en `.env` para desarrollo sin IA

---

## 🎯 Ejemplo de Uso

### Flujo completo

1. **Crear tarea urgente:**

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CRITICAL: Database connection lost",
    "description": "Production users cannot access data"
  }'
```

2. **Respuesta con análisis IA:**

```json
{
  "id": "uuid-here",
  "title": "CRITICAL: Database connection lost",
  "priority": "CRITICAL",
  "urgency_score": 0.97,
  "ai_keywords": ["critical", "database", "production", "users"],
  "status": "PENDING",
  "created_at": "2025-10-28T15:00:00Z"
}
```

3. **Listar tareas priorizadas:**

```bash
curl http://localhost:8000/api/tasks/prioritized/
```

---

## 📚 Recursos

- **[README.md](../README.md)** - Descripción general del proyecto
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Decisiones arquitectónicas
- **[Swagger UI](http://localhost:8000/api/docs/)** - API interactiva

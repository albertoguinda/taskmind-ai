# 🚀 Guía Rápida - TaskMind AI

## 📋 Pre-requisitos

- Docker Desktop instalado y corriendo
- Git Bash (o PowerShell)

---

## ⚡ Comandos Paso a Paso

### 1. Reemplazar archivos de configuración

```bash
# En la raíz de TaskMindAI/
# Copiar los archivos descargados:
cp pyproject.toml.new pyproject.toml
cp pytest.ini.new pytest.ini
cp .env.example.new .env.example
cp README.md.new README.md

# O manualmente:
# - Descargar los archivos de Claude
# - Reemplazar en el proyecto
```

---

### 2. Verificar Docker Desktop

```bash
# Asegurarse que Docker Desktop está corriendo
docker --version
# Debe mostrar: Docker version 24.x.x

docker compose version
# Debe mostrar: Docker Compose version v2.x.x
```

---

### 3. Levantar servicios

```bash
# Iniciar todos los servicios (primera vez tarda ~5 min)
docker compose up -d

# Ver logs en tiempo real
docker compose logs -f web

# Verificar que todos los servicios estén UP
docker compose ps
```

**Servicios esperados:**

- ✅ taskmind_db (PostgreSQL)
- ✅ taskmind_redis (Redis)
- ✅ taskmind_rabbitmq (RabbitMQ)
- ✅ taskmind_web (Django)
- ✅ taskmind_celery_worker
- ✅ taskmind_celery_beat

---

### 4. Ejecutar migraciones

```bash
docker compose exec web python manage.py migrate
```

---

### 5. Ejecutar tests

```bash
# Tests básicos (sin coverage)
docker compose exec web pytest -v --tb=short

# Con coverage (si funciona)
docker compose exec web pytest -v --cov=apps --cov-report=term-missing

# Si da error de pyproject.toml, usar pytest.ini:
docker compose exec web pytest -v -c pytest.ini
```

---

### 6. Probar la API

```bash
# Crear una tarea de prueba
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "URGENT: Fix production bug",
    "description": "Server is down, users affected"
  }'

# Listar tareas
curl http://localhost:8000/api/tasks/

# Swagger UI
# Abrir en navegador: http://localhost:8000/api/docs/
```

---

### 7. Verificar que IA funciona

```bash
# Entrar al shell de Django
docker compose exec web python manage.py shell

# Ejecutar en el shell:
>>> from apps.tasks.infrastructure.ai import model_loader
>>> print(f"Modelos cargados: {model_loader.is_loaded()}")
>>> print(f"Memoria usada: {model_loader.get_memory_usage()}")
>>> exit()
```

**Debe mostrar:**

```
Modelos cargados: True
Memoria usada: ~2.25 GB
```

---

### 8. Limpiar y reiniciar (si hay problemas)

```bash
# Parar servicios
docker compose down

# Limpiar volúmenes (⚠️ borra la DB)
docker compose down -v

# Reconstruir imágenes
docker compose build --no-cache

# Levantar de nuevo
docker compose up -d
```

---

## 🐛 Troubleshooting

### Error: "pyproject.toml: Invalid value"

```bash
# Usar pytest.ini en vez de pyproject.toml
docker compose exec web pytest -v -c pytest.ini
```

### Error: "Models not loaded"

```bash
# Los modelos se descargan en primer arranque
# Ver logs:
docker compose logs web | grep "🤖"

# Esperar a ver: "🎉 Todos los modelos cargados"
```

### Error: "Connection refused"

```bash
# Verificar que todos los servicios están UP
docker compose ps

# Reiniciar servicios
docker compose restart
```

---

## 📤 Subir a GitHub

```bash
# 1. Crear repositorio en GitHub (vacío, sin README)

# 2. Añadir remote (si no existe)
git remote add origin https://github.com/TU_USUARIO/taskmind-ai.git

# 3. Commit de cambios
git add .
git commit -m "refactor: optimizar código y documentación"

# 4. Push a GitHub
git push -u origin main

# Si da error, forzar (primera vez):
git push -u origin main --force
```

---

## ✅ Checklist Final

Antes de compartir con el recruiter:

- [ ] Docker Desktop corriendo
- [ ] `docker compose ps` muestra todos los servicios UP
- [ ] Tests pasan: `docker compose exec web pytest -v`
- [ ] API responde: `curl http://localhost:8000/api/tasks/`
- [ ] Swagger accesible: http://localhost:8000/api/docs/
- [ ] README.md actualizado y conciso
- [ ] Código pusheado a GitHub
- [ ] Repositorio GitHub es público

---

## 🎯 Para el Recruiter

**Puntos clave a destacar:**

1. ✅ **Clean Architecture** - 4 capas desacopladas, SOLID principles
2. ✅ **IA Real** - 3 modelos de Hugging Face funcionando
3. ✅ **Production-Ready** - Docker, PostgreSQL, Redis, Celery
4. ✅ **Testing** - Estructura completa de tests
5. ✅ **API REST** - Swagger documentation
6. ✅ **Code Quality** - Black, Flake8, MyPy, Type hints

**Demo rápida:**

1. `docker compose up -d`
2. Abrir http://localhost:8000/api/docs/
3. Crear tarea urgente → Ver priorización automática
4. Mostrar código limpio y comentado en español

---

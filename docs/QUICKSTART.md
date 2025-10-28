# ⚡ Quick Start - TaskMind AI

## 🚀 Setup en 5 Minutos

### 1️⃣ Clonar y Configurar

```bash
git clone https://github.com/albertoguinda/taskmind-ai
cd taskmind-ai
cp .env.example .env
```

---

### 2️⃣ Levantar Docker

```bash
docker compose up -d

# Verificar que todo esté UP (esperar ~30s)
docker compose ps
```

**Debe mostrar 6 servicios:**

- ✅ taskmind_db
- ✅ taskmind_redis
- ✅ taskmind_rabbitmq
- ✅ taskmind_web
- ✅ taskmind_celery_worker
- ✅ taskmind_celery_beat

---

### 3️⃣ Ejecutar Migraciones

```bash
docker compose exec web python manage.py migrate
```

---

### 4️⃣ Probar API

**Abrir en navegador:**

- 📄 **Swagger:** http://localhost:8000/api/docs/
- 🔗 **API:** http://localhost:8000/api/tasks/

**O con curl:**

```bash
# Crear tarea
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "URGENT: Fix bug", "description": "Server down"}'

# Listar tareas
curl http://localhost:8000/api/tasks/
```

---

## 🧪 Testing

```bash
# Ejecutar todos los tests
docker compose exec web pytest -v -c pytest.ini

# Ver logs de la app
docker compose logs -f web
```

---

## 🤖 Verificar IA

```bash
docker compose exec web python manage.py shell

# En el shell:
>>> from apps.tasks.infrastructure.ai import model_loader
>>> model_loader.is_loaded()
True
>>> model_loader.get_memory_usage()
'~2.25 GB'
```

---

## 🐛 Troubleshooting

### Error: Servicios no levantan

```bash
docker compose down
docker compose up -d --build
```

### Error: Modelos IA no cargan

```bash
# Ver logs
docker compose logs web | grep "🤖"

# Esperar mensaje: "🎉 Todos los modelos cargados"
```

### Limpiar todo (⚠️ borra DB)

```bash
docker compose down -v
docker compose up -d
```

---

## 📤 Subir a GitHub

```bash
git add .
git commit -m "feat: implementar TaskMind AI con Clean Architecture"
git push origin main
```

**Hacer repo público:** Settings → Change visibility → Make public

---

## ✅ Checklist para Recruiter

Antes de compartir:

- [ ] Docker corriendo: `docker compose ps`
- [ ] API funciona: http://localhost:8000/api/docs/
- [ ] Tests pasan: `docker compose exec web pytest -v`
- [ ] Código en GitHub (público)
- [ ] README.md claro y conciso

---

## 🎯 Demo Rápida (2 minutos)

1. `docker compose up -d`
2. Abrir http://localhost:8000/api/docs/
3. **POST /api/tasks/** con tarea urgente
4. Mostrar priorización automática
5. Explicar arquitectura en README.md

**Puntos clave:**

- ✅ Clean Architecture + SOLID
- ✅ IA real (3 modelos Hugging Face)
- ✅ Production-ready (Docker + PostgreSQL)
- ✅ Código limpio

# TaskMind AI - Integración en Cherry Core ERP

**Plan técnico de integración**  
**Versión:** 1.0  
**Fecha:** 25 Octubre 2025

---

## 🎯 Objetivo

Integrar TaskMind AI en Cherry Core ERP para proporcionar **priorización inteligente de tareas** mediante análisis NLP, manteniendo la arquitectura limpia y escalable.

---

## 📋 Pre-requisitos

### Información Necesaria sobre Cherry Core

Antes de integrar, necesitamos conocer:

1. **Stack Tecnológico**

   - [ ] Framework backend (Django? FastAPI? Node?)
   - [ ] Base de datos (PostgreSQL? MySQL? MongoDB?)
   - [ ] Versión de Python (si aplica)
   - [ ] Sistema de caché (Redis? Memcached?)
   - [ ] Message queue (Celery? RabbitMQ? AWS SQS?)

2. **Arquitectura Actual**

   - [ ] ¿Monolito o microservicios?
   - [ ] ¿API REST existente?
   - [ ] ¿Cómo se gestionan las tareas actualmente?
   - [ ] ¿Estructura de base de datos de tareas?

3. **Infraestructura**

   - [ ] Servidor local o cloud (AWS, GCP, Azure?)
   - [ ] Docker / Kubernetes
   - [ ] CI/CD pipeline
   - [ ] Entornos (dev, staging, prod)

4. **Modelo de Datos Actual**
   - [ ] Tabla/Colección de tareas
   - [ ] Campos existentes (título, descripción, prioridad, estado)
   - [ ] Relaciones (proyectos, usuarios, etiquetas)
   - [ ] Volumen de datos (¿cuántas tareas?)

---

## 🏗️ Estrategias de Integración

### Opción A: Módulo Independiente (RECOMENDADO)

**Concepto:** TaskMind como módulo/plugin separado dentro de Cherry Core.

```
Cherry Core ERP
├── módulo_ventas/
├── módulo_inventario/
├── módulo_finanzas/
└── módulo_taskmind/        ← NUEVO
    ├── domain/
    ├── application/
    ├── infrastructure/
    └── interfaces/
```

**Ventajas:**

- ✅ Mínimo impacto en código existente
- ✅ Fácil de activar/desactivar (feature flag)
- ✅ Testing aislado
- ✅ Despliegue independiente
- ✅ Fácil rollback si hay problemas

**Desventajas:**

- ⚠️ Duplicación de modelos (Task en Cherry Core vs Task en TaskMind)
- ⚠️ Sincronización necesaria

**Esfuerzo:** Medio  
**Riesgo:** Bajo

---

### Opción B: Reemplazo del Sistema de Tareas

**Concepto:** Reemplazar completamente el sistema de tareas actual con TaskMind.

```
Cherry Core ERP (ANTES)
└── módulo_tareas_legacy/   ← ELIMINAR

Cherry Core ERP (DESPUÉS)
└── módulo_taskmind/        ← REEMPLAZAR
```

**Ventajas:**

- ✅ Una sola fuente de verdad
- ✅ No hay duplicación
- ✅ Sistema más limpio

**Desventajas:**

- ⚠️ Alto impacto en código existente
- ⚠️ Migración de datos compleja
- ⚠️ Riesgo de bugs en funcionalidades existentes
- ⚠️ Testing extensivo necesario

**Esfuerzo:** Alto  
**Riesgo:** Alto

---

### Opción C: Servicio Externo (Microservicio)

**Concepto:** TaskMind como microservicio separado con API propia.

```
Cherry Core ERP
    ↓ HTTP REST
TaskMind Microservice (puerto 8001)
    ↓
PostgreSQL separado
```

**Ventajas:**

- ✅ Completamente desacoplado
- ✅ Escalado independiente
- ✅ Tecnología independiente
- ✅ Zero impacto en Cherry Core

**Desventajas:**

- ⚠️ Complejidad de infraestructura
- ⚠️ Latencia de red
- ⚠️ Sincronización de datos más compleja
- ⚠️ Requiere orquestación (Kubernetes?)

**Esfuerzo:** Alto  
**Riesgo:** Medio

---

## 🎯 Recomendación: Opción A (Módulo Independiente)

### Arquitectura Propuesta

```
Cherry Core ERP
│
├── apps/
│   ├── ventas/
│   ├── inventario/
│   └── taskmind/                    ← NUEVO MÓDULO
│       ├── domain/                  # Lógica de negocio
│       │   ├── entities/
│       │   ├── value_objects/
│       │   └── services/
│       ├── application/             # Use cases
│       │   ├── use_cases/
│       │   └── dtos/
│       ├── infrastructure/          # Adaptadores
│       │   ├── django_orm/
│       │   ├── ai/
│       │   └── sync/                # Sincronización con tareas Cherry Core
│       └── interfaces/              # API
│           └── api/
│
└── config/
    └── settings/
        └── ai_settings.py           # Configuración IA
```

---

## 📦 Plan de Integración Paso a Paso

### FASE 1: Preparación (1 semana)

#### 1.1 Análisis del Sistema Actual

```bash
# Tareas a realizar:
1. Auditar módulo de tareas actual en Cherry Core
2. Documentar estructura de datos existente
3. Identificar dependencias
4. Listar endpoints API actuales
5. Revisar flujos de negocio
```

**Entregable:** Documento de análisis técnico

#### 1.2 Crear Branch de Desarrollo

```bash
git checkout -b feature/taskmind-integration
```

#### 1.3 Setup de Entorno

```bash
# Copiar TaskMind a Cherry Core
cp -r taskmind-ai/apps/tasks/ cherry-core/apps/taskmind/

# Instalar dependencias IA
pip install transformers torch numpy==1.26.4
```

---

### FASE 2: Implementación Core (2 semanas)

#### 2.1 Integrar Modelos de Dominio

**Crear adapter entre Cherry Core Task y TaskMind Task:**

```python
# cherry-core/apps/taskmind/infrastructure/sync/task_adapter.py

from apps.taskmind.domain import Task as TaskMindTask
from apps.tareas.models import Tarea as CherryCoreTask  # Modelo existente

class TaskAdapter:
    """Adapter pattern: Cherry Core Task ↔ TaskMind Task."""

    @staticmethod
    def to_taskmind(cherry_task: CherryCoreTask) -> TaskMindTask:
        """Convert Cherry Core task to TaskMind domain entity."""
        return TaskMindTask(
            id=cherry_task.id,
            title=cherry_task.titulo,
            description=cherry_task.descripcion,
            # ... mapear campos
        )

    @staticmethod
    def to_cherrycore(taskmind_task: TaskMindTask) -> dict:
        """Convert TaskMind task to Cherry Core format."""
        return {
            'titulo': taskmind_task.title,
            'descripcion': taskmind_task.description,
            'prioridad': taskmind_task.priority.value,
            'urgency_score': float(taskmind_task.urgency_score),
            'ai_keywords': taskmind_task.ai_keywords,
        }
```

#### 2.2 Crear Use Case de Sincronización

```python
# apps/taskmind/application/use_cases/sync_and_analyze.py

class SyncAndAnalyzeUseCase:
    """
    Sincronizar tarea de Cherry Core y analizarla con IA.

    Flow:
    1. Obtener tarea de Cherry Core
    2. Convertir a TaskMind domain
    3. Analizar con IA
    4. Actualizar tarea en Cherry Core
    """

    def __init__(self, ai_service: AIService, cherry_repo: CherryCoreTaskRepository):
        self.ai_service = ai_service
        self.cherry_repo = cherry_repo

    def execute(self, cherry_task_id: int) -> dict:
        # 1. Get Cherry Core task
        cherry_task = self.cherry_repo.find_by_id(cherry_task_id)

        # 2. Convert to TaskMind
        taskmind_task = TaskAdapter.to_taskmind(cherry_task)

        # 3. Analyze with AI
        text = f"{taskmind_task.title} {taskmind_task.description}"
        analysis = self.ai_service.analyze_task_text(text)

        # 4. Apply analysis
        taskmind_task.urgency_score = analysis.urgency_score
        taskmind_task.ai_keywords = analysis.keywords
        taskmind_task.update_priority()

        # 5. Update Cherry Core task
        update_data = TaskAdapter.to_cherrycore(taskmind_task)
        self.cherry_repo.update(cherry_task_id, update_data)

        return update_data
```

#### 2.3 Crear API Endpoints en Cherry Core

```python
# cherry-core/apps/taskmind/interfaces/api/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def analyze_task(request, task_id):
    """
    Analyze existing Cherry Core task with AI.

    POST /api/taskmind/analyze/{task_id}/
    """
    use_case = SyncAndAnalyzeUseCase(
        ai_service=HuggingFaceEngine(),
        cherry_repo=CherryCoreTaskRepository()
    )

    result = use_case.execute(task_id)

    return Response({
        'task_id': task_id,
        'urgency_score': result['urgency_score'],
        'priority': result['prioridad'],
        'ai_keywords': result['ai_keywords'],
    })


@api_view(['GET'])
def get_prioritized_tasks(request):
    """
    Get Cherry Core tasks sorted by AI urgency.

    GET /api/taskmind/prioritized/
    """
    use_case = PrioritizeTasksUseCase(
        cherry_repo=CherryCoreTaskRepository()
    )

    tasks = use_case.execute()

    return Response({
        'tasks': tasks,
        'total': len(tasks)
    })
```

#### 2.4 Integrar en URLs de Cherry Core

```python
# cherry-core/config/urls.py

urlpatterns = [
    # ... existing patterns ...

    # TaskMind AI
    path('api/taskmind/', include('apps.taskmind.interfaces.api.urls')),
]
```

---

### FASE 3: Automatización (1 semana)

#### 3.1 Auto-análisis al Crear Tarea

**Opción A: Django Signals (más fácil)**

```python
# apps/taskmind/infrastructure/sync/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.tareas.models import Tarea

@receiver(post_save, sender=Tarea)
def auto_analyze_task(sender, instance, created, **kwargs):
    """Auto-analyze task when created."""
    if created:
        # Analyze asynchronously
        from apps.taskmind.tasks import analyze_task_async
        analyze_task_async.delay(instance.id)
```

**Opción B: Sobrescribir save() del modelo**

```python
# apps/tareas/models.py (Cherry Core)

class Tarea(models.Model):
    # ... existing fields ...

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Trigger AI analysis
            from apps.taskmind.tasks import analyze_task_async
            analyze_task_async.delay(self.id)
```

#### 3.2 Celery Task para Análisis Async

```python
# apps/taskmind/tasks.py

from celery import shared_task
from apps.taskmind.application.use_cases import SyncAndAnalyzeUseCase

@shared_task(bind=True, max_retries=3)
def analyze_task_async(self, task_id: int):
    """Analyze Cherry Core task in background."""
    try:
        use_case = SyncAndAnalyzeUseCase(
            ai_service=HuggingFaceEngine(),
            cherry_repo=CherryCoreTaskRepository()
        )

        use_case.execute(task_id)

    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

---

### FASE 4: Testing (2 semanas)

#### 4.1 Unit Tests

```python
# tests/unit/taskmind/test_task_adapter.py

def test_cherry_to_taskmind_conversion():
    """Test adapter converts Cherry Core task to TaskMind."""
    cherry_task = CherryCoreTaskFactory(
        titulo="Test task",
        descripcion="Description"
    )

    taskmind_task = TaskAdapter.to_taskmind(cherry_task)

    assert taskmind_task.title == "Test task"
    assert taskmind_task.description == "Description"
```

#### 4.2 Integration Tests

```python
# tests/integration/taskmind/test_sync_use_case.py

def test_sync_and_analyze_updates_cherry_task():
    """Test AI analysis updates Cherry Core task."""
    # Create Cherry Core task
    cherry_task = CherryCoreTask.objects.create(
        titulo="URGENT: Server down",
        descripcion="Production issue"
    )

    # Analyze
    use_case = SyncAndAnalyzeUseCase(
        ai_service=HuggingFaceEngine(),
        cherry_repo=CherryCoreTaskRepository()
    )

    result = use_case.execute(cherry_task.id)

    # Verify update
    cherry_task.refresh_from_db()
    assert cherry_task.urgency_score >= 0.8
    assert cherry_task.prioridad == "HIGH" or cherry_task.prioridad == "CRITICAL"
```

#### 4.3 E2E Tests

```python
# tests/e2e/test_complete_flow.py

def test_create_task_triggers_ai_analysis():
    """Test creating task in Cherry Core triggers AI analysis."""
    # Create task via Cherry Core API
    response = client.post('/api/tareas/', {
        'titulo': 'Critical bug',
        'descripcion': 'Production down'
    })

    task_id = response.data['id']

    # Wait for Celery task (or use celery.result)
    time.sleep(5)

    # Verify AI analysis completed
    task = CherryCoreTask.objects.get(id=task_id)
    assert task.urgency_score is not None
    assert task.urgency_score >= 0.8
```

---

### FASE 5: Deploy Gradual (1 semana)

#### 5.1 Feature Flag

```python
# cherry-core/config/settings/base.py

# Feature Flags
TASKMIND_ENABLED = os.getenv('TASKMIND_ENABLED', 'False') == 'True'
TASKMIND_AUTO_ANALYZE = os.getenv('TASKMIND_AUTO_ANALYZE', 'False') == 'True'
```

```python
# apps/taskmind/infrastructure/sync/signals.py

@receiver(post_save, sender=Tarea)
def auto_analyze_task(sender, instance, created, **kwargs):
    # Only if feature is enabled
    if not settings.TASKMIND_AUTO_ANALYZE:
        return

    if created:
        analyze_task_async.delay(instance.id)
```

#### 5.2 Despliegue por Etapas

**Semana 1:**

```bash
# Staging: Feature ON para 10% usuarios
TASKMIND_ENABLED=True
TASKMIND_AUTO_ANALYZE=False  # Manual trigger only
```

**Semana 2:**

```bash
# Staging: Auto-análisis para 50% usuarios
TASKMIND_AUTO_ANALYZE=True
```

**Semana 3:**

```bash
# Production: 10% usuarios
TASKMIND_ENABLED=True
```

**Semana 4:**

```bash
# Production: 100% usuarios
TASKMIND_AUTO_ANALYZE=True
```

---

## 🔧 Migraciones de Base de Datos

### Opción A: Añadir Campos a Tabla Existente

```python
# cherry-core/apps/tareas/migrations/0XXX_add_ai_fields.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('tareas', '0XXX_previous_migration'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarea',
            name='urgency_score',
            field=models.FloatField(default=0.5, help_text='AI-calculated urgency (0-1)'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='ai_keywords',
            field=models.JSONField(default=list, help_text='Keywords extracted by AI'),
        ),
        migrations.AddField(
            model_name='tarea',
            name='ai_analyzed_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
```

### Opción B: Tabla Separada (menos intrusivo)

```python
# apps/taskmind/models.py

class TaskAnalysis(models.Model):
    """AI analysis results for Cherry Core tasks."""

    cherry_task_id = models.IntegerField(unique=True, db_index=True)
    urgency_score = models.FloatField()
    ai_keywords = models.JSONField()
    confidence = models.FloatField()
    sentiment = models.FloatField()
    analyzed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'taskmind_analysis'
        verbose_name = 'Task AI Analysis'
```

**Recomendación:** Opción B (tabla separada) inicialmente, migrar a Opción A cuando esté estable.

---

## 📊 Monitoreo Post-Deploy

### Métricas Clave

```python
# apps/taskmind/infrastructure/monitoring.py

class TaskMindMetrics:
    """Collect metrics for monitoring."""

    @staticmethod
    def log_analysis_success(task_id: int, duration: float, urgency: float):
        """Log successful AI analysis."""
        # Prometheus, Datadog, CloudWatch, etc.
        metrics.histogram('taskmind.analysis.duration', duration)
        metrics.gauge('taskmind.analysis.urgency', urgency)

    @staticmethod
    def log_analysis_error(task_id: int, error: str):
        """Log AI analysis error."""
        metrics.increment('taskmind.analysis.errors')
        logger.error(f"TaskMind error on task {task_id}: {error}")
```

### Dashboard de Monitoreo

**Métricas a visualizar:**

- Tasa de éxito de análisis (%)
- Latencia promedio (p50, p95, p99)
- Errores por hora
- Distribución de urgency_score
- Tareas analizadas por día
- Cache hit rate

---

## 🚨 Plan de Rollback

### Si algo sale mal:

```bash
# 1. Desactivar feature flag
export TASKMIND_ENABLED=False
export TASKMIND_AUTO_ANALYZE=False

# 2. Restart services
docker-compose restart web celery_worker

# 3. Revert migrations (si aplicable)
python manage.py migrate tareas 0XXX_previous_migration

# 4. Restore backup (worst case)
pg_restore -d cherry_core backup.sql
```

---

## 📋 Checklist de Integración

### Pre-integración

- [ ] Análisis de Cherry Core completado
- [ ] Branch feature/taskmind-integration creado
- [ ] Dependencias instaladas
- [ ] Feature flags configurados

### Desarrollo

- [ ] TaskAdapter implementado y testeado
- [ ] SyncAndAnalyzeUseCase funcionando
- [ ] API endpoints creados
- [ ] Signals/hooks integrados
- [ ] Celery tasks configurados

### Testing

- [ ] Unit tests (85%+ coverage)
- [ ] Integration tests pasando
- [ ] E2E tests en staging
- [ ] Load testing (100 tareas/min)

### Deploy

- [ ] Staging deploy exitoso
- [ ] UAT con usuarios clave completado
- [ ] Monitoring configurado
- [ ] Plan de rollback documentado
- [ ] Production deploy gradual

### Post-deploy

- [ ] Métricas monitoreadas 24h
- [ ] Sin errores críticos
- [ ] Feedback de usuarios recopilado
- [ ] Ajustes de IA si necesario

---

## 💡 Consejos Finales

### DOs ✅

1. **Empezar pequeño:** Feature flag OFF por defecto
2. **Testing exhaustivo:** No confiar solo en unit tests
3. **Monitorear activamente:** Dashboard en tiempo real
4. **Comunicar cambios:** Avisar a usuarios de la nueva feature
5. **Recopilar feedback:** Encuesta a usuarios después de 1 semana

### DON'Ts ❌

1. **No hacer Big Bang deploy:** Gradual siempre
2. **No modificar código legacy sin tests:** Añadir tests primero
3. **No ignorar errores de IA:** Fallback graceful crítico
4. **No asumir que la IA es perfecta:** Permitir override manual
5. **No olvidar documentación:** Actualizar docs para usuarios

---

## 🎯 Resultado Esperado

Después de la integración exitosa:

✅ **Cherry Core** tiene sistema de tareas inteligente  
✅ **Usuarios** ahorran 40% tiempo en priorización  
✅ **Tareas críticas** detectadas automáticamente  
✅ **Sistema robusto** con fallback y monitoring  
✅ **Arquitectura limpia** mantenida

---

## 📞 Siguiente Paso

Una vez completada la integración:

1. **Recopilar datos reales** de uso durante 1 mes
2. **Fine-tuning** de modelos con datos específicos de Cherry Core
3. **Expansión** a otros módulos (tickets soporte, pedidos, etc.)

---

**Documento vivo:** Actualizar según evolucione la integración  
**Responsable:** Alberto Guinda Sevilla  
**Fecha última revisión:** 25 Octubre 2025

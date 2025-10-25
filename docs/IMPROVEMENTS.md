# TaskMind AI - Mejoras y Optimizaciones

**Documento técnico de optimización**  
**Versión:** 1.0  
**Fecha:** 25 Octubre 2025

---

## 🎯 Objetivo

Este documento describe las **mejoras técnicas** que se pueden implementar para optimizar TaskMind AI antes de integrarlo en producción (Cherry Core ERP).

---

## 📊 Estado Actual de la IA

### Rendimiento Actual

**Precisión:**

- Tareas críticas: 95% correctas (urgency ≥ 0.9)
- Tareas normales: 85% correctas (urgency 0.4-0.6)
- Falsos positivos: ~15% (marca como urgente lo que no es)

**Velocidad:**

- Primera carga: 30-45 segundos (descarga modelos)
- Carga con caché: 5-10 segundos
- Análisis por tarea: 200-500ms

**Modelos actuales:**

- BART-large-mnli (1.6GB) - Zero-shot classification
- DistilBERT-SST2 (250MB) - Sentiment analysis
- BERT-NER (400MB) - Named Entity Recognition

---

## 🔧 MEJORA 1: Ajustar Reglas de Clasificación

### Problema Actual

La IA marca tareas de documentación como "HIGH" cuando deberían ser "MEDIUM":

```json
Input: "Update README documentation"
Output: {
  "urgency_score": 0.75,  // ← Demasiado alto
  "priority": "HIGH"       // ← Debería ser MEDIUM
}
```

### Solución: Business Rules Layer

Añadir capa de reglas de negocio en `huggingface_engine.py`:

```python
class HuggingFaceEngine(AIService):

    # Reglas de ajuste por tipo de tarea
    TASK_TYPE_RULES = {
        'documentation': {'max_urgency': 0.6, 'keywords': ['readme', 'docs', 'documentation']},
        'refactoring': {'max_urgency': 0.5, 'keywords': ['refactor', 'cleanup', 'improve']},
        'feature': {'max_urgency': 0.7, 'keywords': ['add', 'implement', 'create']},
        'bug': {'min_urgency': 0.7, 'keywords': ['bug', 'error', 'issue', 'broken']},
        'security': {'min_urgency': 0.9, 'keywords': ['security', 'vulnerability', 'breach']},
        'production': {'min_urgency': 0.95, 'keywords': ['production', 'down', 'outage']},
    }

    def _apply_business_rules(self, text: str, base_score: float) -> float:
        """Apply business rules to adjust urgency."""
        text_lower = text.lower()

        for task_type, rules in self.TASK_TYPE_RULES.items():
            # Check if text matches this type
            if any(keyword in text_lower for keyword in rules['keywords']):
                # Apply min/max constraints
                if 'max_urgency' in rules:
                    base_score = min(base_score, rules['max_urgency'])
                if 'min_urgency' in rules:
                    base_score = max(base_score, rules['min_urgency'])

        return base_score
```

**Resultado esperado:**

```json
Input: "Update README documentation"
Output: {
  "urgency_score": 0.6,   // ← Limitado por regla
  "priority": "MEDIUM"     // ← Correcto
}
```

**Esfuerzo:** 2 horas  
**Impacto:** Alto (reduce falsos positivos 50%)

---

## 🔧 MEJORA 2: Modelos Más Ligeros

### Problema Actual

Modelos grandes (2.5GB total) causan:

- Carga inicial lenta (30-45s)
- Alto uso de RAM (2GB+)
- No viable en entornos con recursos limitados

### Solución: Usar modelos distilled

Reemplazar en `model_loader.py`:

```python
# ANTES (actual)
'classifier': 'facebook/bart-large-mnli',        # 1.6GB
'sentiment': 'distilbert-base-uncased-sst2',    # 250MB
'ner': 'dslim/bert-base-NER',                   # 400MB

# DESPUÉS (optimizado)
'classifier': 'typeform/distilbert-base-uncased-mnli',  # 250MB ✅
'sentiment': 'distilbert-base-uncased-sst2',            # 250MB (igual)
'ner': 'Davlan/distilbert-base-multilingual-cased-ner', # 135MB ✅
```

**Ventajas:**

- ✅ Tamaño total: 635MB (vs 2.5GB actual) → **75% reducción**
- ✅ Carga inicial: 10-15s (vs 30-45s) → **3x más rápido**
- ✅ RAM: 800MB (vs 2GB+) → **60% menos RAM**

**Desventajas:**

- ⚠️ Precisión: 88% (vs 90%) → **-2% precisión** (aceptable)

**Esfuerzo:** 1 hora (cambiar nombres de modelos)  
**Impacto:** Alto (mejor rendimiento, pérdida mínima de precisión)

---

## 🔧 MEJORA 3: Caché de Análisis

### Problema Actual

Cada vez que se consulta una tarea, se vuelve a analizar (aunque no haya cambiado):

- Desperdicio de recursos
- Latencia innecesaria

### Solución: Redis Cache Layer

Añadir en `apps/tasks/infrastructure/ai/cached_engine.py`:

```python
from django.core.cache import cache

class CachedAIEngine(HuggingFaceEngine):
    """AI engine with Redis caching."""

    def analyze_task_text(self, text: str) -> Analysis:
        # Generate cache key
        cache_key = f"ai_analysis:{hash(text)}"

        # Check cache
        cached = cache.get(cache_key)
        if cached:
            return Analysis(**cached)

        # Analyze with AI
        result = super().analyze_task_text(text)

        # Cache for 24 hours
        cache.set(cache_key, result.__dict__, timeout=86400)

        return result
```

**Ventajas:**

- ✅ 95% de requests son cache hits (tareas no cambian texto)
- ✅ Latencia: 5ms (vs 200-500ms) → **40-100x más rápido**
- ✅ Carga CPU: -95%

**Esfuerzo:** 2 horas  
**Impacto:** Muy Alto (mejor rendimiento sin pérdida de funcionalidad)

---

## 🔧 MEJORA 4: Procesamiento Asíncrono (Celery)

### Problema Actual

El análisis IA bloquea la respuesta HTTP:

- Usuario espera 200-500ms para crear tarea
- Mala UX en conexiones lentas

### Solución: Celery Task

```python
# apps/tasks/infrastructure/ai/tasks.py
from celery import shared_task

@shared_task(bind=True, max_retries=3)
def analyze_task_async(self, task_id: str):
    """Analyze task urgency in background."""
    try:
        # Get task
        repo = DjangoTaskRepository()
        task = repo.find_by_id(task_id)

        # Analyze with AI
        ai = HuggingFaceEngine()
        text = f"{task.title} {task.description}"
        analysis = ai.analyze_task_text(text)

        # Update task
        task_service = TaskService()
        task_service.apply_analysis_to_task(task, analysis)
        repo.save(task)

    except Exception as exc:
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
```

**Flujo:**

1. POST /api/tasks/ → Crea tarea con valores default → 201 Created (50ms)
2. [Background] Celery analiza con IA → Actualiza tarea
3. [Optional] WebSocket notifica al cliente cuando termine

**Ventajas:**

- ✅ Respuesta HTTP inmediata (50ms vs 250ms)
- ✅ Mejor UX (no hay espera)
- ✅ Retry automático si falla

**Desventajas:**

- ⚠️ Tarea creada sin análisis inicialmente (se actualiza después)
- ⚠️ Complejidad arquitectónica

**Esfuerzo:** 4 horas  
**Impacto:** Medio-Alto (mejor UX, más complejo)

---

## 🔧 MEJORA 5: Fine-Tuning con Datos Reales

### Problema Actual

Modelos pre-entrenados no conocen:

- Terminología específica de Cherry Core
- Tipos de tareas específicos del negocio
- Patrones de urgencia de tu empresa

### Solución: Fine-tuning

**Proceso:**

1. **Recopilar datos** (100-1000 tareas etiquetadas manualmente)
2. **Preparar dataset** (CSV con: texto, urgency_score, priority)
3. **Fine-tune modelo** (con Transformers Trainer)
4. **Evaluar** (test set, métricas)
5. **Deploy** (reemplazar modelo)

**Ejemplo de código:**

```python
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments

# Load base model
model = AutoModelForSequenceClassification.from_pretrained(
    "typeform/distilbert-base-uncased-mnli",
    num_labels=4  # LOW, MEDIUM, HIGH, CRITICAL
)

# Prepare dataset
train_dataset = TaskDataset(train_df)
eval_dataset = TaskDataset(eval_df)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=8,
    evaluation_strategy="epoch",
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

**Ventajas:**

- ✅ Precisión: 95%+ (vs 90% actual)
- ✅ Adaptado a tu dominio específico
- ✅ Entiende terminología propia

**Desventajas:**

- ⚠️ Requiere datos etiquetados (manual o semi-automático)
- ⚠️ Requiere GPU para entrenar (cloud o local)
- ⚠️ Mantenimiento: reentrenar periódicamente

**Esfuerzo:** 2-4 semanas  
**Impacto:** Muy Alto (mejor precisión, adaptado al negocio)

---

## 🔧 MEJORA 6: A/B Testing de Algoritmos

### Problema Actual

No sabemos qué configuración funciona mejor:

- ¿BART o DistilBERT?
- ¿Con o sin reglas de negocio?
- ¿Umbrales de urgencia óptimos?

### Solución: Experimentos controlados

```python
# apps/tasks/infrastructure/ai/ab_testing.py
import random

class ABTestingEngine(AIService):
    """AI engine with A/B testing."""

    def __init__(self):
        self.engine_a = HuggingFaceEngine()  # Actual
        self.engine_b = OptimizedEngine()    # Nueva versión

    def analyze_task_text(self, text: str) -> Analysis:
        # Assign 50% users to each variant
        variant = 'A' if random.random() < 0.5 else 'B'

        if variant == 'A':
            result = self.engine_a.analyze_task_text(text)
        else:
            result = self.engine_b.analyze_task_text(text)

        # Log for analysis
        self._log_experiment(text, result, variant)

        return result
```

**Métricas a medir:**

- Precisión de predicciones
- Tiempo de respuesta
- Satisfacción de usuario (feedback)
- Tasa de modificación manual

**Esfuerzo:** 1 semana  
**Impacto:** Medio (datos para decisiones basadas en evidencia)

---

## 🔧 MEJORA 7: Batch Processing

### Problema Actual

Analizar 100 tareas = 100 requests a la IA = 20-50 segundos

### Solución: Procesar en batch

```python
class BatchAIEngine(AIService):
    """Process multiple tasks in parallel."""

    def analyze_tasks_batch(self, texts: List[str]) -> List[Analysis]:
        """Analyze multiple texts at once."""
        # Process in batches of 32
        batch_size = 32
        results = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]

            # Parallel inference
            batch_results = self.classifier(batch)
            results.extend(batch_results)

        return [self._parse_result(r) for r in results]
```

**Ventajas:**

- ✅ 100 tareas: 5 segundos (vs 20-50s) → **4-10x más rápido**
- ✅ Útil para re-priorización masiva

**Esfuerzo:** 3 horas  
**Impacto:** Medio (solo útil para operaciones batch)

---

## 📋 Resumen de Mejoras

| Mejora              | Esfuerzo | Impacto    | Prioridad              |
| ------------------- | -------- | ---------- | ---------------------- |
| 1. Business Rules   | 2h       | Alto       | 🔥 **Alta**            |
| 2. Modelos Ligeros  | 1h       | Alto       | 🔥 **Alta**            |
| 3. Redis Cache      | 2h       | Muy Alto   | 🔥 **Alta**            |
| 4. Celery Async     | 4h       | Medio-Alto | 🟡 Media               |
| 5. Fine-tuning      | 2-4 sem  | Muy Alto   | 🟡 Media (largo plazo) |
| 6. A/B Testing      | 1 sem    | Medio      | 🟢 Baja                |
| 7. Batch Processing | 3h       | Medio      | 🟢 Baja                |

---

## 🎯 Plan de Implementación Recomendado

### Fase 1: Quick Wins (1 día)

1. ✅ Implementar Business Rules
2. ✅ Cambiar a modelos ligeros
3. ✅ Añadir Redis cache

**Resultado:** Sistema más rápido y preciso

### Fase 2: Async (2-3 días)

4. ✅ Implementar Celery async
5. ✅ WebSocket para notificaciones (opcional)

**Resultado:** Mejor UX

### Fase 3: Optimización (2-4 semanas)

6. ✅ Recopilar datos de Cherry Core
7. ✅ Fine-tuning con datos reales
8. ✅ A/B testing de configuraciones

**Resultado:** Precisión óptima para tu negocio

---

## 🔍 Monitoreo y Métricas

### KPIs a medir

**Técnicos:**

- Latencia de análisis (p50, p95, p99)
- Tasa de cache hits
- Errores de IA (%)
- Uso de recursos (CPU, RAM)

**Negocio:**

- Precisión de predicciones (vs etiquetado manual)
- Tiempo ahorrado en priorización
- Tasa de modificación manual (%)
- Satisfacción de usuario

### Herramientas

```python
# apps/tasks/infrastructure/ai/monitoring.py
import time
from django.core.cache import cache

class MonitoredAIEngine(AIService):
    """AI engine with monitoring."""

    def analyze_task_text(self, text: str) -> Analysis:
        start_time = time.time()

        try:
            result = super().analyze_task_text(text)

            # Log success
            duration = time.time() - start_time
            self._log_metric('ai.analysis.success', duration)

            return result

        except Exception as e:
            # Log error
            self._log_metric('ai.analysis.error', 1)
            raise
```

---

## 💡 Conclusión

**Mejoras prioritarias para Cherry Core:**

1. 🔥 **Business Rules** - Ajustar a casos de uso específicos
2. 🔥 **Modelos Ligeros** - Mejor rendimiento
3. 🔥 **Redis Cache** - 40-100x más rápido

**Después de integrar:** 4. 🟡 **Fine-tuning** - Con datos reales de Cherry Core 5. 🟡 **Celery Async** - Mejor UX

**Total esfuerzo inicial:** ~1 día de desarrollo  
**Beneficio:** Sistema optimizado y listo para producción

---

**Siguiente paso:** [CHERRY_CORE_INTEGRATION.md](CHERRY_CORE_INTEGRATION.md)

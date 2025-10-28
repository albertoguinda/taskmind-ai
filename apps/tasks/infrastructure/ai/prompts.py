"""
Prompts de IA.

Colección de prompts optimizados para diferentes modelos de IA.
Estos templates se usan cuando se trabaja con modelos basados en prompts
(ej: OpenAI GPT, Claude, etc) en lugar de clasificadores fine-tuned.
"""

# Prompt para análisis de urgencia con modelos generativos
URGENCY_ANALYSIS_PROMPT = """
Analiza la siguiente tarea y determina su nivel de urgencia:

Tarea: {text}

Considera los siguientes factores:
- Keywords que indican urgencia (urgente, crítico, emergencia, ASAP, inmediatamente)
- Impacto (producción, cliente, seguridad, bloqueo)
- Sensibilidad temporal (deadlines, hoy, ahora, esta semana)
- Severidad (caído, roto, fallando, error crítico)

Evalúa la urgencia en una escala de 0.0 (nada urgente) a 1.0 (extremadamente urgente).

Responde únicamente con el número (ej: 0.85).
"""

# Prompt para extracción de keywords con modelos generativos
KEYWORD_EXTRACTION_PROMPT = """
Extrae las keywords más importantes de esta tarea:

Tarea: {text}

Enfócate en:
- Términos técnicos (tecnologías, herramientas, frameworks)
- Verbos de acción (fix, implement, deploy, refactor)
- Conceptos críticos (bug, feature, security, performance)
- Entidades nombradas (productos, servicios, módulos)

Retorna entre 5 y 10 keywords separadas por comas, en minúsculas.
Ejemplo: django, api, production, bug, urgent

Keywords:
"""

# Prompt para análisis de sentimiento con modelos generativos
SENTIMENT_ANALYSIS_PROMPT = """
Analiza el tono emocional de esta tarea:

Tarea: {text}

Determina si el tono es:
- Positivo (constructivo, entusiasta, optimista)
- Neutral (objetivo, descriptivo)
- Negativo (frustrante, preocupante, crítico)

Responde con un número entre -1.0 (muy negativo) y 1.0 (muy positivo).

Responde únicamente con el número (ej: -0.65).
"""

# Prompt completo para análisis multi-aspecto
FULL_ANALYSIS_PROMPT = """
Analiza completamente la siguiente tarea y proporciona:

Tarea: {text}

Retorna un análisis estructurado con:
1. Urgencia (0.0 a 1.0): Qué tan urgente es esta tarea
2. Keywords (5-10): Términos técnicos y conceptos clave
3. Sentimiento (-1.0 a 1.0): Tono emocional del texto
4. Confianza (0.0 a 1.0): Nivel de certeza en el análisis

Formato de respuesta JSON:
{{
  "urgency": 0.85,
  "keywords": ["django", "bug", "production", "api"],
  "sentiment": -0.3,
  "confidence": 0.92
}}
"""


# Mapeo de etiquetas de urgencia en lenguaje natural (para zero-shot)
URGENCY_LABELS_ES = [
    "extremadamente urgente y crítico",
    "alta prioridad e importante",
    "prioridad normal",
    "baja prioridad y no urgente",
]

URGENCY_LABELS_EN = [
    "extremely urgent and critical",
    "high priority and important",
    "normal priority",
    "low priority and not urgent",
]


# Notas de uso:
# --------------
# - Los prompts URGENCY_ANALYSIS_PROMPT y KEYWORD_EXTRACTION_PROMPT están
#   diseñados para modelos generativos (GPT, Claude, Llama)
# - Para modelos fine-tuned (BART, DistilBERT) usados en HuggingFaceEngine,
#   NO se necesitan prompts, ya que están entrenados para tareas específicas
# - FULL_ANALYSIS_PROMPT es útil para implementaciones futuras con LLMs
#   que puedan hacer análisis multi-aspecto en una sola llamada
# - Los URGENCY_LABELS se usan directamente en zero-shot classification
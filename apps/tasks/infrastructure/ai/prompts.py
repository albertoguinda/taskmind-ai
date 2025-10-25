"""
AI Prompts.

Optimized prompts for AI models.
"""

URGENCY_ANALYSIS_PROMPT = """
Analyze the following task and determine its urgency level:

Task: {text}

Consider:
- Keywords indicating urgency (urgent, critical, emergency, ASAP)
- Impact (production, customer-facing, security)
- Time sensitivity (deadlines, today, now)
- Severity (down, broken, failing)

Rate urgency from 0.0 (not urgent) to 1.0 (extremely urgent).
"""

KEYWORD_EXTRACTION_PROMPT = """
Extract the most important keywords from this task:

Task: {text}

Focus on:
- Technical terms
- Action words
- Critical concepts
- Named entities

Return top 5-10 keywords.
"""
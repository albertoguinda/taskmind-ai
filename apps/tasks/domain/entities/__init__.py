"""
Domain Entities.

Entities are objects with identity that persist over time.
"""

from .task import Task
from .analysis import Analysis

__all__ = ["Task", "Analysis"]
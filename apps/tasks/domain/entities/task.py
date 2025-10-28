"""
Entidad Task del Dominio.

Entidad core que representa una tarea en el sistema.
Framework-agnostic: Python puro, sin dependencias de Django.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID, uuid4

from ..value_objects import Priority, Status, UrgencyScore


@dataclass
class Task:
    """
    Entidad de dominio Task (Tarea).
    
    Representa una tarea con toda su lógica de negocio.
    Esta clase es independiente del framework y contiene solo lógica de dominio.
    
    Reglas de Negocio:
    - El título es obligatorio y no puede exceder 200 caracteres
    - La prioridad se deriva automáticamente del urgency_score
    - Las transiciones de estado deben seguir reglas válidas
    - Los timestamps se actualizan automáticamente en cada cambio
    
    Atributos:
        id: Identificador único (UUID v4)
        title: Título de la tarea (obligatorio)
        description: Descripción detallada de la tarea
        priority: Nivel de prioridad (LOW, MEDIUM, HIGH, CRITICAL)
        status: Estado actual (TODO, IN_PROGRESS, DONE, CANCELLED)
        urgency_score: Puntuación de urgencia calculada por IA (0.0-1.0)
        ai_keywords: Keywords extraídos por IA
        created_at: Timestamp de creación (UTC, timezone-aware)
        updated_at: Timestamp de última actualización (UTC, timezone-aware)
    
    Ejemplo:
        >>> task = Task(title="Fix critical bug", description="Production issue")
        >>> task.update_urgency(UrgencyScore(0.95))
        >>> assert task.priority == Priority.CRITICAL
        >>> task.start_work()
        >>> assert task.is_in_progress()
    """
    
    # Campos obligatorios
    title: str
    description: str = ""
    
    # Value objects con valores por defecto
    priority: Priority = Priority.MEDIUM
    status: Status = Status.TODO
    urgency_score: UrgencyScore = field(default_factory=UrgencyScore.default)
    
    # Campos opcionales (generados automáticamente)
    id: UUID = field(default_factory=uuid4)
    ai_keywords: List[str] = field(default_factory=list)
    
    # Timestamps timezone-aware (Python 3.11+)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    
    def __post_init__(self):
        """
        Validación automática después de inicialización.
        Se ejecuta después de __init__ en dataclasses.
        """
        self._validate()
    
    def _validate(self):
        """
        Valida las reglas de negocio de la tarea.
        
        Raises:
            ValueError: Si alguna regla de validación falla
        """
        # Regla 1: El título no puede estar vacío
        if not self.title or not self.title.strip():
            raise ValueError("El título de la tarea no puede estar vacío")
        
        # Regla 2: El título tiene un límite de caracteres
        if len(self.title) > 200:
            raise ValueError("El título no puede exceder 200 caracteres")
        
        # Regla 3: Asegurar que los timestamps sean timezone-aware
        if self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)
        if self.updated_at.tzinfo is None:
            self.updated_at = self.updated_at.replace(tzinfo=timezone.utc)
    
    # ==========================================
    # Métodos de Lógica de Negocio
    # ==========================================
    
    def update_urgency(self, score: UrgencyScore) -> None:
        """
        Actualiza el urgency_score y recalcula la prioridad automáticamente.
        
        Regla de Negocio:
        La prioridad se deriva automáticamente del urgency_score según:
        - 0.0-0.3: LOW
        - 0.3-0.6: MEDIUM
        - 0.6-0.85: HIGH
        - 0.85-1.0: CRITICAL
        
        Args:
            score: Nuevo urgency_score calculado por IA
        
        Ejemplo:
            >>> task.update_urgency(UrgencyScore(0.9))
            >>> assert task.priority == Priority.CRITICAL
        """
        self.urgency_score = score
        self.priority = Priority.from_urgency_score(float(score))
        self._mark_as_updated()
    
    def change_status(self, new_status: Status) -> None:
        """
        Cambia el estado de la tarea con validación de transiciones.
        
        Regla de Negocio:
        Las transiciones de estado deben seguir reglas válidas definidas
        en el value object Status (ej: no se puede ir de DONE a TODO).
        
        Args:
            new_status: Estado destino
        
        Raises:
            ValueError: Si la transición no es válida
        
        Ejemplo:
            >>> task.change_status(Status.IN_PROGRESS)  # OK
            >>> task.change_status(Status.TODO)  # ValueError!
        """
        if not self.status.can_transition_to(new_status):
            raise ValueError(
                f"No se puede transicionar de {self.status.value} "
                f"a {new_status.value}"
            )
        
        self.status = new_status
        self._mark_as_updated()
    
    def start_work(self) -> None:
        """
        Inicia el trabajo en la tarea.
        
        Atajo de negocio para: TODO → IN_PROGRESS
        
        Raises:
            ValueError: Si la tarea no está en estado TODO
        """
        self.change_status(Status.IN_PROGRESS)
    
    def complete(self) -> None:
        """
        Marca la tarea como completada.
        
        Atajo de negocio para: IN_PROGRESS → DONE
        
        Raises:
            ValueError: Si la tarea no está en estado IN_PROGRESS
        """
        self.change_status(Status.DONE)
    
    def cancel(self) -> None:
        """
        Cancela la tarea.
        
        Puede llamarse desde cualquier estado no terminal.
        Una vez cancelada, la tarea no puede reactivarse.
        """
        self.change_status(Status.CANCELLED)
    
    def add_keywords(self, keywords: List[str]) -> None:
        """
        Añade keywords extraídos por IA a la tarea.
        
        Los keywords se limpian automáticamente:
        - Eliminación de duplicados
        - Eliminación de strings vacíos
        - Trim de espacios en blanco
        
        Args:
            keywords: Lista de keywords del análisis de IA
        
        Ejemplo:
            >>> task.add_keywords(["django", "api", "bug", "django"])
            >>> assert task.ai_keywords == ["api", "bug", "django"]  # sin duplicados
        """
        # Limpiar: eliminar duplicados, vacíos y hacer trim
        unique_keywords = list(set(k.strip() for k in keywords if k.strip()))
        self.ai_keywords = sorted(unique_keywords)  # ordenar para consistencia
        self._mark_as_updated()
    
    # ==========================================
    # Métodos de Consulta (Query Methods)
    # ==========================================
    
    def is_urgent(self) -> bool:
        """
        Verifica si la tarea es urgente (urgency_score >= 0.7).
        
        Returns:
            True si es urgente, False en caso contrario
        """
        return self.urgency_score.is_urgent()
    
    def is_critical(self) -> bool:
        """
        Verifica si la tarea es crítica (urgency_score >= 0.85).
        
        Returns:
            True si es crítica, False en caso contrario
        """
        return self.urgency_score.is_critical()
    
    def is_completed(self) -> bool:
        """
        Verifica si la tarea está completada.
        
        Returns:
            True si status == DONE
        """
        return self.status == Status.DONE
    
    def is_in_progress(self) -> bool:
        """
        Verifica si la tarea está en progreso.
        
        Returns:
            True si status == IN_PROGRESS
        """
        return self.status == Status.IN_PROGRESS
    
    def is_cancelled(self) -> bool:
        """
        Verifica si la tarea está cancelada.
        
        Returns:
            True si status == CANCELLED
        """
        return self.status == Status.CANCELLED
    
    # ==========================================
    # Métodos Internos
    # ==========================================
    
    def _mark_as_updated(self) -> None:
        """
        Actualiza el timestamp updated_at al momento actual (UTC).
        Se llama automáticamente en cada operación que modifica la tarea.
        """
        self.updated_at = datetime.now(timezone.utc)
    
    # ==========================================
    # Métodos Dunder (Comparación y Representación)
    # ==========================================
    
    def __eq__(self, other: object) -> bool:
        """
        Dos tareas son iguales si tienen el mismo ID.
        Implementa igualdad por identidad (no por valor).
        """
        if not isinstance(other, Task):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """
        Hash basado en ID para uso en sets/dicts.
        Permite usar Task en estructuras hashables.
        """
        return hash(self.id)
    
    def __str__(self) -> str:
        """
        Representación legible para humanos.
        Usado en logs, debugging casual, prints.
        """
        return f"Task('{self.title}', {self.priority.value}, {self.status.value})"
    
    def __repr__(self) -> str:
        """
        Representación completa para desarrolladores.
        Usado en debugging, REPL, logs técnicos.
        """
        return (
            f"Task(id={self.id}, title='{self.title[:30]}...', "
            f"priority={self.priority.value}, status={self.status.value}, "
            f"urgency_score={float(self.urgency_score):.2f})"
        )
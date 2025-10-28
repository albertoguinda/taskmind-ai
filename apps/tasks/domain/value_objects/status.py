"""
Value Object Status.

Representa el estado actual de una tarea en su ciclo de vida.
"""

from enum import Enum


class Status(str, Enum):
    """
    Estados del workflow de tareas.
    
    Flujo: TODO → IN_PROGRESS → DONE
    """
    
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    CANCELLED = "CANCELLED"
    
    def can_transition_to(self, new_status: "Status") -> bool:
        """
        Verifica si la transición al nuevo estado es válida.
        
        Reglas de negocio:
        - TODO → IN_PROGRESS o CANCELLED
        - IN_PROGRESS → DONE o CANCELLED
        - DONE y CANCELLED son estados terminales (no cambian)
        """
        valid_transitions = {
            Status.TODO: {Status.IN_PROGRESS, Status.CANCELLED},
            Status.IN_PROGRESS: {Status.DONE, Status.CANCELLED},
            Status.DONE: set(),
            Status.CANCELLED: set(),
        }
        
        return new_status in valid_transitions.get(self, set())
    
    def is_terminal(self) -> bool:
        """Verifica si es un estado terminal."""
        return self in {Status.DONE, Status.CANCELLED}
    
    def to_label(self) -> str:
        """Retorna etiqueta en español."""
        labels = {
            Status.TODO: "Por hacer",
            Status.IN_PROGRESS: "En progreso",
            Status.DONE: "Completada",
            Status.CANCELLED: "Cancelada"
        }
        return labels[self]
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"<Status.{self.name}>"
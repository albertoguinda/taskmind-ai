"""
Interfaz del Repositorio de Tareas.

Define el contrato para la persistencia de tareas (puerto/abstracción).
Las implementaciones estarán en la capa de infraestructura.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from ..entities import Task
from ..value_objects import Priority, Status


class TaskRepository(ABC):
    """
    Repositorio abstracto para persistencia de tareas.
    
    Define QUÉ operaciones se pueden hacer, NO cómo se implementan.
    """
    
    @abstractmethod
    def save(self, task: Task) -> Task:
        """Guarda una tarea (create o update)."""
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """Busca tarea por ID. Retorna None si no existe."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Task]:
        """Obtiene todas las tareas."""
        pass
    
    @abstractmethod
    def find_by_status(self, status: Status) -> List[Task]:
        """Busca tareas por estado."""
        pass
    
    @abstractmethod
    def find_by_priority(self, priority: Priority) -> List[Task]:
        """Busca tareas por prioridad."""
        pass
    
    @abstractmethod
    def find_urgent_tasks(self) -> List[Task]:
        """Busca tareas urgentes (urgency >= 0.7), ordenadas por urgencia."""
        pass
    
    @abstractmethod
    def find_by_keyword(self, keyword: str) -> List[Task]:
        """Busca tareas que contengan un keyword."""
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> bool:
        """Elimina una tarea. Retorna True si existía."""
        pass
    
    @abstractmethod
    def exists(self, task_id: UUID) -> bool:
        """Verifica si una tarea existe."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Cuenta el total de tareas."""
        pass
"""
Excepciones de Dominio.

Excepciones personalizadas para errores específicos del dominio.
"""


class DomainException(Exception):
    """Excepción base para todos los errores de dominio."""
    pass


class TaskNotFoundException(DomainException):
    """Se lanza cuando una tarea no se encuentra."""
    
    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(f"Tarea con ID {task_id} no encontrada")


class InvalidTaskStateException(DomainException):
    """Se lanza cuando una operación es inválida para el estado actual."""
    
    def __init__(self, message: str):
        super().__init__(message)


class InvalidPriorityException(DomainException):
    """Se lanza cuando se proporciona una prioridad inválida."""
    
    def __init__(self, priority: str):
        super().__init__(f"Prioridad inválida: {priority}")


class InvalidStatusException(DomainException):
    """Se lanza cuando se proporciona un estado inválido."""
    
    def __init__(self, status: str):
        super().__init__(f"Estado inválido: {status}")


class InvalidStatusTransitionException(DomainException):
    """Se lanza cuando una transición de estado no está permitida."""
    
    def __init__(self, from_status: str, to_status: str):
        super().__init__(f"No se puede transicionar de {from_status} a {to_status}")


class ValidationException(DomainException):
    """Se lanza cuando falla la validación de dominio."""
    
    def __init__(self, message: str):
        super().__init__(message)
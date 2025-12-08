# src/exceptions.py - CORREGIDO

class AppException(Exception):
    """Base exception para errores de la capa de aplicación (HTTP/infraestructura)."""
    def __init__(self, detail: str, status_code: int = 500):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)

class DomainException(Exception):
    """Base exception para reglas de negocio."""
    pass

class NotFoundException(DomainException):
    """Cuando no se encuentra un recurso (cliente, mascota, cita)."""
    pass

class ValidationException(DomainException):
    """Cuando los datos de entrada no cumplen validaciones."""
    pass

class RepositoryException(DomainException):
    """Errores a nivel de persistencia (DB)."""
    pass
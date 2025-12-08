from abc import ABC, abstractmethod

class ILogger(ABC):
    """Interfaz para el sistema de logging (DIP)."""
    
    @abstractmethod
    def info(self, message: str): ...

    @abstractmethod
    def warning(self, message: str): ...

    @abstractmethod
    def error(self, message: str, exception: Exception = None): ...
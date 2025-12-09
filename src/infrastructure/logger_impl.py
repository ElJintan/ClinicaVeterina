import logging
from src.interfaces.logger import ILogger
from src.config.logging_config import get_logger

class LoggerImpl(ILogger):
    """
    Implementación concreta de ILogger (DIP) usando el sistema de logging estándar.
    """
    def __init__(self, name: str):
        self._logger = get_logger(name) 

    def info(self, message: str):
        self._logger.info(message)

    def warning(self, message: str):
        self._logger.warning(message)

    def error(self, message: str, exception: Exception = None):
        if exception:
            self._logger.error(message, exc_info=exception) 
        else:
            self._logger.error(message)

    # 💡 FIX: Implementación del método exception()
    def exception(self, message: str):
        self._logger.exception(message)
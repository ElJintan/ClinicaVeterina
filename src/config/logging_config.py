# src/config/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Optional

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Asegurarse de que exista el directorio
os.makedirs(LOG_DIR, exist_ok=True)

def configure_root_logger(level: int = logging.INFO, logfile: Optional[str] = None):
    """Configura el logger root con RotatingFileHandler + StreamHandler."""
    logger = logging.getLogger()
    if logger.handlers:
        # ya configurado (evitar doble configuración)
        return logger

    logger.setLevel(level)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler rotativo
    file_path = logfile or LOG_FILE
    fh = RotatingFileHandler(file_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
    fh.setLevel(level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger

# helper para obtener logger por módulo
def get_logger(name: str = __name__):
    configure_root_logger()
    return logging.getLogger(name)

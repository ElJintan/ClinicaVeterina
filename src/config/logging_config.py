# src/config/logging_config.py

import logging
from typing import Optional

def configure_root_logger(level: int = logging.INFO):
    """Configura el logger root para que imprima en la consola (stdout)."""
    logger = logging.getLogger()
    
    # Previene que se configure dos veces
    if logger.handlers:
        return logger

    logger.setLevel(level)

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler (StreamHandler)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger

# helper para obtener logger por módulo
def get_logger(name: str = __name__):
    configure_root_logger()
    return logging.getLogger(name)
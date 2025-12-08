import logging
from src.interfaces.logger import ILogger

class StandardLogger(ILogger):
    def __init__(self):
        # Configuración básica (podría ir a un archivo de config)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='app.log', # Guardar en archivo para persistencia
            filemode='a'
        )
        self.logger = logging.getLogger("VetCare")

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str, exception: Exception = None):
        if exception:
            self.logger.error(f"{message} | Excepción: {str(exception)}")
        else:
            self.logger.error(message)
import pytest
import asyncio
from unittest.mock import MagicMock
from src.domain.models import Client
from src.services.client_service import ClientService
from src.interfaces.logger import ILogger

# Mock del Repositorio
class MockRepo:
    async def create(self, client): return '12345'
    async def list(self): return []
    async def get(self, id): return None

# Test: Verificar que se llama al logger correctamente
def test_client_creation_logs_info():
    # 1. Arrange (Preparar)
    repo = MockRepo()
    mock_logger = MagicMock(spec=ILogger) # Mock de la interfaz ILogger
    svc = ClientService(repo, mock_logger)
    client = Client(name='Test', email='test@example.com')

    # 2. Act (Ejecutar)
    loop = asyncio.new_event_loop()
    loop.run_until_complete(svc.create_client(client))
    loop.close()

    # 3. Assert (Verificar)
    # Verificamos que se llamó a info() al menos una vez (entrada y éxito)
    assert mock_logger.info.call_count >= 2
    mock_logger.error.assert_not_called()

def test_client_creation_logs_error_on_exception():
    # 1. Arrange
    repo = MockRepo()
    mock_logger = MagicMock(spec=ILogger)
    svc = ClientService(repo, mock_logger)
    # Email vacío para forzar error
    client = Client(name='Test', email='') 

    # 2. Act & Assert
    loop = asyncio.new_event_loop()
    with pytest.raises(ValueError):
        loop.run_until_complete(svc.create_client(client))
    loop.close()

    # Verificamos que se llamó a warning (nuestra lógica para errores de validación)
    mock_logger.warning.assert_called_once()
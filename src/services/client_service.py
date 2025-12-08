# src/services/client_service.py
from typing import List, Optional
from src.interfaces.repositories import IClientRepository
from src.interfaces.logger import ILogger 
from src.domain.models import Client, ClientCreate 
from src.exceptions import NotFoundException, ValidationException, RepositoryException
from src.infrastructure.logger_impl import LoggerImpl 

class ClientService:
    def __init__(self, repo: IClientRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_client(self, client_data: ClientCreate) -> Client:
        self.logger.info(f"Intento de registro de cliente: {client_data.email}")
        try:
            if not client_data.email:
                raise ValueError('El email es obligatorio')

            client_model = Client(**client_data.dict())
            
            client_id = await self.repo.create(client_model)
            new_client = await self.repo.get(client_id)
            
            if not new_client:
                raise RepositoryException("Cliente creado pero falló al recuperar.")

            self.logger.info(f"Cliente registrado con éxito. ID: {client_id}")
            return new_client

        except ValueError as ve:
            self.logger.warning(f"Error de validación: {str(ve)}")
            raise ValidationException(str(ve)) 

        except Exception as e:
            self.logger.error("Error crítico en base de datos al crear cliente", e)
            raise RepositoryException("Error interno del servidor al crear cliente") from e

    async def list_clients(self) -> List[Client]:
        self.logger.info("Consultando lista de clientes")
        return await self.repo.list()

    async def get_client(self, client_id: str) -> Optional[Client]:
        self.logger.debug(f"Buscando cliente por ID: {client_id}")
        client = await self.repo.get(client_id)
        return client
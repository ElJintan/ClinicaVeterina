# src/services/client_service.py - CÓDIGO COMPLETO Y FINAL
from typing import List, Optional
from src.interfaces.repositories import IClientRepository
from src.interfaces.logger import ILogger 
from src.domain.models import Client, ClientCreate, ClientUpdate 
from src.exceptions import NotFoundException, ValidationException, RepositoryException
from src.infrastructure.logger_impl import LoggerImpl 

class ClientService:
    def __init__(self, repo: IClientRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_client(self, client_data: ClientCreate) -> Client:
        try:
            client_model = Client(**client_data.dict())
            client_id = await self.repo.create(client_model)
            new_client = await self.repo.get(client_id)
            if not new_client:
                raise RepositoryException("Cliente creado pero falló al recuperar.")
            self.logger.info(f"Cliente registrado con éxito. ID: {client_id}")
            return new_client
        except Exception as e:
            self.logger.exception("Error creando cliente")
            raise RepositoryException("Error interno del servidor al crear cliente") from e

    async def list_clients(self) -> List[Client]:
        self.logger.info("Consultando lista de clientes")
        return await self.repo.list()

    async def get_client(self, client_id: str) -> Optional[Client]:
        self.logger.debug(f"Buscando cliente por ID: {client_id}")
        return await self.repo.get(client_id)
    
    # NUEVO: Implementación de UPDATE
    async def update_client(self, client_id: str, updates: ClientUpdate) -> Optional[Client]:
        self.logger.info(f"Actualizando cliente ID: {client_id}")
        updates_dict = updates.dict(exclude_none=True)
        if not updates_dict:
            return await self.get_client(client_id) # No hay nada que actualizar
        
        updated_client = await self.repo.update(client_id, updates_dict)
        if not updated_client:
            raise NotFoundException(f"Cliente {client_id} no encontrado o no se pudo actualizar.")
        return updated_client

    # NUEVO: Implementación de DELETE
    async def delete_client(self, client_id: str) -> bool:
        self.logger.warning(f"Eliminando cliente ID: {client_id}")
        # Consideración de integridad: Debería verificar si tiene mascotas asociadas.
        return await self.repo.delete(client_id)
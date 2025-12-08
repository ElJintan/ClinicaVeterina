from typing import List
from src.interfaces.repositories import IPetRepository
from src.domain.models import Pet

class PetService:
    def __init__(self, repo: IPetRepository):
        self.repo = repo

    async def register_pet(self, pet: Pet) -> str:
        return await self.repo.create(pet)

    async def get_pets_by_owner(self, owner_id: str) -> List[Pet]:
        return await self.repo.list_by_owner(owner_id)

# src/services/client_service.py
from src.infrastructure.logger_impl import LoggerImpl
from src.exceptions import NotFoundException, RepositoryException

class ClientService:
    def __init__(self, repo, logger=None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    def get_client(self, client_id: str):
        self.logger.debug(f"get_client - id={client_id}")
        client = self.repo.find_by_id(client_id)
        if not client:
            self.logger.warning(f"Client not found: {client_id}")
            raise NotFoundException(f"Cliente {client_id} no encontrado")
        self.logger.info(f"Cliente recuperado: {client_id}")
        return client

    def create_client(self, data: dict):
        try:
            self.logger.debug("create_client - data keys: %s", list(data.keys()))
            # validaciones...
            new = self.repo.create(data)
            self.logger.info(f"Cliente creado id={new.get('id')}")
            return new
        except Exception as e:
            self.logger.exception("Error creando cliente")
            raise RepositoryException("Error al crear cliente")

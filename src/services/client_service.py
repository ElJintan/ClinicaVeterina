from typing import List, Optional
from src.interfaces.repositories import IClientRepository
from src.domain.models import Client

class ClientService:
    def __init__(self, repo: IClientRepository):
        self.repo = repo

    async def create_client(self, client: Client) -> str:
        # Validación simple: email obligatorio
        if not client.email:
            raise ValueError('Email es obligatorio')
        return await self.repo.create(client)

    async def list_clients(self) -> List[Client]:
        return await self.repo.list()

    async def get_client(self, client_id: str) -> Optional[Client]:
        return await self.repo.get(client_id)

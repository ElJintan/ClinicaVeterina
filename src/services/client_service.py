from typing import List, Optional
from src.interfaces.repositories import IClientRepository
from src.interfaces.logger import ILogger #
from src.domain.models import Client

class ClientService:
    # Inyección de dependencias: Repo + Logger
    def __init__(self, repo: IClientRepository, logger: ILogger):
        self.repo = repo
        self.logger = logger

    async def create_client(self, client: Client) -> str:
        self.logger.info(f"Intento de registro de cliente: {client.email}")
        try:
            # Validación de negocio
            if not client.email:
                raise ValueError('El email es obligatorio')
            
            # Persistencia
            client_id = await self.repo.create(client)
            self.logger.info(f"Cliente registrado con éxito. ID: {client_id}")
            return client_id

        except ValueError as ve:
            self.logger.warning(f"Error de validación: {str(ve)}")
            raise ve # Re-lanzamos para que el controller informe al front
        except Exception as e:
            self.logger.error("Error crítico en base de datos al crear cliente", e)
            raise RuntimeError("Error interno del servidor") from e

    async def list_clients(self) -> List[Client]:
        self.logger.info("Consultando lista de clientes")
        return await self.repo.list()

    async def get_client(self, client_id: str) -> Optional[Client]:
        return await self.repo.get(client_id)
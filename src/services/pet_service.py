# src/services/pet_service.py
from typing import List, Optional
from src.interfaces.repositories import IPetRepository
from src.interfaces.logger import ILogger
from src.domain.models import Pet, PetCreate # Asumimos PetCreate
from src.infrastructure.logger_impl import LoggerImpl
from src.exceptions import NotFoundException, ValidationException # Importar excepciones

class PetService:
    def __init__(self, repo: IPetRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_pet(self, pet_data: PetCreate) -> Pet:
        self.logger.info(f"Intento de registro de mascota: {pet_data.name}")
        pet_model = Pet(**pet_data.dict())
        pet_id = await self.repo.create(pet_model)
        
        # Nota: Asumimos que podemos construir el objeto de retorno con el ID
        return Pet(id=pet_id, **pet_data.dict()) 

    async def list_pets(self) -> List[Pet]:
        self.logger.info("Consultando lista de todas las mascotas")
        return await self.repo.list()

    async def list_pets_by_owner(self, owner_id: str) -> List[Pet]:
        self.logger.info(f"Consultando mascotas para el dueño: {owner_id}")
        return await self.repo.list_by_owner(owner_id)

    async def get_pet(self, pet_id: str) -> Optional[Pet]:
        # Si tienes este método en el repositorio, se utiliza aquí.
        # Asumimos que IPetRepository tiene un método get(pet_id)
        # return await self.repo.get(pet_id) 
        return None # Placeholder, debes implementarlo si lo necesitas
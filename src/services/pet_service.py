# src/services/pet_service.py - CÓDIGO COMPLETO CON VALIDACIÓN DE FOREIGN KEY
from typing import List, Optional
from src.interfaces.repositories import IPetRepository, IClientRepository # Importamos IClientRepository
from src.interfaces.logger import ILogger 
from src.domain.models import Pet, PetCreate, PetUpdate 
from src.exceptions import NotFoundException, ValidationException, RepositoryException
from src.infrastructure.logger_impl import LoggerImpl 

class PetService:
    # 💡 DIP: Inyectamos ambos repositorios: PetRepository para CRUD de Pet, ClientRepository para validación.
    def __init__(self, pet_repo: IPetRepository, client_repo: IClientRepository, logger: ILogger = None):
        self.pet_repo = pet_repo
        self.client_repo = client_repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_pet(self, pet_data: PetCreate) -> Pet:
        self.logger.info(f"Iniciando registro de mascota para owner_id: {pet_data.owner_id}")
        try:
            # 📌 Lógica de Validación de Integridad (Foreign Key Check)
            owner_exists = await self.client_repo.get(pet_data.owner_id)
            if not owner_exists:
                raise NotFoundException(f"El Cliente con ID '{pet_data.owner_id}' (owner_id) no existe. No se puede crear la mascota.")
            
            pet_model = Pet(**pet_data.dict())
            pet_id = await self.pet_repo.create(pet_model)
            new_pet = await self.pet_repo.get(pet_id)
            
            if not new_pet:
                raise RepositoryException("Mascota creada pero falló al recuperar.")
            
            self.logger.info(f"Mascota registrada con éxito. ID: {pet_id}")
            return new_pet
        except NotFoundException:
            # Propagamos el error específico de no encontrado para el controlador
            raise
        except Exception as e:
            self.logger.exception("Error creando mascota")
            raise RepositoryException("Error interno del servidor al crear mascota") from e


    async def list_pets(self) -> List[Pet]:
        self.logger.info("Consultando lista de mascotas")
        return await self.pet_repo.list()

    async def list_pets_by_owner(self, owner_id: str) -> List[Pet]:
        self.logger.debug(f"Buscando mascotas por owner_id: {owner_id}")
        return await self.pet_repo.list_by_owner(owner_id)
    
    async def get_pet(self, pet_id: str) -> Optional[Pet]:
        self.logger.debug(f"Buscando mascota por ID: {pet_id}")
        return await self.pet_repo.get(pet_id)
    
    # Resto de métodos CRUD para la mascota (update, delete)
    async def update_pet(self, pet_id: str, updates: PetUpdate) -> Optional[Pet]:
        self.logger.info(f"Actualizando mascota ID: {pet_id}")
        updates_dict = updates.dict(exclude_none=True)
        if not updates_dict:
            return await self.get_pet(pet_id)
        
        updated_pet = await self.pet_repo.update(pet_id, updates_dict)
        if not updated_pet:
            raise NotFoundException(f"Mascota {pet_id} no encontrada o no se pudo actualizar.")
        return updated_pet

    async def delete_pet(self, pet_id: str) -> bool:
        self.logger.warning(f"Eliminando mascota ID: {pet_id}")
        return await self.pet_repo.delete(pet_id)
# src/services/pet_service.py - CÓDIGO MODIFICADO
from typing import List, Optional
from src.interfaces.repositories import IPetRepository
from src.interfaces.logger import ILogger 
from src.domain.models import Pet, PetCreate, PetUpdate 
from src.exceptions import NotFoundException, RepositoryException
from src.infrastructure.logger_impl import LoggerImpl 

class PetService:
    # 💡 FIX: Solo inyectamos PetRepository
    def __init__(self, pet_repo: IPetRepository, logger: ILogger = None):
        self.pet_repo = pet_repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_pet(self, pet_data: PetCreate) -> Pet:
        # Cambio: Se elimina la referencia a pet_data.owner_name
        self.logger.info(f"Iniciando registro de mascota: {pet_data.name}") 
        try:
            # ELIMINADO: Lógica de Validación de Integridad (Foreign Key Check)
            
            pet_id = await self.pet_repo.create(pet_data) 
            new_pet = await self.pet_repo.get(pet_id)
            
            if not new_pet:
                raise RepositoryException("Mascota creada pero falló al recuperar.")
            
            self.logger.info(f"Mascota registrada con éxito. ID: {pet_id}")
            return new_pet
        except Exception as e:
            self.logger.exception("Error creando mascota")
            raise RepositoryException("Error interno del servidor al crear mascota") from e


    async def list_pets(self) -> List[Pet]:
        self.logger.info("Consultando lista de mascotas")
        return await self.pet_repo.list()

    # ELIMINADO: list_pets_by_owner ya no existe
    # async def list_pets_by_owner(self, owner_id: str) -> List[Pet]:
    #     pass
    
    async def get_pet(self, pet_id: str) -> Optional[Pet]:
        self.logger.debug(f"Buscando mascota por ID: {pet_id}")
        return await self.pet_repo.get(pet_id)
    
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
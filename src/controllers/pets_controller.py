# src/controllers/pets_controller.py - CORREGIDO
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional 

from src.domain.models import Pet, PetCreate
from src.services.pet_service import PetService
from src.exceptions import NotFoundException, ValidationException, RepositoryException
from src.repositories.mongo_repo import MongoPetRepository 
from src.infrastructure.logger_impl import LoggerImpl 

router = APIRouter()

# FIX: Función de inyección de dependencia que crea el servicio con sus dependencias
def get_pet_service() -> PetService:
    repo = MongoPetRepository()
    logger = LoggerImpl(PetService.__name__)
    return PetService(repo=repo, logger=logger) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Pet)
async def create_pet_endpoint(
    pet_create: PetCreate,
    pet_service: PetService = Depends(get_pet_service)
):
    """Crea una nueva mascota."""
    try:
        pet = await pet_service.create_pet(pet_create)
        return pet
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# FIX: Endpoint único para listado general y por dueño
@router.get("/", response_model=List[Pet])
async def list_pets_endpoint(
    owner_id: Optional[str] = None, 
    pet_service: PetService = Depends(get_pet_service)
):
    """Obtiene la lista completa de mascotas o mascotas por dueño."""
    if owner_id:
        return await pet_service.list_pets_by_owner(owner_id)
    
    return await pet_service.list_pets()
# src/controllers/pets_controller.py - SIN FILTRADO POR DUEÑO
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional 

from src.domain.models import Pet, PetCreate, PetUpdate
from src.services.pet_service import PetService
from src.exceptions import NotFoundException, ValidationException, RepositoryException
from src.repositories.mongo_repo import MongoPetRepository 
from src.infrastructure.logger_impl import LoggerImpl 

router = APIRouter()

def get_pet_service() -> PetService:
    # 💡 FIX: Solo inyectamos MongoPetRepository
    pet_repo = MongoPetRepository()
    logger = LoggerImpl(PetService.__name__)
    # Pasamos None para client_repo, ya que PetService ha sido actualizado
    return PetService(pet_repo=pet_repo, logger=logger) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Pet)
async def create_pet_endpoint(
    pet_create: PetCreate,
    pet_service: PetService = Depends(get_pet_service)
):
    """Crea una nueva mascota (ya no requiere owner_id válido)."""
    try:
        pet = await pet_service.create_pet(pet_create)
        return pet
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=List[Pet])
async def list_pets_endpoint(
    # ELIMINADO: owner_id: Optional[str] = None, 
    pet_service: PetService = Depends(get_pet_service)
):
    """Obtiene la lista completa de mascotas."""
    # ELIMINADO: Lógica de filtrado
    return await pet_service.list_pets()

@router.get("/{pet_id}", response_model=Pet)
async def get_pet_endpoint(pet_id: str, pet_service: PetService = Depends(get_pet_service)):
    pet = await pet_service.get_pet(pet_id)
    if not pet: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada.")
    return pet

@router.put("/{pet_id}", response_model=Pet)
async def update_pet_endpoint(
    pet_id: str,
    updates: PetUpdate,
    pet_service: PetService = Depends(get_pet_service)
):
    try:
        pet = await pet_service.update_pet(pet_id, updates)
        return pet
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pet_endpoint(pet_id: str, pet_service: PetService = Depends(get_pet_service)):
    success = await pet_service.delete_pet(pet_id)
    if not success: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mascota no encontrada o no se pudo eliminar.")
    return
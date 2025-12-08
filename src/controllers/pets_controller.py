from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional # Importar Optional para el parámetro de consulta

from src.domain.models import Pet, PetCreate
from src.services.pet_service import PetService
from src.exceptions import NotFoundException, ValidationException

router = APIRouter()

# Inyección de dependencia (PetService)
def get_pet_service() -> PetService:
    # Esto asume que PetService puede ser instanciado aquí
    return PetService()

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

# ENDPOINT CORREGIDO: Maneja GET /pets y GET /pets?owner_id={id}
@router.get("/", response_model=List[Pet])
async def list_pets_endpoint(
    owner_id: Optional[str] = None, # Parámetro de consulta opcional para filtrar
    pet_service: PetService = Depends(get_pet_service)
):
    """Obtiene la lista completa de mascotas o mascotas por dueño."""
    # Principio de Sustitución de Liskov: Si se proporciona un owner_id, 
    # se usa el método de filtrado. Si no, se usa el método de listado general.
    if owner_id:
        return await pet_service.list_pets_by_owner(owner_id)
    
    # Asume que PetService tiene un método list_pets() que retorna todas las mascotas.
    return await pet_service.list_pets() 

@router.get("/{pet_id}", response_model=Pet)
async def get_pet_endpoint(
    pet_id: str,
    pet_service: PetService = Depends(get_pet_service)
):
    """Obtiene una mascota por ID."""
    try:
        pet = await pet_service.get_pet(pet_id)
        if not pet:
            raise NotFoundException(f"Mascota con ID {pet_id} no encontrada.")
        return pet
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# Si tu servicio de mascotas ya tiene un endpoint /owner/{owner_id} definido, 
# debes asegurarte de que el list_pets_endpoint anterior lo maneje como query param 
# para evitar ambigüedad de rutas. El código de arriba resuelve ambas necesidades.
from fastapi import APIRouter, Depends
from src.domain.models import Pet
from src.services.pet_service import PetService
from src.repositories.mongo_repo import MongoPetRepository

router = APIRouter()

def get_pet_service():
    repo = MongoPetRepository()
    return PetService(repo)

@router.post('/', response_model=Pet)
async def create_pet(payload: Pet, svc: PetService = Depends(get_pet_service)):
    pet_id = await svc.register_pet(payload)
    return {**payload.dict(), 'id': pet_id}

@router.get('/owner/{owner_id}', response_model=list[Pet])
async def pets_by_owner(owner_id: str, svc: PetService = Depends(get_pet_service)):
    return await svc.get_pets_by_owner(owner_id)

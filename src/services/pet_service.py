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

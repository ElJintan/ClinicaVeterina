from src.interfaces.repositories import IMedicalRepository, IPetRepository
from src.domain.models import MedicalRecord
from src.exceptions import NotFoundException

class MedicalService:
    def __init__(self, medical_repo: IMedicalRepository, pet_repo: IPetRepository):
        self.medical_repo = medical_repo
        self.pet_repo = pet_repo

    async def add_diagnosis(self, pet_id: str, diagnosis: str, treatment: str, medication: str = None) -> str:
        # Validación: Mascota debe existir
        pet = await self.pet_repo.get_by_id(pet_id)
        if not pet:
            raise NotFoundException(f"No existe mascota con ID {pet_id}")
        
        record = MedicalRecord(
            pet_id=pet_id,
            diagnosis=diagnosis,
            treatment=treatment,
            medication=medication
        )
        return await self.medical_repo.add_entry(record)

    async def get_pet_history(self, pet_id: str):
        return await self.medical_repo.get_history(pet_id)
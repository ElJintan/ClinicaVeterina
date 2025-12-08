# src/services/medical_service.py - CÓDIGO COMPLETO Y FINAL (NUEVO)
from typing import List, Optional
from src.interfaces.repositories import IMedicalRecordRepository
from src.interfaces.logger import ILogger
from src.domain.models import MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate
from src.infrastructure.logger_impl import LoggerImpl

class MedicalService:
    def __init__(self, repo: IMedicalRecordRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_record(self, record_data: MedicalRecordCreate) -> MedicalRecord:
        self.logger.info(f"Creando registro médico para mascota: {record_data.pet_id}")
        record_model = MedicalRecord(**record_data.dict())
        record_id = await self.repo.create(record_model)
        # Asumimos que recuperamos el objeto completo para el retorno (con ID y fecha)
        return await self.repo.get(record_id)

    async def list_all_records(self) -> List[MedicalRecord]:
        self.logger.info("Consultando todos los historiales médicos.")
        return await self.repo.list()

    async def list_records_by_pet(self, pet_id: str) -> List[MedicalRecord]:
        self.logger.info(f"Consultando historial para mascota: {pet_id}")
        return await self.repo.list_by_pet(pet_id)

    async def update_record(self, record_id: str, updates: MedicalRecordUpdate) -> Optional[MedicalRecord]:
        updates_dict = updates.dict(exclude_none=True)
        if not updates_dict: return await self.repo.get(record_id)
        return await self.repo.update(record_id, updates_dict)

    async def delete_record(self, record_id: str) -> bool:
        return await self.repo.delete(record_id)
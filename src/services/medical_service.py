# src/services/medical_service.py - CÓDIGO MODIFICADO (SOLID)
from typing import List, Optional
from src.interfaces.repositories import IMedicalRecordRepository # DIP: Dependencia de Abstracción
from src.interfaces.logger import ILogger
from src.domain.models import MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate
from src.infrastructure.logger_impl import LoggerImpl

class MedicalService:
    def __init__(self, repo: IMedicalRecordRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_record(self, record_data: MedicalRecordCreate) -> MedicalRecord:
        # Manejamos si pet_id es None para el log (Desacoplamiento)
        pet_info = record_data.pet_id if record_data.pet_id else "Sin Mascota" 
        self.logger.info(f"Creando registro médico para mascota: {pet_info}")
        record_model = MedicalRecord(**record_data.dict())
        record_id = await self.repo.create(record_model)
        return await self.repo.get(record_id)

    async def list_all_records(self) -> List[MedicalRecord]:
        self.logger.info("Consultando todos los historiales médicos.")
        return await self.repo.list()

    # Mantenemos este método para la funcionalidad de consulta (es el SRP del MedicalService)
    async def list_records_by_pet(self, pet_id: str) -> List[MedicalRecord]:
        self.logger.info(f"Consultando historial para mascota: {pet_id}")
        return await self.repo.list_by_pet(pet_id) # Usa el método del IMedicalRecordRepository (LSP)

    async def update_record(self, record_id: str, updates: MedicalRecordUpdate) -> Optional[MedicalRecord]:
        updates_dict = updates.dict(exclude_none=True)
        if not updates_dict: return await self.repo.get(record_id)
        return await self.repo.update(record_id, updates_dict)

    async def delete_record(self, record_id: str) -> bool:
        return await self.repo.delete(record_id)
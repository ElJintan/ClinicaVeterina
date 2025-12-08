# src/controllers/medical_records_controller.py - SIN FILTRADO POR MASCOTA
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
from src.domain.models import MedicalRecord, MedicalRecordCreate, MedicalRecordUpdate
from src.services.medical_service import MedicalService
from src.exceptions import NotFoundException
from src.repositories.mongo_repo import MongoMedicalRecordRepository
from src.infrastructure.logger_impl import LoggerImpl

router = APIRouter()

def get_medical_service() -> MedicalService:
    repo = MongoMedicalRecordRepository()
    logger = LoggerImpl(MedicalService.__name__)
    return MedicalService(repo=repo, logger=logger)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MedicalRecord)
async def create_medical_record_endpoint(record_create: MedicalRecordCreate, svc: MedicalService = Depends(get_medical_service)):
    try:
        record = await svc.create_record(record_create)
        return record
    except Exception as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[MedicalRecord])
async def list_medical_records_endpoint(
    # ELIMINADO: pet_id: Optional[str] = None, 
    svc: MedicalService = Depends(get_medical_service)
):
    """Lista todos los registros."""
    # ELIMINADO: Lógica de filtrado
    return await svc.list_all_records()

@router.get("/{record_id}", response_model=MedicalRecord)
async def get_medical_record_endpoint(record_id: str, svc: MedicalService = Depends(get_medical_service)):
    record = await svc.get_record(record_id)
    if not record: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado.")
    return record

@router.put("/{record_id}", response_model=MedicalRecord)
async def update_medical_record_endpoint(
    record_id: str, 
    updates: MedicalRecordUpdate, 
    svc: MedicalService = Depends(get_medical_service)
):
    try:
        record = await svc.update_record(record_id, updates)
        return record
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medical_record_endpoint(record_id: str, svc: MedicalService = Depends(get_medical_service)):
    success = await svc.delete_record(record_id)
    if not success: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado o no se pudo eliminar.")
    return
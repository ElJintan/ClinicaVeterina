# src/controllers/appointments_controller.py - CORREGIDO
from fastapi import APIRouter, Depends, HTTPException, status
from src.domain.models import Appointment, AppointmentCreate # Asumimos AppointmentCreate
from src.services.appointment_service import AppointmentService
from src.repositories.mongo_repo import MongoAppointmentRepository
from src.infrastructure.logger_impl import LoggerImpl 

router = APIRouter()

# FIX: Inyección de Dependencias
def get_appointment_service() -> AppointmentService:
    repo = MongoAppointmentRepository()
    logger = LoggerImpl(AppointmentService.__name__)
    return AppointmentService(repo=repo, logger=logger)

@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    payload: AppointmentCreate, 
    svc: AppointmentService = Depends(get_appointment_service)
):
    try:
        appointment = await svc.create_appointment(payload) 
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    return appointment
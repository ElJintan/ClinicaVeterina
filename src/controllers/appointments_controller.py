from fastapi import APIRouter, Depends, HTTPException
from src.domain.models import Appointment
from src.services.appointment_service import AppointmentService
from src.repositories.mongo_repo import MongoAppointmentRepository

router = APIRouter()

def get_appointment_service():
    repo = MongoAppointmentRepository()
    return AppointmentService(repo)

@router.post('/', response_model=Appointment)
async def create_appointment(payload: Appointment, svc: AppointmentService = Depends(get_appointment_service)):
    try:
        appointment_id = await svc.schedule(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {**payload.dict(), 'id': appointment_id}

# src/services/appointment_service.py
from typing import List
from src.interfaces.repositories import IAppointmentRepository
from src.interfaces.logger import ILogger
from src.domain.models import Appointment, AppointmentCreate
from src.infrastructure.logger_impl import LoggerImpl

class AppointmentService:
    def __init__(self, repo: IAppointmentRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        self.logger.info(f"Scheduling appointment for pet: {appointment_data.pet_id} at {appointment_data.date_time}")
        
        appointment_model = Appointment(**appointment_data.dict())
        appointment_id = await self.repo.create(appointment_model)
        
        return Appointment(id=appointment_id, **appointment_data.dict())

    async def schedule(self, payload):
        # Alias para compatibilidad
        return await self.create_appointment(payload)
# src/services/appointment_service.py - CÓDIGO MODIFICADO (SOLID)
from typing import List
from src.interfaces.repositories import IAppointmentRepository
from src.interfaces.logger import ILogger
from src.domain.models import Appointment, AppointmentCreate
from src.infrastructure.logger_impl import LoggerImpl

class AppointmentService:
    def __init__(self, repo: IAppointmentRepository, logger: ILogger = None): # DIP: Dependencia de Abstracción
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        # Manejamos si pet_id es None para el log (Desacoplamiento)
        pet_info = appointment_data.pet_id if appointment_data.pet_id else "Sin Mascota"
        self.logger.info(f"Scheduling appointment for pet: {pet_info} at {appointment_data.date_time}")
        
        # El modelo de cita se crea directamente sin validación de ID de mascota.
        appointment_model = Appointment(**appointment_data.dict())
        appointment_id = await self.repo.create(appointment_model)
        
        return Appointment(id=appointment_id, **appointment_data.dict())

    async def schedule(self, payload):
        return await self.create_appointment(payload)
# src/services/appointment_service.py
from src.interfaces.repositories import IAppointmentRepository
from src.interfaces.logger import ILogger
from src.domain.models import Appointment, AppointmentCreate
from src.infrastructure.logger_impl import LoggerImpl

class AppointmentService:
    def __init__(self, repo: IAppointmentRepository, logger: ILogger = None): 
        # DIP: Dependencia de Abstracción (IAppointmentRepository), no de la implementación concreta
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_appointment(self, appointment_data: AppointmentCreate) -> Appointment:
        pet_info = appointment_data.pet_id if appointment_data.pet_id else "Sin Mascota"
        self.logger.info(f"Programando cita para mascota: {pet_info} el {appointment_data.date_time}")
        
        # 1. Pasamos el DTO (AppointmentCreate) al repositorio
        appointment_id = await self.repo.create(appointment_data)
        
        # 2. Recuperamos la entidad completa creada (o la construimos para retornar)
        # Es buena práctica recuperar lo que se guardó o construir el objeto de retorno con el ID generado
        return Appointment(id=appointment_id, **appointment_data.dict())

    async def schedule(self, payload: AppointmentCreate) -> Appointment:
        return await self.create_appointment(payload)
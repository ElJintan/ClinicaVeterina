from typing import List
from src.interfaces.repositories import IAppointmentRepository
from src.domain.models import Appointment
from datetime import datetime

class AppointmentService:
    def __init__(self, repo: IAppointmentRepository):
        self.repo = repo

    async def schedule(self, appointment: Appointment) -> str:
        # Regla: la fecha debe ser en el futuro
        try:
            appt_date = datetime.fromisoformat(appointment.date)
            if appt_date <= datetime.now():
                raise ValueError('La fecha de la cita debe ser futura')
        except Exception as e:
            raise ValueError('Formato de fecha inválido o fecha pasada') from e
        return await self.repo.create(appointment)

    async def list_for_pet(self, pet_id: str) -> List[Appointment]:
        return await self.repo.list_by_pet(pet_id)

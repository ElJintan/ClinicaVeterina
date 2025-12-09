# src/interfaces/repositories.py
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Dict, Any
from src.domain.models import (
    Client, Pet, Appointment, MedicalRecord, Invoice,
    ClientCreate, PetCreate, AppointmentCreate, MedicalRecordCreate, InvoiceCreate
)

# Definimos tipos genéricos: T para el Modelo (lectura), C para el CreateDTO (escritura)
T = TypeVar('T')
C = TypeVar('C')

# --- Interfaz Base Genérica (Segregación de Interfaces + Liskov) ---
class IBaseRepository(ABC, Generic[T, C]):
    @abstractmethod
    async def create(self, create_data: C) -> str: 
        """Recibe un DTO de creación y retorna el ID generado."""
        pass

    @abstractmethod
    async def list(self) -> List[T]: 
        pass

    @abstractmethod
    async def get(self, entity_id: str) -> Optional[T]: 
        pass

    @abstractmethod
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[T]: 
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool: 
        pass

# --- Interfaces Específicas ---

class IClientRepository(IBaseRepository[Client, ClientCreate]):
    pass

class IPetRepository(IBaseRepository[Pet, PetCreate]):
    # Si en el futuro necesitas filtrar por dueño, añádelo aquí
    pass

class IAppointmentRepository(IBaseRepository[Appointment, AppointmentCreate]):
    # Mantenemos las interfaces limpias, pero preparadas para extensión
    pass

class IMedicalRecordRepository(IBaseRepository[MedicalRecord, MedicalRecordCreate]):
    @abstractmethod
    async def list_by_pet(self, pet_id: str) -> List[MedicalRecord]:
        """Método específico para historiales médicos."""
        pass

class IBillingRepository(IBaseRepository[Invoice, InvoiceCreate]):
    pass
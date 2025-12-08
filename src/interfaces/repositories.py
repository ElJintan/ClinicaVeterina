# src/interfaces/repositories.py - CONTRATOS SIMPLIFICADOS
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.models import Client, Pet, Appointment, MedicalRecord, Invoice, ClientCreate, PetCreate, AppointmentCreate, MedicalRecordCreate, InvoiceCreate 

# --- Interfaz Base para CRUD (DIP/SOLID) ---
class IBaseRepository(ABC):
    @abstractmethod
    async def create(self, entity: Any) -> str: pass
    @abstractmethod
    async def list(self) -> List[Any]: pass
    @abstractmethod
    async def get(self, entity_id: str) -> Optional[Any]: pass
    @abstractmethod
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Any]: pass
    @abstractmethod
    async def delete(self, entity_id: str) -> bool: pass

# --- Interfaces de Repositorios Específicos ---

class IClientRepository(IBaseRepository):
    @abstractmethod
    async def create(self, client_data: ClientCreate) -> str: pass 
    @abstractmethod
    async def list(self) -> List[Client]: pass
    @abstractmethod
    async def get(self, client_id: str) -> Optional[Client]: pass

class IPetRepository(IBaseRepository):
    @abstractmethod
    async def create(self, pet_data: PetCreate) -> str: pass
    @abstractmethod
    async def list(self) -> List[Pet]: pass
    # ELIMINADO: @abstractmethod async def list_by_owner(self, owner_id: str) -> List[Pet]: pass
    @abstractmethod
    async def get(self, pet_id: str) -> Optional[Pet]: pass

class IAppointmentRepository(IBaseRepository):
    @abstractmethod
    async def create(self, appointment_data: AppointmentCreate) -> str: pass
    @abstractmethod
    async def list(self) -> List[Appointment]: pass
    # ELIMINADO: @abstractmethod async def list_by_pet(self, pet_id: str) -> List[Appointment]: pass
    @abstractmethod
    async def get(self, appointment_id: str) -> Optional[Appointment]: pass

class IMedicalRecordRepository(IBaseRepository):
    @abstractmethod
    async def create(self, record_data: MedicalRecordCreate) -> str: pass
    @abstractmethod
    async def list(self) -> List[MedicalRecord]: pass
    # ELIMINADO: @abstractmethod async def list_by_pet(self, pet_id: str) -> List[MedicalRecord]: pass
    @abstractmethod
    async def get(self, record_id: str) -> Optional[MedicalRecord]: pass

class IBillingRepository(IBaseRepository):
    @abstractmethod
    async def create(self, invoice_data: InvoiceCreate) -> str: pass
    @abstractmethod
    async def list(self) -> List[Invoice]: pass
    # ELIMINADO: @abstractmethod async def list_by_client(self, client_id: str) -> List[Invoice]: pass
    @abstractmethod
    async def get(self, invoice_id: str) -> Optional[Invoice]: pass
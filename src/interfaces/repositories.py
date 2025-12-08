# src/interfaces/repositories.py - CÓDIGO COMPLETO Y CORREGIDO
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
# Importamos todos los modelos de dominio para que las interfaces los usen
from src.domain.models import Client, Pet, Appointment, MedicalRecord, Invoice 

# --- Interfaz Base para CRUD (SOLID) ---
class IBaseRepository(ABC):
    @abstractmethod
    async def create(self, entity: Any) -> str: 
        """Crea una nueva entidad y retorna su ID."""
        pass

    @abstractmethod
    async def list(self) -> List[Any]: 
        """Obtiene una lista de todas las entidades."""
        pass
    
    @abstractmethod
    async def get(self, entity_id: str) -> Optional[Any]: 
        """Obtiene una entidad por ID."""
        pass
    
    @abstractmethod
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Any]: 
        """Actualiza una entidad y retorna el objeto actualizado."""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool: 
        """Elimina una entidad y retorna True si tuvo éxito."""
        pass

# --- Interfaces de Repositorios Específicos (Heredan de IBaseRepository) ---

class IClientRepository(IBaseRepository):
    @abstractmethod
    async def create(self, client: Client) -> str: pass
    @abstractmethod
    async def list(self) -> List[Client]: pass
    @abstractmethod
    async def get(self, client_id: str) -> Optional[Client]: pass

class IPetRepository(IBaseRepository):
    @abstractmethod
    async def create(self, pet: Pet) -> str: pass
    @abstractmethod
    async def list(self) -> List[Pet]: pass
    @abstractmethod
    async def list_by_owner(self, owner_id: str) -> List[Pet]: pass
    @abstractmethod
    async def get(self, pet_id: str) -> Optional[Pet]: pass

class IAppointmentRepository(IBaseRepository):
    @abstractmethod
    async def create(self, appointment: Appointment) -> str: pass
    @abstractmethod
    async def list(self) -> List[Appointment]: pass
    @abstractmethod
    async def list_by_pet(self, pet_id: str) -> List[Appointment]: pass
    @abstractmethod
    async def get(self, appointment_id: str) -> Optional[Appointment]: pass

# FIX CRÍTICO: IMedicalRecordRepository
class IMedicalRecordRepository(IBaseRepository):
    @abstractmethod
    async def create(self, record: MedicalRecord) -> str: pass
    @abstractmethod
    async def list(self) -> List[MedicalRecord]: pass
    @abstractmethod
    async def list_by_pet(self, pet_id: str) -> List[MedicalRecord]: pass
    @abstractmethod
    async def get(self, record_id: str) -> Optional[MedicalRecord]: pass

# FIX CRÍTICO: IBillingRepository
class IBillingRepository(IBaseRepository):
    @abstractmethod
    async def create(self, invoice: Invoice) -> str: pass
    @abstractmethod
    async def list(self) -> List[Invoice]: pass
    @abstractmethod
    async def get(self, invoice_id: str) -> Optional[Invoice]: pass
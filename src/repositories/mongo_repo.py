# src/repositories/mongo_repo.py - REPOSITORIO EN MEMORIA MODIFICADO (SOLID)
from typing import List, Optional, Dict, Any, TypeVar, Generic
import logging
from pydantic import BaseModel
from src.interfaces.repositories import (
    IClientRepository, IPetRepository, IAppointmentRepository, 
    IMedicalRecordRepository, IBillingRepository
)
from src.domain.models import (
    Client, Pet, Appointment, MedicalRecord, Invoice,
    ClientCreate, PetCreate, AppointmentCreate, MedicalRecordCreate, InvoiceCreate
)
import uuid 

repo_logger = logging.getLogger(__name__)

# Base de datos en memoria 
IN_MEMORY_DB: Dict[str, Dict[str, Dict[str, Any]]] = {
    'clients': {}, 'pets': {}, 'appointments': {}, 
    'medical_records': {}, 'invoices': {}
}

# --- Funciones de ciclo de vida ---
async def connect_to_mongo():
    repo_logger.info("Usando repositorio In-Memory. No se requiere conexión a DB.")
    pass

async def close_mongo_connection():
    repo_logger.info("Cerrando repositorio In-Memory. No hay conexión que cerrar.")
    pass
# ---------------------------------------------------------------------------------

T = TypeVar('T', bound=BaseModel)
C = TypeVar('C', bound=BaseModel)

class InMemoryBaseRepository(Generic[T, C]):
    def __init__(self, collection_name: str, entity_model: TypeVar):
        self.col = IN_MEMORY_DB[collection_name]
        self.model_type = entity_model
        
    async def _list_by_field(self, field_name: str, field_value: Any) -> List[T]:
        """Ayudante para filtrar la colección en memoria por un campo (DRY)."""
        results = []
        for data in self.col.values():
            if data.get(field_name) == field_value:
                results.append(self.model_type(**data))
        return results

    async def create(self, create_data: C) -> str:
        new_id = str(uuid.uuid4())
        
        data_dict = create_data.dict(exclude_none=True)
        # Seteamos 'id' con el alias '_id' para el modelo base Pydantic
        full_entity = self.model_type(id=new_id, **data_dict)

        # Almacenar los datos de la entidad como diccionario
        self.col[new_id] = full_entity.dict(by_alias=False)
        return new_id

    async def list(self) -> List[T]:
        return [self.model_type(**d) for d in self.col.values()]

    async def get(self, entity_id: str) -> Optional[T]:
        data = self.col.get(entity_id)
        if not data:
            return None
        return self.model_type(**data)

    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[T]:
        if entity_id not in self.col:
            return None
        
        self.col[entity_id].update({k: v for k, v in updates.items() if v is not None})
        return await self.get(entity_id)

    async def delete(self, entity_id: str) -> bool:
        if entity_id in self.col:
            del self.col[entity_id]
            return True
        return False

# Repositorios Específicos
class MongoClientRepository(InMemoryBaseRepository[Client, ClientCreate], IClientRepository):
    def __init__(self): super().__init__('clients', Client)

class MongoPetRepository(InMemoryBaseRepository[Pet, PetCreate], IPetRepository):
    def __init__(self): super().__init__('pets', Pet)

class MongoAppointmentRepository(InMemoryBaseRepository[Appointment, AppointmentCreate], IAppointmentRepository):
    def __init__(self): super().__init__('appointments', Appointment)
    
class MongoMedicalRecordRepository(InMemoryBaseRepository[MedicalRecord, MedicalRecordCreate], IMedicalRecordRepository):
    def __init__(self):
        super().__init__('medical_records', MedicalRecord)
    
    # Implementa el método del contrato (IMedicalRecordRepository) usando el helper base.
    async def list_by_pet(self, pet_id: str) -> List[MedicalRecord]:
        return await self._list_by_field('pet_id', pet_id)


class MongoBillingRepository(InMemoryBaseRepository[Invoice, InvoiceCreate], IBillingRepository):
    def __init__(self): super().__init__('invoices', Invoice)
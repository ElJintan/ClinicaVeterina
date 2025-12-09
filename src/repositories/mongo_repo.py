# src/repositories/mongo_repo.py - REPOSITORIO MONGODB REAL (CON MOTOR)
import os
import logging
import uuid
from typing import List, Optional, Dict, Any, TypeVar, Generic
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from src.interfaces.repositories import (
    IClientRepository, IPetRepository, IAppointmentRepository, 
    IMedicalRecordRepository, IBillingRepository
)
from src.domain.models import (
    Client, Pet, Appointment, MedicalRecord, Invoice,
    ClientCreate, PetCreate, AppointmentCreate, MedicalRecordCreate, InvoiceCreate
)

repo_logger = logging.getLogger(__name__)

# Variables globales para la conexión
DB_CLIENT: Optional[AsyncIOMotorClient] = None
DB_DATABASE = None

# --- Funciones de ciclo de vida ---
async def connect_to_mongo():
    global DB_CLIENT, DB_DATABASE
    # Obtenemos la URI del docker-compose environment o usamos local por defecto
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGO_DB_NAME", "clinica_veterinaria")
    
    repo_logger.info(f"Conectando a MongoDB en: {mongo_uri} (DB: {db_name})")
    
    try:
        DB_CLIENT = AsyncIOMotorClient(mongo_uri)
        DB_DATABASE = DB_CLIENT[db_name]
        # Verificar conexión (ping)
        await DB_CLIENT.admin.command('ping')
        repo_logger.info("¡Conexión a MongoDB exitosa!")
    except Exception as e:
        repo_logger.error(f"Error conectando a MongoDB: {e}")
        raise e

async def close_mongo_connection():
    global DB_CLIENT
    if DB_CLIENT:
        repo_logger.info("Cerrando conexión a MongoDB...")
        DB_CLIENT.close()
        repo_logger.info("Conexión cerrada.")
# ---------------------------------------------------------------------------------

T = TypeVar('T', bound=BaseModel)
C = TypeVar('C', bound=BaseModel)

class MongoBaseRepository(Generic[T, C]):
    def __init__(self, collection_name: str, entity_model: TypeVar):
        self.collection_name = collection_name
        self.model_type = entity_model

    @property
    def col(self):
        """
        Accede a la colección de forma perezosa (lazy) para asegurar 
        que DB_DATABASE ya esté inicializado.
        """
        if DB_DATABASE is None:
            raise ConnectionError("La base de datos no está conectada. Llama a connect_to_mongo() primero.")
        return DB_DATABASE[self.collection_name]

    def _map_doc(self, doc: Dict[str, Any]) -> Optional[T]:
        """Convierte el documento de Mongo (_id) al modelo Pydantic (id)."""
        if not doc:
            return None
        # Mapear _id (Mongo) a id (Pydantic)
        if '_id' in doc:
            doc['id'] = doc.pop('_id')
        return self.model_type(**doc)

    async def _list_by_field(self, field_name: str, field_value: Any) -> List[T]:
        cursor = self.col.find({field_name: field_value})
        docs = await cursor.to_list(length=None)
        return [self._map_doc(doc) for doc in docs]

    async def create(self, create_data: C) -> str:
        new_id = str(uuid.uuid4())
        data = create_data.dict(exclude_none=True)
        
        # Asignamos el ID generado a _id para Mongo
        data['_id'] = new_id
        
        # Insertamos en Mongo
        await self.col.insert_one(data)
        return new_id

    async def list(self) -> List[T]:
        cursor = self.col.find()
        docs = await cursor.to_list(length=None)
        return [self._map_doc(doc) for doc in docs]

    async def get(self, entity_id: str) -> Optional[T]:
        doc = await self.col.find_one({'_id': entity_id})
        return self._map_doc(doc)

    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[T]:
        # Filtramos valores None para no borrarlos accidentalmente
        clean_updates = {k: v for k, v in updates.items() if v is not None}
        
        if clean_updates:
            result = await self.col.update_one(
                {'_id': entity_id}, 
                {'$set': clean_updates}
            )
            if result.matched_count == 0:
                return None
                
        return await self.get(entity_id)

    async def delete(self, entity_id: str) -> bool:
        result = await self.col.delete_one({'_id': entity_id})
        return result.deleted_count > 0

# src/repositories/mongo_repo.py (Asegúrate de que estas clases estén añadidas)

# Repositorios Específicos
class MongoClientRepository(MongoBaseRepository[Client, ClientCreate], IClientRepository):
    # Asumo que esta clase ya existía
    def __init__(self): super().__init__('clients', Client)

# --- INICIO DE LOS REPOSITORIOS FALTANTES ---

class MongoPetRepository(MongoBaseRepository[Pet, PetCreate], IPetRepository):
    def __init__(self): super().__init__('pets', Pet)
    async def list_by_owner(self, owner_id: str) -> List[Pet]:
        # Implementación específica para la interfaz IPetRepository
        return await self._list_by_field('client_id', owner_id)

class MongoAppointmentRepository(MongoBaseRepository[Appointment, AppointmentCreate], IAppointmentRepository):
    def __init__(self): super().__init__('appointments', Appointment)
    async def list_by_pet(self, pet_id: str) -> List[Appointment]:
        # Implementación específica para la interfaz IAppointmentRepository
        return await self._list_by_field('pet_id', pet_id)

class MongoMedicalRecordRepository(MongoBaseRepository[MedicalRecord, MedicalRecordCreate], IMedicalRecordRepository):
    def __init__(self): super().__init__('medical_records', MedicalRecord)
    async def list_by_pet(self, pet_id: str) -> List[MedicalRecord]:
        # Implementación específica para la interfaz IMedicalRecordRepository
        return await self._list_by_field('pet_id', pet_id)

class MongoBillingRepository(MongoBaseRepository[Invoice, InvoiceCreate], IBillingRepository):
    def __init__(self): super().__init__('billing', Invoice)
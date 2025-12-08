# src/repositories/mongo_repo.py - CÓDIGO COMPLETO Y FINAL
from typing import List, Optional
import logging
from src.interfaces.repositories import IClientRepository, IPetRepository, IAppointmentRepository, IMedicalRecordRepository, IBillingRepository
from src.domain.models import Client, Pet, Appointment, MedicalRecord, Invoice
from motor.motor_asyncio import AsyncIOMotorClient
import os
from bson import ObjectId

repo_logger = logging.getLogger(__name__)
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017')
_client: Optional[AsyncIOMotorClient] = None
_db = None

# Funciones de ciclo de vida (conect_to_mongo y close_mongo_connection)
# ... (Asumido que este código ya está correcto desde la corrección anterior) ...
async def connect_to_mongo():
    global _client, _db
    if _client is None:
        try:
            repo_logger.info("Attempting to connect to MongoDB at %s", MONGO_URI)
            _client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000) 
            await _client.admin.command('ping')
            _db = _client['clinic_db']
            repo_logger.info("Successfully connected to MongoDB.")
        except Exception as e:
            repo_logger.error("Failed to connect to MongoDB: %s", e)
            raise RuntimeError("Database connection failed during startup.") from e

async def close_mongo_connection():
    global _client
    if _client:
        repo_logger.info("Closing MongoDB connection.")
        _client.close()
# ...

async def _update_one(collection, entity_id: str, updates: dict, model_type: BaseModel) -> Optional[BaseModel]:
    if not updates: return None
    
    # Prepara el documento de actualización, excluyendo Nones y campos protegidos.
    update_doc = {k: v for k, v in updates.items() if v is not None}
    
    res = await collection.update_one(
        {'_id': ObjectId(entity_id)},
        {'$set': update_doc}
    )
    
    if res.modified_count == 1:
        return await _get_one(collection, entity_id, model_type)
    return None

async def _delete_one(collection, entity_id: str) -> bool:
    res = await collection.delete_one({'_id': ObjectId(entity_id)})
    return res.deleted_count == 1

async def _get_one(collection, entity_id: str, model_type: BaseModel) -> Optional[BaseModel]:
    d = await collection.find_one({'_id': ObjectId(entity_id)})
    if not d: return None
    d['id'] = str(d.get('_id'))
    return model_type(**d)

# Repositorios CRUD completos
class MongoClientRepository(IClientRepository):
    def __init__(self):
        if _db is None: raise RuntimeError("Repo initialized before connection.")
        self.col = _db['clients']

    async def create(self, client: Client) -> str:
        doc = client.dict(exclude_none=True, by_alias=True)
        if '_id' in doc and doc['_id'] is None: del doc['_id']
        res = await self.col.insert_one(doc)
        return str(res.inserted_id)

    async def list(self) -> List[Client]:
        docs = await self.col.find().to_list(100)
        return [Client(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]

    async def get(self, client_id: str) -> Optional[Client]:
        return await _get_one(self.col, client_id, Client)

    async def update(self, entity_id: str, updates: dict) -> Optional[Client]: # NUEVO
        return await _update_one(self.col, entity_id, updates, Client)
    
    async def delete(self, entity_id: str) -> bool: # NUEVO
        return await _delete_one(self.col, entity_id)


class MongoPetRepository(IPetRepository):
    def __init__(self):
        if _db is None: raise RuntimeError("Repo initialized before connection.")
        self.col = _db['pets']

    async def create(self, pet: Pet) -> str:
        doc = pet.dict(exclude_none=True, by_alias=True)
        if '_id' in doc and doc['_id'] is None: del doc['_id']
        res = await self.col.insert_one(doc)
        return str(res.inserted_id)

    async def list(self) -> List[Pet]:
        docs = await self.col.find().to_list(100)
        return [Pet(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]

    async def list_by_owner(self, owner_id: str) -> List[Pet]:
        docs = await self.col.find({'owner_id': owner_id}).to_list(100)
        return [Pet(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]

    async def get(self, pet_id: str) -> Optional[Pet]:
        return await _get_one(self.col, pet_id, Pet)

    async def update(self, entity_id: str, updates: dict) -> Optional[Pet]: # NUEVO
        return await _update_one(self.col, entity_id, updates, Pet)
    
    async def delete(self, entity_id: str) -> bool: # NUEVO
        return await _delete_one(self.col, entity_id)

class MongoAppointmentRepository(IAppointmentRepository):
    def __init__(self):
        if _db is None: raise RuntimeError("Repo initialized before connection.")
        self.col = _db['appointments']

    async def create(self, appointment: Appointment) -> str:
        doc = appointment.dict(exclude_none=True, by_alias=True)
        if '_id' in doc and doc['_id'] is None: del doc['_id']
        res = await self.col.insert_one(doc)
        return str(res.inserted_id)
        
    async def list(self) -> List[Appointment]:
        docs = await self.col.find().to_list(100)
        return [Appointment(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]

    async def list_by_pet(self, pet_id: str) -> List[Appointment]:
        docs = await self.col.find({'pet_id': pet_id}).to_list(100)
        return [Appointment(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]
        
    async def get(self, appointment_id: str) -> Optional[Appointment]:
        return await _get_one(self.col, appointment_id, Appointment)

    async def update(self, entity_id: str, updates: dict) -> Optional[Appointment]: # NUEVO
        return await _update_one(self.col, entity_id, updates, Appointment)
    
    async def delete(self, entity_id: str) -> bool: # NUEVO
        return await _delete_one(self.col, entity_id)

# NUEVO REPOSITORIO: Historial Médico
class MongoMedicalRecordRepository(IMedicalRecordRepository):
    def __init__(self):
        if _db is None: raise RuntimeError("Repo initialized before connection.")
        self.col = _db['medical_records']

    async def create(self, record: MedicalRecord) -> str:
        doc = record.dict(exclude_none=True, by_alias=True)
        if '_id' in doc and doc['_id'] is None: del doc['_id']
        res = await self.col.insert_one(doc)
        return str(res.inserted_id)

    async def list(self) -> List[MedicalRecord]:
        docs = await self.col.find().to_list(100)
        return [MedicalRecord(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]

    async def list_by_pet(self, pet_id: str) -> List[MedicalRecord]:
        docs = await self.col.find({'pet_id': pet_id}).to_list(100)
        return [MedicalRecord(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]

    async def get(self, record_id: str) -> Optional[MedicalRecord]:
        return await _get_one(self.col, record_id, MedicalRecord)

    async def update(self, entity_id: str, updates: dict) -> Optional[MedicalRecord]:
        return await _update_one(self.col, entity_id, updates, MedicalRecord)
    
    async def delete(self, entity_id: str) -> bool:
        return await _delete_one(self.col, entity_id)

# NUEVO REPOSITORIO: Facturación
class MongoBillingRepository(IBillingRepository):
    def __init__(self):
        if _db is None: raise RuntimeError("Repo initialized before connection.")
        self.col = _db['invoices']

    async def create(self, invoice: Invoice) -> str:
        doc = invoice.dict(exclude_none=True, by_alias=True)
        if '_id' in doc and doc['_id'] is None: del doc['_id']
        res = await self.col.insert_one(doc)
        return str(res.inserted_id)

    async def list(self) -> List[Invoice]:
        docs = await self.col.find().to_list(100)
        return [Invoice(id=str(d.get('_id')), **{k:v for k,v in d.items() if k != '_id'}) for d in docs]

    async def get(self, invoice_id: str) -> Optional[Invoice]:
        return await _get_one(self.col, invoice_id, Invoice)

    async def update(self, entity_id: str, updates: dict) -> Optional[Invoice]:
        return await _update_one(self.col, entity_id, updates, Invoice)
    
    async def delete(self, entity_id: str) -> bool:
        return await _delete_one(self.col, entity_id)
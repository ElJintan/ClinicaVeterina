from typing import List, Optional, Type, TypeVar
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from src.interfaces.repositories import (
    IClientRepository, IPetRepository, IAppointmentRepository,
    IMedicalRepository, IBillingRepository, IFeedbackRepository
)
from src.domain.models import Client, Pet, Appointment, MedicalRecord, Invoice, Feedback

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
_client = AsyncIOMotorClient(MONGO_URI)
_db = _client['clinic_db']

T = TypeVar('T')

# Helper para convertir _id de Mongo a string
def map_doc(doc, model_class: Type[T]) -> T:
    if not doc: return None
    doc['_id'] = str(doc['_id'])
    return model_class(**doc)

class MongoClientRepository(IClientRepository):
    def __init__(self): self.col = _db['clients']
    
    async def create(self, client: Client) -> str:
        res = await self.col.insert_one(client.dict(exclude={'id'}, exclude_none=True))
        return str(res.inserted_id)
        
    async def get_all(self) -> List[Client]:
        docs = await self.col.find().to_list(100)
        return [map_doc(d, Client) for d in docs]
        
    async def get_by_id(self, client_id: str) -> Optional[Client]:
        try:
            doc = await self.col.find_one({'_id': ObjectId(client_id)})
            return map_doc(doc, Client)
        except: return None

class MongoPetRepository(IPetRepository):
    def __init__(self): self.col = _db['pets']
    
    async def create(self, pet: Pet) -> str:
        res = await self.col.insert_one(pet.dict(exclude={'id'}, exclude_none=True))
        return str(res.inserted_id)

    async def list_by_owner(self, owner_id: str) -> List[Pet]:
        docs = await self.col.find({'owner_id': owner_id}).to_list(100)
        return [map_doc(d, Pet) for d in docs]
        
    async def get_by_id(self, pet_id: str) -> Optional[Pet]:
        try:
            doc = await self.col.find_one({'_id': ObjectId(pet_id)})
            return map_doc(doc, Pet)
        except: return None

class MongoAppointmentRepository(IAppointmentRepository):
    def __init__(self): self.col = _db['appointments']

    async def create(self, appointment: Appointment) -> str:
        res = await self.col.insert_one(appointment.dict(exclude={'id'}, exclude_none=True))
        return str(res.inserted_id)

    async def list_by_pet(self, pet_id: str) -> List[Appointment]:
        docs = await self.col.find({'pet_id': pet_id}).to_list(100)
        return [map_doc(d, Appointment) for d in docs]
    
    async def update_status(self, appointment_id: str, status: str) -> bool:
        res = await self.col.update_one({'_id': ObjectId(appointment_id)}, {'$set': {'status': status}})
        return res.modified_count > 0

class MongoMedicalRepository(IMedicalRepository):
    def __init__(self): self.col = _db['medical_records']
    
    async def add_entry(self, entry: MedicalRecord) -> str:
        res = await self.col.insert_one(entry.dict(exclude={'id'}, exclude_none=True))
        return str(res.inserted_id)
        
    async def get_history(self, pet_id: str) -> List[MedicalRecord]:
        docs = await self.col.find({'pet_id': pet_id}).to_list(100)
        return [map_doc(d, MedicalRecord) for d in docs]

class MongoBillingRepository(IBillingRepository):
    def __init__(self): self.col = _db['invoices']
    
    async def create_invoice(self, invoice: Invoice) -> str:
        res = await self.col.insert_one(invoice.dict(exclude={'id'}, exclude_none=True))
        return str(res.inserted_id)
        
    async def get_client_invoices(self, client_id: str) -> List[Invoice]:
        docs = await self.col.find({'client_id': client_id}).to_list(100)
        return [map_doc(d, Invoice) for d in docs]

class MongoFeedbackRepository(IFeedbackRepository):
    def __init__(self): self.col = _db['feedback']
    
    async def add_feedback(self, feedback: Feedback) -> str:
        res = await self.col.insert_one(feedback.dict(exclude={'id'}, exclude_none=True))
        return str(res.inserted_id)
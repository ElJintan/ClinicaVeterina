from typing import List, Optional
from src.interfaces.repositories import IClientRepository, IPetRepository, IAppointmentRepository
from src.domain.models import Client, Pet, Appointment
from motor.motor_asyncio import AsyncIOMotorClient
import os
from bson import ObjectId

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
_client = AsyncIOMotorClient(MONGO_URI)
_db = _client['clinic_db']

class MongoClientRepository(IClientRepository):
    def __init__(self):
        self.col = _db['clients']

    async def create(self, client: Client) -> str:
        doc = client.dict(exclude_none=True)
        res = await self.col.insert_one(doc)
        return str(res.inserted_id)

    async def list(self) -> List[Client]:
        docs = await self.col.find().to_list(100)
        result = []
        for d in docs:
            d['id'] = str(d.get('_id'))
            result.append(Client(**d))
        return result

    async def get(self, client_id: str) -> Optional[Client]:
        d = await self.col.find_one({'_id': ObjectId(client_id)})
        if not d:
            return None
        d['id'] = str(d.get('_id'))
        return Client(**d)

class MongoPetRepository(IPetRepository):
    def __init__(self):
        self.col = _db['pets']

    async def create(self, pet: Pet) -> str:
        res = await self.col.insert_one(pet.dict(exclude_none=True))
        return str(res.inserted_id)

    async def list_by_owner(self, owner_id: str) -> List[Pet]:
        docs = await self.col.find({'owner_id': owner_id}).to_list(100)
        result = []
        for d in docs:
            d['id'] = str(d.get('_id'))
            result.append(Pet(**d))
        return result

class MongoAppointmentRepository(IAppointmentRepository):
    def __init__(self):
        self.col = _db['appointments']

    async def create(self, appointment: Appointment) -> str:
        res = await self.col.insert_one(appointment.dict(exclude_none=True))
        return str(res.inserted_id)

    async def list_by_pet(self, pet_id: str) -> List[Appointment]:
        docs = await self.col.find({'pet_id': pet_id}).to_list(100)
        result = []
        for d in docs:
            d['id'] = str(d.get('_id'))
            result.append(Appointment(**d))
        return result

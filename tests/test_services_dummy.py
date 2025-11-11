import asyncio
from src.domain.models import Client
from src.services.client_service import ClientService

class DummyRepo:
    def __init__(self):
        self.storage = []
    async def create(self, client):
        self.storage.append(client)
        return 'id123'
    async def list(self):
        return self.storage
    async def get(self, client_id):
        return None

def test_client_service():
    repo = DummyRepo()
    svc = ClientService(repo)
    client = Client(name='Ana', email='ana@example.com')
    loop = asyncio.get_event_loop()
    cid = loop.run_until_complete(svc.create_client(client))
    assert cid == 'id123'
    lst = loop.run_until_complete(svc.list_clients())
    assert len(lst) == 1

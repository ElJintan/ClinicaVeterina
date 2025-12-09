import pytest
from unittest.mock import MagicMock
from typing import Optional, List, Dict, Any
import uuid

# Importaciones de la API
from src.main import app 
from src.interfaces.repositories import (
    IClientRepository, IPetRepository, IAppointmentRepository, IBillingRepository
)
from src.domain.models import (
    Client, ClientCreate,
    Pet, PetCreate, 
    Appointment, AppointmentCreate, 
    Invoice, InvoiceCreate, 
)
# Importamos los inyectores de dependencia desde los controladores
from src.controllers.clients_controller import get_client_service
from src.controllers.pets_controller import get_pet_service
from src.controllers.appointments_controller import get_appointment_service
from src.controllers.billing_controller import get_billing_service
from src.services.client_service import ClientService
from src.services.pet_service import PetService
from src.services.appointment_service import AppointmentService
from src.services.billing_service import BillingService


# --- CLASE BASE DE REPOSITORIO EN MEMORIA ---
class InMemoryBaseRepository:
    """Implementación de la lógica en memoria, sin heredar interfaces abstractas (ABC)."""
    def __init__(self, model_type):
        self.storage: Dict[str, dict] = {}
        self.model_type = model_type

    async def _create_base(self, create_data) -> str:
        new_id = str(uuid.uuid4())
        data = create_data.model_dump(exclude_none=True) 
        self.storage[new_id] = data
        return new_id

    async def _list_base(self) -> List[Any]:
        return [self.model_type(id=k, **v) for k, v in self.storage.items()]

    async def _get_base(self, entity_id: str) -> Optional[Any]:
        data = self.storage.get(entity_id)
        if data:
            return self.model_type(id=entity_id, **data)
        return None

    async def _update_base(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Any]:
        if entity_id in self.storage:
            self.storage[entity_id].update(updates)
            return await self._get_base(entity_id)
        return None

    async def _delete_base(self, entity_id: str) -> bool:
        if entity_id in self.storage:
            del self.storage[entity_id]
            return True
        return False
        
# --- REPOSITORIOS MOCK ESPECÍFICOS (Delegación explícita para pasar el chequeo ABC) ---

class MockClientRepository(IClientRepository, InMemoryBaseRepository):
    def __init__(self): super().__init__(Client)
    # 💡 DELEGACIÓN EXPLÍCITA (Soluciona el TypeError para Cliente)
    async def create(self, create_data: ClientCreate) -> str: return await self._create_base(create_data)
    async def list(self) -> List[Client]: return await self._list_base()
    async def get(self, entity_id: str) -> Optional[Client]: return await self._get_base(entity_id)
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Client]: return await self._update_base(entity_id, updates)
    async def delete(self, entity_id: str) -> bool: return await self._delete_base(entity_id)

class MockPetRepository(IPetRepository, InMemoryBaseRepository):
    def __init__(self): super().__init__(Pet)
    # 💡 DELEGACIÓN EXPLÍCITA (Soluciona el TypeError para Mascota)
    async def create(self, create_data: PetCreate) -> str: return await self._create_base(create_data)
    async def list(self) -> List[Pet]: return await self._list_base()
    async def get(self, entity_id: str) -> Optional[Pet]: return await self._get_base(entity_id)
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Pet]: return await self._update_base(entity_id, updates)
    async def delete(self, entity_id: str) -> bool: return await self._delete_base(entity_id)
    async def list_by_owner(self, owner_id: str) -> List[Pet]:
        return [Pet(id=k, **v) for k, v in self.storage.items() if v.get('client_id') == owner_id]

class MockAppointmentRepository(IAppointmentRepository, InMemoryBaseRepository):
    def __init__(self): super().__init__(Appointment)
    # 💡 DELEGACIÓN EXPLÍCITA (Soluciona el TypeError para Cita)
    async def create(self, create_data: AppointmentCreate) -> str: return await self._create_base(create_data)
    async def list(self) -> List[Appointment]: return await self._list_base()
    async def get(self, entity_id: str) -> Optional[Appointment]: return await self._get_base(entity_id)
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Appointment]: return await self._update_base(entity_id, updates)
    async def delete(self, entity_id: str) -> bool: return await self._delete_base(entity_id)
    async def list_by_pet(self, pet_id: str) -> List[Appointment]:
        return [Appointment(id=k, **v) for k, v in self.storage.items() if v.get('pet_id') == pet_id]

class MockBillingRepository(IBillingRepository, InMemoryBaseRepository):
    def __init__(self): super().__init__(Invoice)
    # 💡 DELEGACIÓN EXPLÍCITA (Soluciona el TypeError para Factura)
    async def create(self, create_data: InvoiceCreate) -> str: return await self._create_base(create_data)
    async def list(self) -> List[Invoice]: return await self._list_base()
    async def get(self, entity_id: str) -> Optional[Invoice]: return await self._get_base(entity_id)
    async def update(self, entity_id: str, updates: Dict[str, Any]) -> Optional[Invoice]: return await self._update_base(entity_id, updates)
    async def delete(self, entity_id: str) -> bool: return await self._delete_base(entity_id)


# --- INYECTORES DE MOCK DE SERVICIO ---
def get_mock_service(ServiceClass, RepoClass):
    repo = RepoClass()
    return ServiceClass(repo=repo, logger=MagicMock()) 

def get_mock_client_service():
    return get_mock_service(ClientService, MockClientRepository)

def get_mock_pet_service():
    return get_mock_service(PetService, MockPetRepository)

def get_mock_appointment_service():
    return get_mock_service(AppointmentService, MockAppointmentRepository)

def get_mock_billing_service():
    return get_mock_service(BillingService, MockBillingRepository)


# --- FIXTURE AUTOUSE ---
@pytest.fixture(scope="session", autouse=True)
def override_all_dependencies():
    app.dependency_overrides[get_client_service] = get_mock_client_service
    app.dependency_overrides[get_pet_service] = get_mock_pet_service
    app.dependency_overrides[get_appointment_service] = get_mock_appointment_service
    app.dependency_overrides[get_billing_service] = get_mock_billing_service
    
    yield
    
    app.dependency_overrides.clear()
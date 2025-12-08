# src/controllers/clients_controller.py - CORREGIDO
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional # Asegurar Optional si lo usas
from src.domain.models import Client, ClientCreate # Asumimos ClientCreate existe
from src.services.client_service import ClientService
from src.exceptions import NotFoundException, ValidationException, RepositoryException
from src.repositories.mongo_repo import MongoClientRepository 
from src.infrastructure.logger_impl import LoggerImpl 

router = APIRouter()

# FIX: Función de inyección de dependencia que crea el servicio con sus dependencias
def get_client_service() -> ClientService:
    repo = MongoClientRepository()
    logger = LoggerImpl(ClientService.__name__)
    return ClientService(repo=repo, logger=logger) 

# POST endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Client)
async def create_client_endpoint(
    client_create: ClientCreate,
    client_service: ClientService = Depends(get_client_service)
):
    """Crea un nuevo cliente."""
    try:
        client = await client_service.create_client(client_create)
        return client
    except ValidationException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepositoryException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# GET LIST endpoint
@router.get("/", response_model=List[Client])
async def list_clients_endpoint(
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene la lista completa de clientes."""
    return await client_service.list_clients()

# GET by ID endpoint
@router.get("/{client_id}", response_model=Client)
async def get_client_endpoint(
    client_id: str,
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene un cliente por ID."""
    try:
        client = await client_service.get_client(client_id)
        if not client:
            raise NotFoundException(f"Cliente con ID {client_id} no encontrado.")
        return client
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
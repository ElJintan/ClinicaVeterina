# src/controllers/clients_controller.py - FIX CRUD COMPLETO
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional

from src.domain.models import Client, ClientCreate, ClientUpdate # Importar ClientUpdate
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

# POST: Crea Cliente
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Client)
async def create_client_endpoint(client_create: ClientCreate, client_service: ClientService = Depends(get_client_service)):
    # ... (lógica de try/except) ...
    try: client = await client_service.create_client(client_create); return client
    except ValidationException as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepositoryException as e: raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# GET: Lista Clientes
@router.get("/", response_model=List[Client])
async def list_clients_endpoint(client_service: ClientService = Depends(get_client_service)):
    return await client_service.list_clients()

# PUT: Actualiza Cliente
@router.put("/{client_id}", response_model=Client)
async def update_client_endpoint(
    client_id: str, 
    updates: ClientUpdate, 
    client_service: ClientService = Depends(get_client_service)
):
    try:
        client = await client_service.update_client(client_id, updates)
        if not client: raise NotFoundException("Cliente no encontrado.")
        return client
    except NotFoundException as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# DELETE: Elimina Cliente
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client_endpoint(client_id: str, client_service: ClientService = Depends(get_client_service)):
    success = await client_service.delete_client(client_id)
    if not success: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado o no se pudo eliminar.")
    return
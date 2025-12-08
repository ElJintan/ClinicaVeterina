# src/controllers/clients_controller.py - CORREGIDO
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List

from src.domain.models import Client, ClientCreate
from src.services.client_service import ClientService
from src.exceptions import NotFoundException, ValidationException # Importar excepciones

router = APIRouter()

# Inyección de dependencia (ClientService)
def get_client_service() -> ClientService:
    # Esto asume que ClientService puede ser instanciado aquí
    return ClientService()

@router.post("", status_code=status.HTTP_201_CREATED, response_model=Client)
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


@router.get("/", response_model=List[Client])
async def list_clients_endpoint(
    client_service: ClientService = Depends(get_client_service)
):
    """Obtiene la lista completa de clientes."""
    # El endpoint vacío ("") y el de raíz ("/") apuntan al mismo lugar si la URL no termina en barra.
    # Usar "/" es más seguro para asegurar que GET /clients/ funcione.
    return await client_service.list_clients()


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
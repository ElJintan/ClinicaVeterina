from fastapi import APIRouter, Depends, HTTPException
from src.domain.models import Client
from src.services.client_service import ClientService
from src.repositories.mongo_repo import MongoClientRepository

router = APIRouter()

def get_client_service():
    repo = MongoClientRepository()
    return ClientService(repo)

@router.post('/', response_model=Client)
async def create_client(payload: Client, svc: ClientService = Depends(get_client_service)):
    try:
        client_id = await svc.create_client(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {**payload.dict(), 'id': client_id}

@router.get('/', response_model=list[Client])
async def list_clients(svc: ClientService = Depends(get_client_service)):
    return await svc.list_clients()

from fastapi import APIRouter, Depends, HTTPException
from src.domain.models import Client
from src.services.client_service import ClientService
from src.repositories.mongo_repo import MongoClientRepository
from src.infrastructure.logger import StandardLogger

router = APIRouter()

# Factory para inyectar dependencias
def get_client_service():
    repo = MongoClientRepository()
    logger = StandardLogger()
    return ClientService(repo, logger)

@router.post('/', response_model=dict) # Cambiado para devolver dict flexible
async def create_client(payload: Client, svc: ClientService = Depends(get_client_service)):
    try:
        client_id = await svc.create_client(payload)
        return {**payload.dict(), 'id': client_id}
    except ValueError as e:
        # Errores de validación (400)
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        # Errores internos (500)
        raise HTTPException(status_code=500, detail=str(e))
# src/main.py
import logging
from contextlib import asynccontextmanager 
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.logging_config import configure_root_logger 
from src.repositories.mongo_repo import connect_to_mongo, close_mongo_connection 

# Asumiendo que estos archivos existen en tu proyecto local ya que no fueron provistos para corrección
from src.controllers.clients_controller import router as clients_router
from src.controllers.pets_controller import router as pets_router
from src.controllers.appointments_controller import router as appointments_router
from src.controllers.medical_records_controller import router as medical_records_router
from src.controllers.billing_controller import router as billing_router

from src.exceptions import AppException, DomainException, NotFoundException

# Configuración inicial
configure_root_logger(level=logging.INFO) 
logger = logging.getLogger("clinica")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación y repositorios In-Memory...")
    await connect_to_mongo() 
    logger.info("Aplicación iniciada.")
    yield
    logger.info("Apagando aplicación...")
    await close_mongo_connection()
    logger.info("Aplicación finalizada.")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Error no manejado: {e}")
            raise

app = FastAPI(title='Clínica Veterinaria - SOLID Refactored', lifespan=lifespan)
app.add_middleware(LoggingMiddleware)

# Routers
app.include_router(clients_router, prefix='/clients', tags=['clients'])
app.include_router(pets_router, prefix='/pets', tags=['pets'])
app.include_router(appointments_router, prefix='/appointments', tags=['appointments'])
app.include_router(medical_records_router, prefix='/medical-records', tags=['medical records'])
app.include_router(billing_router, prefix='/billing', tags=['billing'])

@app.get('/')
async def root():
    return {'message': 'Clínica Veterinaria - SOLID API funcionando'}

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    if isinstance(exc, NotFoundException):
        raise HTTPException(status_code=404, detail=str(exc))
    raise HTTPException(status_code=400, detail=str(exc))
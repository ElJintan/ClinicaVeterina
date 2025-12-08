import logging
from contextlib import asynccontextmanager 
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.config.logging_config import configure_root_logger 
from src.repositories.mongo_repo import connect_to_mongo, close_mongo_connection 

from src.controllers.clients_controller import router as clients_router
from src.controllers.pets_controller import router as pets_router
from src.controllers.appointments_controller import router as appointments_router
from src.exceptions import AppException, DomainException, NotFoundException

# 1. Configuración del logger antes de usarlo
configure_root_logger(level=logging.INFO) 
logger = logging.getLogger("clinica")

# 2. Definición del Lifespan para manejar el ciclo de vida (SOLID)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Evento de Startup
    logger.info("Starting up application and connecting to MongoDB...")
    await connect_to_mongo() 
    logger.info("MongoDB connection attempt finished.")
    yield
    # Evento de Shutdown
    logger.info("Shutting down application and closing MongoDB connection...")
    await close_mongo_connection()
    logger.info("MongoDB connection closed.")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        try:
            response = await call_next(request)
            logger.info(f"Response status: {response.status_code} for {request.method} {request.url}")
            return response
        except Exception as e:
            logger.exception(f"Unhandled exception for {request.method} {request.url}: {e}")
            raise

# Pasar el lifespan al constructor de FastAPI
app = FastAPI(title='Clínica Veterinaria - SOLID', lifespan=lifespan)
app.add_middleware(LoggingMiddleware)

# Inclusión de routers
app.include_router(clients_router, prefix='/clients', tags=['clients'])
app.include_router(pets_router, prefix='/pets', tags=['pets'])
app.include_router(appointments_router, prefix='/appointments', tags=['appointments'])

@app.get('/')
async def root():
    return {'message': 'Clínica Veterinaria - SOLID (src)'}

# Handler para excepciones de la capa de aplicación (AppException)
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.warning("AppException: %s %s -> %s", request.method, request.url.path, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Handler para excepciones de la capa de dominio (DomainException)
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    logger.warning(f"DomainException: {type(exc).__name__} - {exc}")
    if isinstance(exc, NotFoundException):
        raise HTTPException(status_code=404, detail=str(exc))
    raise HTTPException(status_code=400, detail=str(exc))
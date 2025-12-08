from fastapi import FastAPI

from src.controllers.clients_controller import router as clients_router
from src.controllers.pets_controller import router as pets_router
from src.controllers.appointments_controller import router as appointments_router

app = FastAPI(title='Clínica Veterinaria - SOLID')

app.include_router(clients_router, prefix='/clients', tags=['clients'])
app.include_router(pets_router, prefix='/pets', tags=['pets'])
app.include_router(appointments_router, prefix='/appointments', tags=['appointments'])

@app.get('/')
async def root():
    return {'message': 'Clínica Veterinaria - SOLID (src)'}

# fragmento para src/main.py (ver bloque completo después)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.exceptions import AppException

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger = logging.getLogger("clinica")
    logger.warning("AppException: %s %s -> %s", request.method, request.url.path, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
# fragmento para src/main.py (ver bloque completo después)
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.exceptions import AppException

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger = logging.getLogger("clinica")
    logger.warning("AppException: %s %s -> %s", request.method, request.url.path, exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
# al inicio

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

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture
def create_test_cliente():
    # Campos corregidos para ClientCreate: name, email, phone
    cliente_data = {
        "name": "Test Cliente",
        "email": "test@example.com",
        "phone": "987654321", 
        "address": "Calle Falsa 123"
    }
    # Ruta corregida: /clients/
    response = client.post("/clients/", json=cliente_data)
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def create_test_mascota(create_test_cliente):
    # Campos corregidos para PetCreate
    mascota_data = {
        "client_id": create_test_cliente,
        "name": "Firulais",
        "species": "Perro",
        "breed": "Labrador",
        "birthdate": "2020-05-10"
    }
    # Ruta corregida: /pets/
    response = client.post("/pets/", json=mascota_data)
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def create_test_cita(create_test_mascota):
    # Campos corregidos para AppointmentCreate
    cita_data = {
        "date_time": "2024-12-15T09:00:00Z", 
        "reason": "Control veterinario",     
        "pet_id": create_test_mascota
    }
    # Ruta corregida: /appointments/
    response = client.post("/appointments/", json=cita_data)
    assert response.status_code == 201
    return response.json()["id"]

def test_create_factura(create_test_cita):
    # Campos corregidos para InvoiceCreate: appointment_id, amount, details
    factura_data = {
        "appointment_id": create_test_cita,
        "amount": 100.50, 
        "details": "Consulta y vacunas", 
        "paid": False 
    }
    # Ruta corregida: /billing/
    response = client.post("/billing/", json=factura_data)
    
    assert response.status_code == 201
    response_json = response.json()
    assert "id" in response_json
    assert response_json["amount"] == 100.50

def test_list_all_facturas():
    # Ruta corregida: /billing/
    response = client.get("/billing/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
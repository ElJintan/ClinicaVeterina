import pytest
from fastapi.testclient import TestClient
# Esta importación ahora debería funcionar gracias a pytest.ini
from src.main import app 

client = TestClient(app)

@pytest.fixture
def create_test_cliente():
    # Usando los nombres de campos del modelo (name, email, phone)
    cliente_data = {
        "name": "Test Cliente",
        "email": "test@example.com",
        "phone": "987654321", 
        "address": "Calle Falsa 123"
    }
    # Endpoint corregido: /clients/
    response = client.post("/clients/", json=cliente_data)
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def create_test_mascota(create_test_cliente):
    # Usando los nombres de campos del modelo (name, species, birthdate)
    mascota_data = {
        "client_id": create_test_cliente, 
        "name": "Firulais",
        "species": "Perro",
        "raza": "Labrador",
        "birthdate": "2020-05-10"
    }
    # Endpoint corregido: /pets/
    response = client.post("/pets/", json=mascota_data)
    assert response.status_code == 201
    return response.json()["id"]

def test_create_cita(create_test_cliente, create_test_mascota):
    # Usando los nombres de campos del modelo AppointmentCreate (date_time, reason, pet_id)
    cita_data = {
        "date_time": "2024-12-15T09:00:00Z",
        "reason": "Control veterinario",
        "pet_id": create_test_mascota
    }

    # Endpoint corregido: /appointments/
    response = client.post("/appointments/", json=cita_data)
    
    assert response.status_code == 201
    assert response.json()["pet_id"] == create_test_mascota
    assert response.json()["reason"] == "Control veterinario" 


def test_update_cita(create_test_cliente, create_test_mascota):
    # 1. Crear Cita
    cita_create_data = {
        "date_time": "2024-12-15T09:00:00Z",
        "reason": "Control veterinario",
        "pet_id": create_test_mascota
    }

    create_response = client.post("/appointments/", json=cita_create_data)
    assert create_response.status_code == 201
    cita_id = create_response.json()["id"]

    # 2. Actualizar Cita
    update_data = {
        "date_time": "2024-12-15T11:00:00Z",
        "reason": "Consulta general", 
    }

    # Endpoint corregido: /appointments/{cita_id}
    update_response = client.put(f"/appointments/{cita_id}", json=update_data)
    
    assert update_response.status_code == 200
    assert update_response.json()["reason"] == "Consulta general"

def test_delete_cita(create_test_cliente, create_test_mascota):
    # 1. Crear Cita
    cita_create_data = {
        "date_time": "2024-12-15T09:00:00Z",
        "reason": "Control veterinario",
        "pet_id": create_test_mascota
    }

    create_response = client.post("/appointments/", json=cita_create_data)
    assert create_response.status_code == 200
    cita_id = create_response.json()["id"]

    # 2. Eliminar Cita
    # Endpoint corregido: /appointments/{cita_id}
    delete_response = client.delete(f"/appointments/{cita_id}")
    
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Cita eliminada" 

    # 3. Verificar que se eliminó
    get_response = client.get(f"/appointments/{cita_id}")
    assert get_response.status_code == 404


def test_get_all_citas():
    # Endpoint corregido: /appointments/
    response = client.get("/appointments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
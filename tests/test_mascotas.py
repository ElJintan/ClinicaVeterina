import pytest
from fastapi.testclient import TestClient
from src.main import app 

client = TestClient(app)

# Fixture para crear un cliente (la mascota necesita un dueño válido)
@pytest.fixture
def create_test_cliente():
    # 💡 CORRECCIÓN: Usando campos del modelo Cliente: name, email, phone
    cliente_data = {
        "name": "Cliente Dueño Test",
        "email": "owner@example.com",
        "phone": "999111222", 
        "address": "Dirección Cliente"
    }
    # 💡 Ruta corregida: /clients/
    response = client.post("/clients/", json=cliente_data)
    assert response.status_code == 201
    return response.json()["id"]

@pytest.fixture
def mascota_data(create_test_cliente):
    # 💡 CORRECCIÓN: Usando campos del modelo PetCreate
    return {
        "client_id": create_test_cliente, # ID del cliente creado
        "name": "Firulais", 
        "species": "Perro",
        "breed": "Labrador",
        "birthdate": "2021-05-10" 
    }

def test_create_mascota(mascota_data):
    # 💡 Ruta corregida: /pets/
    response = client.post("/pets/", json=mascota_data)
    assert response.status_code == 201 
    assert "id" in response.json()

def test_get_mascota(mascota_data):
    # 1. Crear mascota
    create_response = client.post("/pets/", json=mascota_data)
    mascota_id = create_response.json()["id"]

    # 2. Obtener mascota
    # 💡 Ruta corregida: /pets/{id}
    response = client.get(f"/pets/{mascota_id}")
    assert response.status_code == 200
    # 💡 Campo corregido: "nombre" -> "name"
    assert response.json()["name"] == mascota_data["name"]

def test_update_mascota(mascota_data):
    # 1. Crear mascota
    create_response = client.post("/pets/", json=mascota_data)
    mascota_id = create_response.json()["id"]

    # 2. Actualizar mascota
    updated_data = {"name": "Firu actualizado"} 
    # 💡 Ruta corregida: /pets/{id}
    response = client.put(f"/pets/{mascota_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Firu actualizado"

def test_delete_mascota(mascota_data):
    # 1. Crear mascota
    create_response = client.post("/pets/", json=mascota_data)
    mascota_id = create_response.json()["id"]

    # 2. Eliminar mascota
    # 💡 Ruta corregida: /pets/{id}
    response = client.delete(f"/pets/{mascota_id}")
    assert response.status_code == 204 # El delete en el controlador devuelve 204 No Content

    # 3. Verificar que la mascota no existe
    response = client.get(f"/pets/{mascota_id}")
    assert response.status_code == 404

def test_get_all_mascotas(mascota_data):
    client.post("/pets/", json=mascota_data)

    # 💡 Ruta corregida: /pets/
    response = client.get("/pets/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
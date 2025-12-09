# tests/test_clientes.py (Código completo y corregido)
import pytest
from fastapi.testclient import TestClient
from src.main import app 

client = TestClient(app)

cliente_data = {
    "name": "Cliente Test",
    "email": "cliente@example.com",
    "phone": "123456789", 
    "address": "Dirección 1" 
}

@pytest.fixture
def create_test_cliente():
    response = client.post("/clients/", json=cliente_data)
    assert response.status_code == 201
    return response.json()["id"]

def test_create_cliente():
    response = client.post("/clients/", json=cliente_data)
    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"]

def test_get_cliente(create_test_cliente):
    cliente_id = create_test_cliente
    response = client.get(f"/clients/{cliente_id}")
    assert response.status_code == 200
    cliente = response.json()
    assert cliente["name"] == cliente_data["name"]

def test_update_cliente(create_test_cliente):
    cliente_id = create_test_cliente
    update_data = {"name": "Cliente Actualizado"} 
    response = client.put(f"/clients/{cliente_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Cliente actualizado" 

    response = client.get(f"/clients/{cliente_id}")
    assert response.status_code == 200
    cliente = response.json()
    assert cliente["name"] == "Cliente Actualizado"

def test_delete_cliente(create_test_cliente):
    cliente_id = create_test_cliente
    response = client.delete(f"/clients/{cliente_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Cliente y sus mascotas eliminados" 

    response = client.get(f"/clients/{cliente_id}")
    assert response.status_code == 404

def test_get_all_clientes(create_test_cliente):
    response = client.get("/clients/")
    assert response.status_code == 200
    clientes = response.json()
    assert isinstance(clientes, list)
    assert any(cliente["name"] == cliente_data["name"] for cliente in clientes)
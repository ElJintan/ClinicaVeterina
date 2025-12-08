# streamlit_app/api_client.py - CÓDIGO COMPLETO
import requests
import streamlit as st
import json

# Usamos el nombre del servicio Docker Compose 'backend'
API_BASE_URL = "http://backend:8000" 

@st.cache_data(ttl=60)
def fetch_data(endpoint: str):
    """Función genérica para obtener datos de la API (GET)."""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Error: No se pudo conectar con la API en {API_BASE_URL}. Asegúrate de que el contenedor 'backend' esté activo.")
        return []
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get('detail', e.response.reason)
        except:
            detail = e.response.reason
        st.error(f"Error HTTP al obtener datos de {endpoint}: {e.response.status_code} - {detail}")
        return []

def post_data(endpoint: str, data: dict):
    """Función genérica para enviar datos a la API (POST)."""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.post(url, json=data, timeout=5)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Error: No se pudo conectar con la API en {API_BASE_URL} durante la creación.")
        return None
    except requests.exceptions.HTTPError as e:
        try:
            detail = e.response.json().get('detail', e.response.reason)
        except:
            detail = e.response.reason
        st.error(f"Error al crear {endpoint}: {e.response.status_code} - {detail}")
        return None

# --- Funciones CRUD específicas ---

def get_clients():
    return fetch_data('clients')

def create_client(name: str, email: str, phone: str, address: str):
    data = {"name": name, "email": email, "phone": phone, "address": address}
    return post_data('clients', data) 

def get_pets_by_client(client_id: str):
    return fetch_data(f'pets?owner_id={client_id}') 

def create_pet(name: str, species: str, breed: str, age: int, owner_id: str):
    data = {"name": name, "species": species, "breed": breed, "age": age, "owner_id": owner_id}
    return post_data('pets', data) 

def create_appointment(pet_id: str, date: str, time: str, reason: str):
    # Formato requerido por el backend (ISO 8601)
    datetime_str = f"{date}T{time}:00" 
    data = {"pet_id": pet_id, "date_time": datetime_str, "reason": reason}
    return post_data('appointments', data)

# ... (resto de funciones simuladas) ...
def get_medical_records(pet_id: str):
    return [
        {"date": "2025-10-01", "reason": "Vacunación anual", "diagnosis": "Salud óptima", "treatment": "Vacuna Triple Canina"},
        {"date": "2025-05-15", "reason": "Tos y letargo", "diagnosis": "Bronquitis leve", "treatment": "Antibióticos por 7 días"}
    ]
def get_invoices():
    return [
        {"id": "INV-001", "client": "Cliente A", "date": "2025-11-20", "total": 45.00, "status": "Paid"},
        {"id": "INV-002", "client": "Cliente B", "date": "2025-11-25", "total": 120.50, "status": "Pending"},
    ]
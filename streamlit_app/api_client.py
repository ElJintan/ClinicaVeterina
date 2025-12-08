# streamlit_app/api_client.py
import requests
import streamlit as st

# Usamos el nombre del servicio Docker Compose 'backend'
API_BASE_URL = "http://backend:8000" 

@st.cache_data(ttl=60)
def fetch_data(endpoint: str):
    """Función genérica para obtener datos de la API."""
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Error: No se pudo conectar con la API en {API_BASE_URL}. Asegúrate de que el contenedor 'backend' esté activo.")
        return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos de {endpoint}: {e}")
        return []

# --- Funciones específicas ---

def get_clients():
    return fetch_data('clients')

def get_pets_by_client(client_id: str):
    return fetch_data(f'pets?owner_id={client_id}') # Asumiendo un endpoint de filtrado

# Función para la nueva sección de Historial Médico
def get_medical_records(pet_id: str):
    return [
        {"date": "2025-10-01", "reason": "Vacunación anual", "diagnosis": "Salud óptima", "treatment": "Vacuna Triple Canina"},
        {"date": "2025-05-15", "reason": "Tos y letargo", "diagnosis": "Bronquitis leve", "treatment": "Antibióticos por 7 días"}
    ]

# Función para la nueva sección de Facturación
def get_invoices():
    return [
        {"id": "INV-001", "client": "Cliente A", "date": "2025-11-20", "total": 45.00, "status": "Paid"},
        {"id": "INV-002", "client": "Cliente B", "date": "2025-11-25", "total": 120.50, "status": "Pending"},
    ]
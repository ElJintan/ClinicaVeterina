# streamlit_app/api_client.py - CÓDIGO COMPLETO MODIFICADO PARA DESACOPLAMIENTO
import requests
import streamlit as st
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

API_BASE_URL = "http://backend:8000" 

@st.cache_data(ttl=60)
def fetch_data(endpoint: str) -> List[Dict[str, Any]]:
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Error: No se pudo conectar con la API en {API_BASE_URL}.")
        return []
    except requests.exceptions.HTTPError as e:
        # FIX: Intentar obtener el JSON de error, si falla, usar el texto
        detail = e.response.reason
        try:
            detail = e.response.json().get('detail', e.response.reason)
        except json.JSONDecodeError:
             # Si el backend devuelve texto plano o un error 500 que no es JSON, esto evita el crash
             pass
        
        if e.response.status_code >= 500:
            st.error(f"Error interno del servidor (500): {detail}")
        # Si es 404, devuelve lista vacía sin error.
        return []


def post_data(endpoint: str, data: dict) -> Optional[Dict[str, Any]]:
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        # Limpiamos los valores None/vacíos antes de enviar, Pydantic/FastAPI lo agradecerán.
        cleaned_data = {k: v for k, v in data.items() if v is not None}
        
        response = requests.post(url, json=cleaned_data, timeout=5)
        response.raise_for_status() 
        st.cache_data.clear() # LIMPIEZA GLOBAL CRÍTICA
        return response.json()
    except requests.exceptions.HTTPError as e:
        detail = e.response.reason
        try:
            detail = e.response.json().get('detail', e.response.reason)
        except json.JSONDecodeError:
            pass
        st.error(f"Error al crear {endpoint}: {e.response.status_code} - {detail}")
        return None

def delete_data(endpoint: str) -> bool:
    url = f"{API_BASE_URL}/{endpoint}"
    try:
        response = requests.delete(url, timeout=5)
        response.raise_for_status() 
        st.cache_data.clear() # LIMPIEZA GLOBAL CRÍTICA
        return True
    except requests.exceptions.HTTPError as e:
        # FIX CRÍTICO: Manejar JSONDecodeError en DELETE
        detail = e.response.reason
        try:
            # Intenta obtener el error JSON del backend (si lo devuelve)
            detail = e.response.json().get('detail', e.response.reason)
        except json.JSONDecodeError:
            # Si llegó aquí con un 404/500 y no había JSON, mostramos el código de estado.
            if e.response.status_code == 404:
                st.warning(f"No se encontró el recurso a eliminar en {endpoint}.")
                return False

        st.error(f"Error al eliminar {endpoint}: {e.response.status_code} - {detail}")
        return False
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión al eliminar {endpoint}: {e}")
        return False

# --- Funciones CRUD Específicas (MODIFICADAS) ---

# CLIENTES (No cambiaron las reglas de negocio, solo se limpia la caché)
def get_clients(): return fetch_data('clients')
def create_client(name, email, phone, address):
    return post_data('clients', {"name": name, "email": email, "phone": phone, "address": address})
def delete_client(client_id):
    return delete_data(f'clients/{client_id}')

# MASCOTAS (Decoupled: Eliminado owner_id, cambiado age por birthdate)
def get_pets(): return fetch_data('pets') # Nueva función para listar TODAS las mascotas
# Eliminado: get_pets_by_client

def create_pet(name, species, breed, birthdate): 
    # birthdate puede ser None o ""
    data = {
        "name": name, 
        "species": species, 
        "breed": breed if breed else None, 
        "birthdate": birthdate if birthdate else None
    }
    return post_data('pets', data)
def delete_pet(pet_id):
    return delete_data(f'pets/{pet_id}')

# CITAS (pet_id es opcional)
def get_appointments(): return fetch_data('appointments')
def create_appointment(pet_id, date, time, reason):
    datetime_str = f"{date}T{time}:00" 
    # pet_id puede ser None
    data = {
        "pet_id": pet_id if pet_id else None,
        "date_time": datetime_str,
        "reason": reason
    }
    return post_data('appointments', data)
def delete_appointment(appointment_id):
    return delete_data(f'appointments/{appointment_id}')

# HISTORIAL MÉDICO (pet_id es opcional)
def get_medical_records_by_pet(pet_id): return fetch_data(f'medical_records?pet_id={pet_id}')
def create_medical_record(pet_id, diagnosis, treatment, medication, notes):
    # pet_id puede ser None
    data = {
        "pet_id": pet_id if pet_id else None,
        "diagnosis": diagnosis, 
        "treatment": treatment, 
        "medication": medication if medication else None, 
        "notes": notes if notes else None
    }
    return post_data('medical_records', data)
def delete_medical_record(record_id): return delete_data(f'medical_records/{record_id}')

# FACTURACIÓN (Decoupled: client_id cambia a client_name, appointment_id eliminado)
def get_invoices(): return fetch_data('billing')
def create_invoice(client_name, amount, details, paid=False):
    # El campo es ahora client_name (referencia textual opcional), y ya no hay appointment_id
    data = {
        "client_name": client_name if client_name else None,
        "amount": amount, 
        "details": details, 
        "paid": paid
    }
    return post_data('billing', data)
def delete_invoice(invoice_id):
    return delete_data(f'billing/{invoice_id}')
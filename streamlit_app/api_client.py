import requests
import os

# Usamos el nombre del servicio 'backend' si estamos en docker, o localhost si es local
API_URL = os.getenv("API_URL", "http://backend:8000")

class APIClient:
    def __init__(self):
        self.base_url = API_URL

    # --- CLIENTS ---
    def get_clients(self):
        try:
            response = requests.get(f"{self.base_url}/clients/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching clients: {e}")
            return []

    def create_client(self, data: dict):
        response = requests.post(f"{self.base_url}/clients/", json=data)
        return response

    def delete_client(self, client_id: str):
        response = requests.delete(f"{self.base_url}/clients/{client_id}")
        return response

    # --- PETS ---
    def get_pets(self):
        try:
            response = requests.get(f"{self.base_url}/pets/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching pets: {e}")
            return []

    def create_pet(self, data: dict):
        response = requests.post(f"{self.base_url}/pets/", json=data)
        return response

    def delete_pet(self, pet_id: str):
        response = requests.delete(f"{self.base_url}/pets/{pet_id}")
        return response

    # --- APPOINTMENTS ---
    def get_appointments(self):
        try:
            response = requests.get(f"{self.base_url}/appointments/")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching appointments: {e}")
            return []

    def create_appointment(self, data: dict):
        response = requests.post(f"{self.base_url}/appointments/", json=data)
        return response

    def delete_appointment(self, appointment_id: str):
        response = requests.delete(f"{self.base_url}/appointments/{appointment_id}")
        return response
    
    # --- MEDICAL RECORDS ---
    def get_medical_records(self, pet_id: str):
        try:
            response = requests.get(f"{self.base_url}/medical-records/pet/{pet_id}")
            response.raise_for_status()
            return response.json()
        except Exception:
            return []

    def create_medical_record(self, data: dict):
        return requests.post(f"{self.base_url}/medical-records/", json=data)

    # --- BILLING ---
    def get_invoices(self):
        try:
            return requests.get(f"{self.base_url}/billing/").json()
        except:
            return []
            
    def create_invoice(self, data: dict):
        return requests.post(f"{self.base_url}/billing/", json=data)
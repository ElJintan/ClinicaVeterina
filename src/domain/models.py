# src/domain/models.py - Modelos simplificados sin IDs de relación obligatorios
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# --- Modelos Base (Entidades con ID) ---

class Client(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    # Email como str simple para evitar la validación estricta 422
    email: str 
    phone: str
    address: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Pet(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    species: str
    breed: Optional[str] = None
    birthdate: Optional[str] = None
    # Campo 'owner_name' eliminado
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Appointment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    # pet_id ahora es opcional
    pet_id: Optional[str] = None
    veterinarian_id: Optional[str] = "Vet-General"
    date_time: datetime 
    reason: str
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

# --- Modelos de Creación (Input DTOs para POST) ---

class ClientCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: Optional[str] = None

class PetCreate(BaseModel):
    name: str
    species: str
    breed: Optional[str] = None
    birthdate: Optional[str] = None
    # Campo 'owner_name' eliminado

class AppointmentCreate(BaseModel):
    # pet_id ahora es opcional
    pet_id: Optional[str] = None
    veterinarian_id: Optional[str] = "Vet-General"
    date_time: datetime
    reason: str
    status: AppointmentStatus = AppointmentStatus.SCHEDULED

# --- Modelos de Actualización (Input DTOs para PUT/PATCH) ---

class ClientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class PetUpdate(BaseModel):
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    birthdate: Optional[str] = None
    # Campo 'owner_name' eliminado
    
class AppointmentUpdate(BaseModel):
    # pet_id es opcional para actualización
    pet_id: Optional[str] = None
    veterinarian_id: Optional[str] = None
    date_time: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[AppointmentStatus] = None

# --- Nuevas Funcionalidades ---

class MedicalRecord(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    # pet_id ahora es opcional
    pet_id: Optional[str] = None
    date: datetime = Field(default_factory=datetime.now)
    diagnosis: str
    treatment: str
    medication: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class MedicalRecordCreate(BaseModel):
    # pet_id ahora es opcional
    pet_id: Optional[str] =
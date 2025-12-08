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
    # Ya no es un ID, es solo un nombre para mostrar
    owner_name: Optional[str] = "Desconocido"
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class Appointment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    pet_id: str
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
    # Campo simplificado sin necesidad de validar un ID existente
    owner_name: Optional[str] = "Desconocido" 

class AppointmentCreate(BaseModel):
    pet_id: str
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
    owner_name: Optional[str] = None 
    
class AppointmentUpdate(BaseModel):
    pet_id: Optional[str] = None
    veterinarian_id: Optional[str] = None
    date_time: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[AppointmentStatus] = None

# --- Nuevas Funcionalidades ---

class MedicalRecord(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    pet_id: str
    date: datetime = Field(default_factory=datetime.now)
    diagnosis: str
    treatment: str
    medication: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class MedicalRecordCreate(BaseModel):
    pet_id: str
    diagnosis: str
    treatment: str
    medication: Optional[str] = None
    notes: Optional[str] = None

class MedicalRecordUpdate(BaseModel):
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medication: Optional[str] = None
    notes: Optional[str] = None

class Invoice(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    # Ya no es un ID, es solo un nombre para mostrar
    client_name: Optional[str] = "Desconocido"
    appointment_id: Optional[str] = None
    amount: float
    date: datetime = Field(default_factory=datetime.now)
    paid: bool = False
    details: str
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class InvoiceCreate(BaseModel):
    # Campo simplificado sin necesidad de validar un ID existente
    client_name: Optional[str] = "Desconocido"
    appointment_id: Optional[str] = None
    amount: float
    paid: bool = False
    details: str
    
class InvoiceUpdate(BaseModel):
    amount: Optional[float] = None
    paid: Optional[bool] = None
    details: Optional[str] = None

class Feedback(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    appointment_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
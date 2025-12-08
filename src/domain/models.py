# src/domain/models.py - Modelos desacoplados y simplificados
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
    # Campo 'owner_name' eliminado para desacoplamiento total
    
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

class AppointmentCreate(BaseModel):
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
    
class AppointmentUpdate(BaseModel):
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
    pet_id: Optional[str] = None
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
    # client_name ahora es simplemente opcional
    client_name: Optional[str] = None
    # appointment_id ahora es opcional/eliminado para desacoplar facturas
    appointment_id: Optional[str] = None
    amount: float
    date: datetime = Field(default_factory=datetime.now)
    paid: bool = False
    details: str
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class InvoiceCreate(BaseModel):
    client_name: Optional[str] = None
    appointment_id: Optional[str] = None
    amount: float
    paid: bool = False
    details: str
    
class InvoiceUpdate(BaseModel):
    amount: Optional[float] = None
    paid: Optional[bool] = None
    details: Optional[str] = None
    client_name: Optional[str] = None 

class Feedback(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    # appointment_id ahora es opcional
    appointment_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
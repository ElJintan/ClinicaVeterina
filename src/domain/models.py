from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AppointmentStatus(str, Enum):
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

# --- Modelos Base ---

class Client(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    email: EmailStr
    phone: str
    address: Optional[str] = None

class Pet(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    name: str
    species: str
    breed: Optional[str] = None
    birthdate: Optional[str] = None
    owner_id: str

class Appointment(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    pet_id: str
    veterinarian_id: Optional[str] = "Vet-General"
    date: datetime
    reason: str
    status: AppointmentStatus = AppointmentStatus.SCHEDULED

# --- Nuevas Funcionalidades ---

class MedicalRecord(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    pet_id: str
    date: datetime = Field(default_factory=datetime.now)
    diagnosis: str
    treatment: str
    medication: Optional[str] = None
    notes: Optional[str] = None

class Invoice(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    client_id: str
    appointment_id: Optional[str] = None
    amount: float
    date: datetime = Field(default_factory=datetime.now)
    paid: bool = False
    details: str

class Feedback(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    appointment_id: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
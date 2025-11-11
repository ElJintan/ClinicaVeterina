from pydantic import BaseModel, Field
from typing import Optional

class Client(BaseModel):
    id: Optional[str] = Field(None, example="client123")
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None

class Pet(BaseModel):
    id: Optional[str] = Field(None, example="pet123")
    name: str
    species: str
    breed: Optional[str] = None
    birthdate: Optional[str] = None
    owner_id: Optional[str] = None

class Appointment(BaseModel):
    id: Optional[str] = Field(None, example="appt123")
    pet_id: str
    veterinarian_id: Optional[str] = None
    date: str
    reason: Optional[str] = None
    status: Optional[str] = "scheduled"

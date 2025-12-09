# src/controllers/__init__.py

from .clients_controller import router as clients_controller
from .pets_controller import router as pets_controller
from .appointments_controller import router as appointments_controller
from .medical_records_controller import router as medical_records_controller
from .billing_controller import router as billing_controller
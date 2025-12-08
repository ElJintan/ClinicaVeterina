import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime
from src.services.medical_service import MedicalService
from src.domain.models import Pet
from src.exceptions import NotFoundException

# Decorador para tests asíncronos
@pytest.mark.asyncio
async def test_add_diagnosis_success():
    # Arrange
    mock_med_repo = AsyncMock()
    mock_pet_repo = AsyncMock()
    
    # Simulamos que la mascota existe
    mock_pet_repo.get_by_id.return_value = Pet(
        _id="pet123", name="Firu", species="Dog", owner_id="owner1"
    )
    mock_med_repo.add_entry.return_value = "record_new_id"

    service = MedicalService(mock_med_repo, mock_pet_repo)

    # Act
    result = await service.add_diagnosis("pet123", "Otitis", "Limpieza")

    # Assert
    assert result == "record_new_id"
    mock_med_repo.add_entry.assert_called_once()

@pytest.mark.asyncio
async def test_add_diagnosis_pet_not_found():
    # Arrange
    mock_med_repo = AsyncMock()
    mock_pet_repo = AsyncMock()
    
    # Simulamos que la mascota NO existe
    mock_pet_repo.get_by_id.return_value = None

    service = MedicalService(mock_med_repo, mock_pet_repo)

    # Act & Assert
    with pytest.raises(NotFoundException):
        await service.add_diagnosis("pet_fake", "Algo", "Nada")
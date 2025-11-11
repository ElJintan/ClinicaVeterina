from src.domain.models import Client, Pet, Appointment

def test_models_exist():
    c = Client(name='Test', email='t@example.com')
    assert c.name == 'Test'
    p = Pet(name='Fido', species='Perro')
    assert p.species == 'Perro'
    a = Appointment(pet_id='pet1', date='2099-01-01T10:00')
    assert a.pet_id == 'pet1'

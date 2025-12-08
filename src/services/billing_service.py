from src.interfaces.repositories import IBillingRepository, IClientRepository
from src.domain.models import Invoice
from src.exceptions import NotFoundException

class BillingService:
    def __init__(self, billing_repo: IBillingRepository, client_repo: IClientRepository):
        self.billing_repo = billing_repo
        self.client_repo = client_repo

    async def create_invoice(self, client_id: str, amount: float, details: str, appointment_id: str = None) -> str:
        client = await self.client_repo.get_by_id(client_id)
        if not client:
            raise NotFoundException(f"Cliente {client_id} no encontrado")
        
        invoice = Invoice(
            client_id=client_id,
            appointment_id=appointment_id,
            amount=amount,
            details=details
        )
        return await self.billing_repo.create_invoice(invoice)
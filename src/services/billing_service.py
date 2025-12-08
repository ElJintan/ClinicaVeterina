# src/services/billing_service.py - CÓDIGO COMPLETO Y FINAL (NUEVO)
from typing import List, Optional
from src.interfaces.repositories import IBillingRepository
from src.interfaces.logger import ILogger
from src.domain.models import Invoice, InvoiceCreate, InvoiceUpdate
from src.infrastructure.logger_impl import LoggerImpl

class BillingService:
    def __init__(self, repo: IBillingRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_invoice(self, invoice_data: InvoiceCreate) -> Invoice:
        self.logger.info(f"Creando factura para cliente: {invoice_data.client_id}")
        invoice_model = Invoice(**invoice_data.dict())
        invoice_id = await self.repo.create(invoice_model)
        return await self.repo.get(invoice_id)

    async def list_invoices(self) -> List[Invoice]:
        self.logger.info("Consultando todas las facturas.")
        return await self.repo.list()

    async def update_invoice(self, invoice_id: str, updates: InvoiceUpdate) -> Optional[Invoice]:
        updates_dict = updates.dict(exclude_none=True)
        if not updates_dict: return await self.repo.get(invoice_id)
        return await self.repo.update(invoice_id, updates_dict)

    async def delete_invoice(self, invoice_id: str) -> bool:
        return await self.repo.delete(invoice_id)
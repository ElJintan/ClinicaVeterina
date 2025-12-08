# src/services/billing_service.py - CÓDIGO SIN FILTRADO POR CLIENTE
from typing import List, Optional
from src.interfaces.repositories import IBillingRepository
from src.interfaces.logger import ILogger
from src.domain.models import Invoice, InvoiceCreate, InvoiceUpdate
from src.infrastructure.logger_impl import LoggerImpl
from src.exceptions import RepositoryException, NotFoundException 

class BillingService:
    def __init__(self, repo: IBillingRepository, logger: ILogger = None):
        self.repo = repo
        self.logger = logger or LoggerImpl(self.__class__.__name__)

    async def create_invoice(self, invoice_data: InvoiceCreate) -> Invoice:
        self.logger.info(f"Creando factura para cliente: {invoice_data.client_name}")
        try:
            invoice_id = await self.repo.create(invoice_data)
            new_invoice = await self.repo.get(invoice_id)
            if not new_invoice:
                raise RepositoryException("Factura creada pero falló al recuperar.")
            return new_invoice
        except Exception as e:
            self.logger.exception("Error creando factura")
            raise RepositoryException("Error interno del servidor al crear factura") from e


    async def list_invoices(self) -> List[Invoice]:
        # ELIMINADO: el parámetro client_id y la lógica de filtrado
        self.logger.info("Consultando todas las facturas.")
        return await self.repo.list()

    async def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        self.logger.debug(f"Buscando factura por ID: {invoice_id}")
        return await self.repo.get(invoice_id)
        
    async def update_invoice(self, invoice_id: str, updates: InvoiceUpdate) -> Optional[Invoice]:
        self.logger.info(f"Actualizando factura ID: {invoice_id}")
        updates_dict = updates.dict(exclude_none=True)
        if not updates_dict: return await self.repo.get(invoice_id)
        
        updated_invoice = await self.repo.update(invoice_id, updates_dict)
        if not updated_invoice:
            raise NotFoundException(f"Factura {invoice_id} no encontrada o no se pudo actualizar.")
        return updated_invoice

    async def delete_invoice(self, invoice_id: str) -> bool:
        self.logger.warning(f"Eliminando factura ID: {invoice_id}")
        return await self.repo.delete(invoice_id)
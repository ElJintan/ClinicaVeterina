# src/controllers/billing_controller.py (NUEVO)
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List, Optional
from src.domain.models import Invoice, InvoiceCreate, InvoiceUpdate
from src.services.billing_service import BillingService
from src.exceptions import NotFoundException
from src.repositories.mongo_repo import MongoBillingRepository
from src.infrastructure.logger_impl import LoggerImpl

router = APIRouter()

def get_billing_service() -> BillingService:
    repo = MongoBillingRepository()
    logger = LoggerImpl(BillingService.__name__)
    return BillingService(repo=repo, logger=logger)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Invoice)
async def create_invoice_endpoint(invoice_create: InvoiceCreate, svc: BillingService = Depends(get_billing_service)):
    try:
        invoice = await svc.create_invoice(invoice_create)
        return invoice
    except Exception as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[Invoice])
async def list_invoices_endpoint(client_id: Optional[str] = None, svc: BillingService = Depends(get_billing_service)):
    return await svc.list_invoices() 

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice_endpoint(invoice_id: str, svc: BillingService = Depends(get_billing_service)):
    success = await svc.delete_invoice(invoice_id)
    if not success: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada o no se pudo eliminar.")
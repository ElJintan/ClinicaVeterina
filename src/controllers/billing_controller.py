# src/controllers/billing_controller.py - NUEVO
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

# POST: Crea Factura
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Invoice)
async def create_invoice_endpoint(invoice_create: InvoiceCreate, svc: BillingService = Depends(get_billing_service)):
    try:
        invoice = await svc.create_invoice(invoice_create)
        return invoice
    except Exception as e: raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# GET: Lista Facturas
@router.get("/", response_model=List[Invoice])
async def list_invoices_endpoint(client_id: Optional[str] = None, svc: BillingService = Depends(get_billing_service)):
    # Simulación de filtrado, asumimos list_invoices soporta un client_id query param
    return await svc.list_invoices() 

# PUT: Actualiza Factura (p. ej. marcar como pagada)
@router.put("/{invoice_id}", response_model=Invoice)
async def update_invoice_endpoint(invoice_id: str, updates: InvoiceUpdate, svc: BillingService = Depends(get_billing_service)):
    try:
        invoice = await svc.update_invoice(invoice_id, updates)
        if not invoice: raise NotFoundException("Factura no encontrada.")
        return invoice
    except NotFoundException as e: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

# DELETE: Elimina Factura
@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_invoice_endpoint(invoice_id: str, svc: BillingService = Depends(get_billing_service)):
    success = await svc.delete_invoice(invoice_id)
    if not success: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Factura no encontrada o no se pudo eliminar.")
    return
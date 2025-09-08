from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.payment_schema import PaymentInvoiceCreate, PaymentInvoiceOut
from services.payment_service import (
    create_payment_invoice,
    approve_payment_finance,
    approve_payment_president,
    get_pending_invoices
)
from models.user_model import User
from utils.dependencies import get_current_user

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/", response_model=PaymentInvoiceOut)
def create_invoice(data: PaymentInvoiceCreate, db: Session = Depends(get_db)):
    return create_payment_invoice(db, data)

@router.post("/{invoice_id}/approve-finance", response_model=PaymentInvoiceOut)
def approve_finance(invoice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return approve_payment_finance(db, invoice_id, current_user)

@router.post("/{invoice_id}/approve-president", response_model=PaymentInvoiceOut)
def approve_president(invoice_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return approve_payment_president(db, invoice_id, current_user)

@router.get("/pending", response_model=list[PaymentInvoiceOut])
def list_pending_invoices(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_pending_invoices(db, current_user)

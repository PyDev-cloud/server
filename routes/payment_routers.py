from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.payment_schema import PaymentInvoiceCreate, PaymentInvoiceOut
from services.payment_service import (
    create_payment_invoice,
    approve_payment_finance,
    approve_payment_president,
    get_pending_invoices,
    get_user_payment_status,
)
from models.user_model import User
from utils.permissions import require_roles
from utils.dependencies import get_current_user

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/", response_model=PaymentInvoiceOut)
async def create_invoice(
    data: PaymentInvoiceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="আপনি শুধু নিজের ইনভয়েস তৈরি করতে পারেন")
    return create_payment_invoice(db, data, current_user)


@router.post("/{invoice_id}/approve-Finance-Secretary", response_model=PaymentInvoiceOut)
async def approve_finance(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("Finance Secretary"))
):
    return approve_payment_finance(db, invoice_id, current_user)


@router.post("/{invoice_id}/approve-President", response_model=PaymentInvoiceOut)
async def approve_president(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("President"))
):
    return approve_payment_president(db, invoice_id, current_user)


@router.get("/pending", response_model=list[PaymentInvoiceOut])
async def list_pending_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_pending_invoices(db, current_user)


@router.get("/my-payments", response_model=list[PaymentInvoiceOut])
async def my_payment_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_payment_status(db, current_user.id)

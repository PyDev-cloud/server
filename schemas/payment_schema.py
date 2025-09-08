from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from models.payment_model import InvoiceStatus

class PaymentInvoiceCreate(BaseModel):
    user_id: int
    transaction_id: str
    payment_slip: Optional[str] = None
    amount: float
    payment_type: str
    account_number: Optional[str] = None

    model_config = {"from_attributes": True}

class PaymentDeductionOut(BaseModel):
    installment_id: int
    amount: float

    model_config = {"from_attributes": True}

class PaymentInvoiceOut(BaseModel):
    id: int
    user_id: int
    date: date
    transaction_id: str
    payment_slip: Optional[str]
    amount: float
    payment_type: str
    account_number: Optional[str]
    approved_by_finance: bool
    approved_by_president: bool
    status: InvoiceStatus
    deductions: List[PaymentDeductionOut] = []

    model_config = {"from_attributes": True}

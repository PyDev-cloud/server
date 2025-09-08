from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.payment_model import PaymentInvoice, PaymentDeduction, InvoiceStatus
from models.instalment_model import Instalment
from models.user_account_Model import UserAccount
from models.user_model import User
from schemas.payment_schema import PaymentInvoiceCreate
from utils.permissions import require_role

# -------------------
# Create Payment Invoice
# -------------------
def create_payment_invoice(db: Session, invoice_data: PaymentInvoiceCreate) -> PaymentInvoice:
    invoice = PaymentInvoice(
        **invoice_data.model_dump(),
        status=InvoiceStatus.PENDING.value,
        approved_by_finance=False,
        approved_by_president=False
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

# -------------------
# Finance Approve
# -------------------
@require_role("finance")
def approve_payment_finance(db: Session, invoice_id: int, user: User) -> PaymentInvoice:
    invoice: PaymentInvoice = db.get(PaymentInvoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice.approved_by_finance:
        return invoice

    invoice.approved_by_finance = True
    invoice.status = InvoiceStatus.FINANCE_APPROVED.value
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return invoice

# -------------------
# President Approve + Deduct Installments + Update Account
# -------------------
@require_role("president")
def approve_payment_president(db: Session, invoice_id: int, user: User) -> PaymentInvoice:
    invoice: PaymentInvoice = db.get(PaymentInvoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if not invoice.approved_by_finance:
        raise HTTPException(status_code=400, detail="Finance approval required first")
    if invoice.approved_by_president:
        return invoice

    with db.begin():  # transaction-safe
        invoice.approved_by_president = True
        invoice.status = InvoiceStatus.PRESIDENT_APPROVED.value
        db.add(invoice)

        # Deduct from installments
        remaining_amount = float(invoice.amount)
        user_instalments = (
            db.query(Instalment)
            .filter(Instalment.user_id == invoice.user_id)
            .order_by(Instalment.id)
            .all()
        )

        for inst in user_instalments:
            if float(inst.amount_due) <= 0:
                continue
            deduct = min(float(inst.amount_due), remaining_amount)
            inst.amount_due = float(inst.amount_due) - deduct
            remaining_amount -= deduct
            db.add(inst)

            deduction = PaymentDeduction(invoice_id=invoice.id, installment_id=inst.id, amount=deduct)
            db.add(deduction)

            if remaining_amount <= 0:
                break

        # Update or create user account
        account: UserAccount = db.query(UserAccount).filter(UserAccount.user_id == invoice.user_id).first()
        if not account:
            account = UserAccount(user_id=invoice.user_id, balance=0.0)
            db.add(account)

        account.balance = float(account.balance) + float(invoice.amount)
        db.add(account)

    db.commit()
    db.refresh(invoice)
    return invoice

# -------------------
# Pending Invoices
# -------------------
def get_pending_invoices(db: Session, user: User):
    if user.role in ["finance", "president"]:
        return db.query(PaymentInvoice).filter(PaymentInvoice.status != InvoiceStatus.PRESIDENT_APPROVED.value).all()
    return db.query(PaymentInvoice).filter(PaymentInvoice.user_id == user.id).all()

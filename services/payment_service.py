from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.payment_model import PaymentInvoice, PaymentDeduction, InvoiceStatus
from models.instalment_model import Instalment
from models.user_account_Model import UserAccount
from models.user_model import User
from models.companyAccount_model import CompanyAccount 

def create_payment_invoice(db: Session, invoice_data, user: User) -> PaymentInvoice:
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

def approve_payment_finance(db: Session, invoice_id: int, user: User) -> PaymentInvoice:
    invoice = db.query(PaymentInvoice).filter(PaymentInvoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if invoice.approved_by_finance:
        return invoice

    invoice.approved_by_finance = True
    invoice.status = InvoiceStatus.FINANCE_APPROVED.value
    db.commit()
    db.refresh(invoice)
    return invoice



def approve_payment_president(db: Session, invoice_id: int, user: User) -> PaymentInvoice:
    invoice = db.query(PaymentInvoice).filter(PaymentInvoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    if not invoice.approved_by_finance:
        raise HTTPException(status_code=400, detail="Finance approval required first")
    if invoice.approved_by_president:
        return invoice

    with db.begin():
        invoice.approved_by_president = True
        invoice.status = InvoiceStatus.PRESIDENT_APPROVED.value

        remaining_amount = float(invoice.amount)

        user_instalments = (
            db.query(Instalment)
            .filter(Instalment.user_id == invoice.user_id)
            .order_by(Instalment.year, Instalment.month)
            .all()
        )

        for inst in user_instalments:
            if inst.amount_due <= 0:
                continue
            deduct_amount = min(inst.amount_due, remaining_amount)
            inst.amount_due -= deduct_amount
            remaining_amount -= deduct_amount
            db.add(inst)

            deduction = PaymentDeduction(
                invoice_id=invoice.id,
                installment_id=inst.id,
                amount=deduct_amount
            )
            db.add(deduction)

            if remaining_amount <= 0:
                break

        # ✅ Step 1: ইউজারের অ্যাকাউন্ট আপডেট বা তৈরি
        account = db.query(UserAccount).filter_by(user_id=invoice.user_id).first()
        if not account:
            account = UserAccount(user_id=invoice.user_id, balance=0.0)
        account.balance += invoice.amount
        db.add(account)

        # ✅ Step 2: কোম্পানি একাউন্ট থেকে ব্যালেন্স কমাও
        company_account = db.query(CompanyAccount).filter_by(id=1).first()
        if not company_account:
            raise HTTPException(status_code=500, detail="Company account not found")

        if company_account.balance < invoice.amount:
            raise HTTPException(status_code=400, detail="Insufficient company balance")

        company_account.balance -= invoice.amount
        db.add(company_account)

    db.commit()
    db.refresh(invoice)
    return invoice


def get_pending_invoices(db: Session, user: User):
    if user.role in ["finance", "president"]:
        return db.query(PaymentInvoice).filter(PaymentInvoice.status != InvoiceStatus.PRESIDENT_APPROVED.value).all()
    return db.query(PaymentInvoice).filter(PaymentInvoice.user_id == user.id).all()

def get_user_payment_status(db: Session, user_id: int):
    invoices = db.query(PaymentInvoice).filter(PaymentInvoice.user_id == user_id).order_by(PaymentInvoice.date.desc()).all()
    return invoices

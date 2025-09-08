from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from database import Base
import enum

class InvoiceStatus(str, enum.Enum):
    PENDING = "pending"
    FINANCE_APPROVED = "finance_approved"
    PRESIDENT_APPROVED = "president_approved"

class PaymentInvoice(Base):
    __tablename__ = "payment_invoices"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, default=date.today)
    transaction_id = Column(String, nullable=False)
    payment_slip = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    payment_type = Column(String, nullable=False)
    account_number = Column(String, nullable=True)

    approved_by_finance = Column(Boolean, default=False)
    approved_by_president = Column(Boolean, default=False)
    status = Column(String, default=InvoiceStatus.PENDING.value)

    user = relationship("User", back_populates="invoices")
    deductions = relationship("PaymentDeduction", back_populates="invoice")

class PaymentDeduction(Base):
    __tablename__ = "payment_deductions"

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey("payment_invoices.id"))
    installment_id = Column(Integer, ForeignKey("instalments.id"))  # ok, string reference
    amount = Column(Float)

    invoice = relationship("PaymentInvoice", back_populates="deductions")
    installment = relationship("Instalment", back_populates="deductions")

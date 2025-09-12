# models/instalment_model.py
from sqlalchemy import Column, Integer, Float, ForeignKey,String
from sqlalchemy.orm import relationship
from database import Base
from models.ledger_model import Ledger
class Instalment(Base):
    __tablename__ = "instalments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    ledger_id = Column(Integer, ForeignKey("ledgers.id"))
    amount_due = Column(Float)
    month = Column(Integer)
    status = Column(String, default="due")  # due / partial / paid
    category_id = Column(Integer, ForeignKey("ledger_categories.id"), nullable=True)

    user = relationship("User", back_populates="instalments")
    ledger = relationship("Ledger", back_populates="instalments")
    deductions = relationship("PaymentDeduction", back_populates="installment")
    category = relationship("LedgerCategory", back_populates="installments")


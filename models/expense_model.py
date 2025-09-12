# models/expense_model.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("ledger_categories.id"))
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=True)

    status = Column(String, default="pending")  # pending / finance_approved / manager_approved / rejected
    approved_by_finance = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_by_manager = Column(Integer, ForeignKey("users.id"), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    category = relationship("LedgerCategory")
    finance_approver = relationship("User", foreign_keys=[approved_by_finance])
    manager_approver = relationship("User", foreign_keys=[approved_by_manager])

# models/ledger_model.py

from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

# Income বা Expense টাইপের Enum
class LedgerType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

# ক্যাটাগরি মডেল
class LedgerCategory(Base):
    __tablename__ = "ledger_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Income → মাসের নাম, Expense → নাম
    type = Column(Enum(LedgerType), nullable=False)
    month = Column(Integer, nullable=True)  # শুধু monthly income

    ledgers = relationship("Ledger", back_populates="category")
    installments = relationship("Instalment", back_populates="category")

# লেজার মডেল (ইনকাম / এক্সপেন্স উভয়ের জন্য)
class Ledger(Base):
    __tablename__ = "ledgers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("ledger_categories.id"))

    amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    status = Column(String, default="due")  # due / partial / paid
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    month = Column(Integer, nullable=True)

    
    approval_status = Column(String, default="pending")  # pending / finance_approved / manager_approved / rejected
    approved_by_finance = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_by_manager = Column(Integer, ForeignKey("users.id"), nullable=True)

    # ✅ Relationships
    user = relationship("User", back_populates="ledger_entries", foreign_keys=[user_id])
    category = relationship("LedgerCategory", back_populates="ledgers")
    instalments = relationship("Instalment", back_populates="ledger")

    # ✅ Optional approver relationships
    approved_finance_user = relationship("User", foreign_keys=[approved_by_finance])
    approved_manager_user = relationship("User", foreign_keys=[approved_by_manager])


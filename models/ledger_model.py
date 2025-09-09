# models/ledger_model.py
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum

class LedgerType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class LedgerCategory(Base):
    __tablename__ = "ledger_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Income → মাসের নাম, Expense → নাম
    type = Column(Enum(LedgerType), nullable=False)
    month = Column(Integer, nullable=True)  # শুধু monthly income

    ledgers = relationship("Ledger", back_populates="category")

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

    user = relationship("User", back_populates="ledger_entries")
    category = relationship("LedgerCategory", back_populates="ledgers")

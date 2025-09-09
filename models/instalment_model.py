# models/instalment_model.py
from sqlalchemy import Column, Integer, Float, ForeignKey,String
from sqlalchemy.orm import relationship
from database import Base

class Instalment(Base):
    __tablename__ = "instalments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    month = Column(Integer)
    amount_due = Column(Float)
    status = Column(String, default="due")  # due / partial / paid
    ledger_id = Column(Integer, ForeignKey("ledgers.id"), nullable=True)

    user = relationship("User", back_populates="instalments")
    ledger = relationship("Ledger")

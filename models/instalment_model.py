from sqlalchemy import Column, String, Integer,Date,Float,ForeignKey,Boolean
from sqlalchemy.orm import relationship
from database import Base

class Instalment(Base):
    __tablename__ = "instalments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    month = Column(Integer)
    amount_due = Column(Float)

    deductions = relationship("PaymentDeduction", back_populates="installment")


from sqlalchemy import Column, Integer, Float, String
from database import Base

class CompanyAccount(Base):
    __tablename__ = "company_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, nullable=False)     
    bank_name = Column(String, nullable=False)        
    routing_number = Column(String, nullable=False)   
    account_number = Column(String, nullable=False, unique=True)  
    balance = Column(Float, default=0.0)             

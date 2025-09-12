# schemas/company_schema.py

from pydantic import BaseModel

class CompanyAccountCreate(BaseModel):
    account_name: str
    bank_name: str
    routing_number: str
    account_number: str
    balance: float

class CompanyAccountOut(BaseModel):
    id: int
    account_name: str
    bank_name: str
    routing_number: str
    account_number: str
    balance: float

    class Config:
        orm_mode = True

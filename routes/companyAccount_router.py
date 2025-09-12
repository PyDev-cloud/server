from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.companyAccount_schema import CompanyAccountCreate, CompanyAccountOut
from services.companyAccount_service import (
    create_company_account,
    get_company_account,
    update_company_balance,
)

router = APIRouter(prefix="/company-account", tags=["Company Account"])

@router.post("/", response_model=CompanyAccountOut)
def create_account(data: CompanyAccountCreate, db: Session = Depends(get_db)):
    return create_company_account(db, data)

@router.get("/", response_model=CompanyAccountOut)
def get_account(db: Session = Depends(get_db)):
    account = get_company_account(db)
    if not account:
        raise HTTPException(status_code=404, detail="Company account not found")
    return account

@router.post("/adjust", response_model=CompanyAccountOut)
def adjust_balance(amount: float, increase: bool = True, db: Session = Depends(get_db)):
    try:
        return update_company_balance(db, amount=amount, increase=increase)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

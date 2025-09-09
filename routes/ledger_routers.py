from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.ledger_model import Ledger,LedgerCategory,LedgerType
from schemas.ledger_schema import LedgerCategoryOut, LedgerCategoryCreate, LedgerCreate, LedgerOut
from services.ledger_service import create_category,get_categories,create_ledger,get_ledgers

router = APIRouter(
    prefix="/ledger",
    tags=["Ledger"]
)

# ------------------------
# Category Endpoints
# ------------------------
@router.post("/categories/", response_model=LedgerCategoryOut)
async def create_category_route(category: LedgerCategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)

@router.get("/categories/", response_model=list[LedgerCategoryOut])
async def get_categories_route(db: Session = Depends(get_db)):
    return get_categories(db)

# ------------------------
# Ledger Endpoints
# ------------------------
@router.post("/ledgers/", response_model=LedgerOut)
async def create_ledger_route(ledger: LedgerCreate, db: Session = Depends(get_db)):
    return create_ledger(db, ledger)

@router.get("/ledgers/", response_model=list[LedgerOut])
async def get_ledgers_route(db: Session = Depends(get_db)):
    return get_ledgers(db)

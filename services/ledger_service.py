from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.ledger_model import LedgerCategory,Ledger

from schemas.ledger_schema import LedgerCreate,LedgerCategoryCreate,LedgerType

def create_category(db: Session, category: LedgerCategoryCreate):
    if category.type == LedgerType.INCOME and not category.month:
        raise HTTPException(status_code=400, detail="Income category must have a month name")

    db_category = LedgerCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(LedgerCategory).all()



def create_ledger(db: Session, ledger: LedgerCreate):
    db_ledger = Ledger(**ledger.dict())
    db.add(db_ledger)
    db.commit()
    db.refresh(db_ledger)
    return db_ledger

def get_ledgers(db: Session):
    return db.query(Ledger).all()
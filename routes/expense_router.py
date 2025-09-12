# routers/expense_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.expense_schema import ExpenseCreate, ExpenseOut
from services.expense_service import create_expense, approve_by_finance, approve_by_manager
from models.user_model import User
from utils.dependencies import get_current_user  # আপনার auth system অনুযায়ী
from typing import List

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/create", response_model=ExpenseOut)
def create(data: ExpenseCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_expense(db, user, data)

@router.post("/approve/finance/{expense_id}")
def finance_approve(expense_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return approve_by_finance(db, user, expense_id)

@router.post("/approve/manager/{expense_id}")
def manager_approve(expense_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return approve_by_manager(db, user, expense_id)

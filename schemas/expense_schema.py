# schemas/expense_schema.py

from pydantic import BaseModel
from typing import Optional

class ExpenseCreate(BaseModel):
    category_id: int
    amount: float
    description: Optional[str] = None
    year: int
    month: Optional[int] = None

class ExpenseOut(BaseModel):
    id: int
    user_id: int
    category_id: int
    amount: float
    description: Optional[str]
    year: int
    month: Optional[int]
    status: str

    class Config:
        orm_mode = True

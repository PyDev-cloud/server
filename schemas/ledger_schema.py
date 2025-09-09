from pydantic import BaseModel
from typing import Optional
import enum

class LedgerType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class LedgerCategoryBase(BaseModel):
    name: str
    type: LedgerType
    month: Optional[str] = None

class LedgerCategoryCreate(LedgerCategoryBase):
    pass

class LedgerCategoryOut(LedgerCategoryBase):
    id: int
    class Config:
        orm_mode = True

class LedgerBase(BaseModel):
    category_id: int
    amount: int
    year: int
    description: Optional[str] = None

class LedgerCreate(LedgerBase):
    pass

class LedgerOut(LedgerBase):
    id: int
    category: LedgerCategoryOut
    class Config:
        orm_mode = True

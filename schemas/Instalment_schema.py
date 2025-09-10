from pydantic import BaseModel
from typing import Optional, List

class InstalmentBase(BaseModel):
    user_id: int
    ledger_id: int
    amount_due: float
    months: List[int]
    status: Optional[str] = "due"
    category_id: Optional[int] = None

class InstalmentCreate(InstalmentBase):
    pass

class InstalmentRead(InstalmentBase):
    id: int

    class Config:
        orm_mode = True

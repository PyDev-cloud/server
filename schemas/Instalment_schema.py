# schemas/instalment_schema.py
from pydantic import BaseModel

class InstalmentCreate(BaseModel):
    user_id: int | None = None   # None → all users
    months: int                  # কত মাসের dues create
    amount_due: float

class InstalmentOut(BaseModel):
    id: int
    user_id: int
    month: int
    amount_due: float
    status: str

    class Config:
        orm_mode = True

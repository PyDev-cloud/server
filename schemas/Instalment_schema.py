from pydantic import BaseModel,validator
from datetime import date

class InstalmentCreate(BaseModel):
    month: str  # keep as string from frontend (YYYY-MM)
    amount_due: float
    global_user: bool
    user_id: int | None

    @validator("month")
    def parse_month(cls, v):
        # Convert YYYY-MM to date object (first day of month)
        parts = v.split("-")
        if len(parts) == 2:
            year, month = map(int, parts)
            return date(year, month, 1)
        raise ValueError("month must be in YYYY-MM format")

class InstalmentSchema(BaseModel): 
    id: int
    month: date
    amount_due: float
    user_id: int | None

    class Config:
        orm_mode = True
from pydantic import BaseModel
from typing import Optional, List


# ✅ Base model: সব কমন ফিল্ড এখানে থাকবে
class InstalmentBase(BaseModel):
    user_id: int
    ledger_id: int
    amount_due: float
    month: int
    status: Optional[str] = "due"  # default status
    category_id: Optional[int] = None


# ✅ Create model (single month create)
class InstalmentSingleCreate(InstalmentBase):
    pass


# ✅ Create model for multiple months (auto create service-এর জন্য)
class InstalmentCreate(BaseModel):
    user_id: Optional[int] = None           # যদি None হয়, সব ইউজারের জন্য
    amount_due: float                       # প্রতি মাসে কত টাকার ইনস্টলমেন্ট
    months: List[int]  
    category_id: Optional[int] = None                     # একাধিক মাস (e.g. [1,2,3])


# ✅ Update model (PATCH / PUT)
class InstalmentUpdate(BaseModel):
    user_id: Optional[int] = None
    ledger_id: Optional[int] = None
    amount_due: Optional[float] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    month: Optional[int] = None


# ✅ Read model
class InstalmentRead(InstalmentBase):
    id: int

    class Config:
        orm_mode = True

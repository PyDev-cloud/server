from pydantic import BaseModel, EmailStr, StringConstraints, Field
from typing import Annotated, Optional

# Custom type with regex validation for BD phone number
PhoneStr = Annotated[str, StringConstraints(pattern=r'^\+8801[0-9]{9}$')]

class UserCreate(BaseModel):
    name: str
    phone: PhoneStr
    email: EmailStr
    alternative_Phone: Optional[str] = None
    role: Optional[str] = Field(default="general")

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    alternative_Phone: Optional[str] = None
    role: Optional[str] = "general"

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

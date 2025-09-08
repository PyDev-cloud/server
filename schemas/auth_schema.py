from pydantic import BaseModel, Field, EmailStr
from typing import Annotated

# Request Schemas
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class SetPasswordRequest(BaseModel):
    token: str
    password: Annotated[str, Field(min_length=8, description="Password must be at least 8 characters")]

# Response Schemas
class TokenResponse(BaseModel):
    token: str
    message: str = "Login successful"

class PasswordSetResponse(BaseModel):
    user_id: int
    message: str = "Password set successfully"

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

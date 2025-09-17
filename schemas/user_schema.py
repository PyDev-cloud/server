import enum
from pydantic import BaseModel, EmailStr
from typing import Optional,List
from datetime import date


# ------------------------
# User Schemas
# ------------------------

class UserRole(str, enum.Enum):
    GENERAL = "General User"
    President = "President"
    Finance_Secretary = "Finance Secretary"
    Office_Admin = "Office Admin"
    ADMIN = "admin"
class UserCreate(BaseModel):
    name: str
    phone: str
    alternative_phone: Optional[str] = None
    email: EmailStr
    role: UserRole = UserRole.GENERAL 

    model_config = {
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    alternative_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

    model_config = {
        "from_attributes": True
    }




# ------------------------
# Profile Schemas
# ------------------------
class UserProfileCreate(BaseModel):
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class UserProfileUpdate(BaseModel):
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# ------------------------
# Occupation Schemas
# ------------------------
class OccupationCreate(BaseModel):
    occupation: Optional[str] = None
    company_name: Optional[str] = None
    designation: Optional[str] = None
    annual_income: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


class OccupationUpdate(BaseModel):
    occupation: Optional[str] = None
    company_name: Optional[str] = None
    designation: Optional[str] = None
    annual_income: Optional[float] = None

    model_config = {
        "from_attributes": True
    }


# ------------------------
# Nominee Schemas
# ------------------------
class NomineeCreate(BaseModel):
    name: str
    relation: str
    phone: Optional[str] = None
    address: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class NomineeUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    relation: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


# ------------------------
# Kid Schemas
# ------------------------
class KidCreate(BaseModel):
    name: str
    dob: Optional[date] = None
    gender: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class KidUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

# ------------------------
# Document Schemas
# ------------------------
class DocumentCreate(BaseModel):
    doc_type: str
    file_path: str

    model_config = {
        "from_attributes": True
    }

class DocumentUpdate(BaseModel):
    id: Optional[int] = None
    doc_type: Optional[str] = None
    file_path: Optional[str] = None
    
    model_config = {
            "from_attributes": True
        }



class NomineeOut(BaseModel):
    id: int
    name: str
    relation: str
    phone: Optional[str]
    address: Optional[str]

    model_config = {"from_attributes": True}

class KidOut(BaseModel):
    id: int
    name: str
    dob: Optional[date]
    gender: Optional[str]

    model_config = {"from_attributes": True}

class DocumentOut(BaseModel):
    id: int
    doc_type: str
    file_path: str

    model_config = {"from_attributes": True}

class UserProfileOut(BaseModel):
    dob: Optional[date]
    gender: Optional[str]
    address: Optional[str]
    blood_group: Optional[str]

    model_config = {"from_attributes": True}

class OccupationOut(BaseModel):
    occupation: Optional[str]
    company_name: Optional[str]
    designation: Optional[str]
    annual_income: Optional[float]

    model_config = {"from_attributes": True}

class UserOut(BaseModel):
    id: int
    name: Optional[str]  # <- changed
    phone: Optional[str]  # <- changed
    alternative_phone: Optional[str]
    email: Optional[EmailStr]  # <- changed
    role: str
    is_active: bool
    profile: Optional[UserProfileOut]
    occupation: Optional[OccupationOut]
    nominees: List[NomineeOut] = []
    kids: List[KidOut] = []
    documents: List[DocumentOut] = []

    
    class Config:
        orm_mode = True

class DraftUserUpdateRequest(BaseModel):
    user: Optional[UserUpdate] = None
    profile: Optional[UserProfileUpdate] = None
    occupation: Optional[OccupationUpdate] = None
    nominees: Optional[List[NomineeUpdate]] = None
    kids: Optional[List[KidUpdate]] = None
    documents: Optional[List[DocumentUpdate]] = None
    model_config = {
            "from_attributes": True
        }

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Text, Float,Enum
from sqlalchemy.orm import relationship
from database import Base
from models.payment_model import PaymentInvoice
import enum
import uuid

class UserRole(str, enum.Enum):
    GENERAL = "General User"
    President = "President"
    Finance_Secretary = "Finance Secretary"
    Office_Admin = "Office Admin"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    alternative_phone = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(UserRole), default=UserRole.GENERAL, nullable=False)
    
    is_active = Column(Boolean, default=False)
    is_super_admin = Column(Boolean, default=False)  # ✅ নতুন ফিল্ড

    temp_token = Column(String(36), nullable=True, unique=True, default=lambda: str(uuid.uuid4()))
    hashed_password = Column(String(255), nullable=True)

    # Relationships (ডেমো হিসেবে, তুমি চাইলে কমাতে পারো
    invoices = relationship("PaymentInvoice", back_populates="user")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    occupation = relationship("OccupationInfo", back_populates="user", uselist=False, cascade="all, delete-orphan")
    nominees = relationship("Nominee", back_populates="user", cascade="all, delete-orphan")
    kids = relationship("Kid", back_populates="user", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="user", cascade="all, delete-orphan")
    instalments = relationship("Instalment", back_populates="user")
    ledger_entries = relationship("Ledger", back_populates="user", foreign_keys="Ledger.user_id")
    user_account = relationship("UserAccount", back_populates="user")
   
    
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    address = Column(Text, nullable=True)
    blood_group = Column(String(5), nullable=True)

    user = relationship("User", back_populates="profile")


class OccupationInfo(Base):
    __tablename__ = "occupation_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    occupation = Column(String(100), nullable=True)
    company_name = Column(String(150), nullable=True)
    designation = Column(String(100), nullable=True)
    annual_income = Column(Float, nullable=True)

    user = relationship("User", back_populates="occupation")


class Nominee(Base):
    __tablename__ = "nominees"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    relation = Column(String(50), nullable=False)
    phone = Column(String(20), nullable=True)
    address = Column(Text, nullable=True)

    user = relationship("User", back_populates="nominees")


class Kid(Base):
    __tablename__ = "kids"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)

    user = relationship("User", back_populates="kids")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    doc_type = Column(String(50), nullable=False)  # e.g., "NID", "Passport", "Certificate"
    file_path = Column(String(255), nullable=False)  # saved file path

    user = relationship("User", back_populates="documents")

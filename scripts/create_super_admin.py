import sys
import os

# প্রোজেক্ট রুট পাথ যুক্ত করা যাতে মডিউল খুঁজে পায়
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user_model import User, UserRole  # এখন এটি সঠিকভাবে কাজ করবে
from models.user_account_Model import UserAccount
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base  # তোমার base model যেটা Base = declarative_base() হয়
import uuid
from passlib.context import CryptContext

# পাসওয়ার্ড হ্যাশ করার জন্য (যদি তোমার পাসওয়ার্ড হ্যাশিং এভাবে হয়)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ডাটাবেস কানেকশন URL - তোমার সেটিং অনুসারে পরিবর্তন করবে
DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_super_admin():
    db = SessionLocal()
    try:
        # চেক করো সুপার অ্যাডমিন আছে কিনা
        existing_admin = db.query(User).filter_by(is_super_admin=True).first()
        if existing_admin:
            print("Super Admin already exists:", existing_admin.email)
            return

        # নতুন সুপার অ্যাডমিন তৈরি
        super_admin = User(
            name="Md Raju Ahamed",
            phone="+8801630595056",
            alternative_phone=None,
            email="rajuoffice220@gmail.com",
            role=UserRole.ADMIN,  # তোমার ইউজার রোলে যেটা super admin তার নাম
            is_active=True,
            is_super_admin=True,
            temp_token=str(uuid.uuid4()),
            hashed_password=get_password_hash("supersecretpassword")  # পাসওয়ার্ড
        )

        db.add(super_admin)
        db.commit()
        print("Super Admin created successfully!")

    except Exception as e:
        db.rollback()
        print("Error creating Super Admin:", e)
    finally:
        db.close()

if __name__ == "__main__":
    create_super_admin()

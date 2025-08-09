from sqlalchemy.orm import Session
from models.user_model import User
from schemas.user_schema import UserCreate

ROLE_LIMITS = {
    "president": 1,
    "finance": 1,
    "expense": 1,
    "member": 5
}

def create_user(db: Session, user_data: UserCreate):
    user = User(
        name=user_data.name,
        phone=user_data.phone,
        email=user_data.email,
        alternative_Phone=user_data.alternative_Phone,
        role=user_data.role or "general"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()

def get_users_by_role(db: Session, role: str):
    return db.query(User).filter(User.role == role).all()

def assign_role(db: Session, user_id: int, role: str):
    if role not in ROLE_LIMITS:
        return {"error": "Invalid role"}
    
    # চেক করো রোল পূর্ণ হয়েছে কিনা
    current_count = db.query(User).filter(User.role == role).count()
    if current_count >= ROLE_LIMITS[role]:
        return {"error": f"{role} role is already full"}
    
    # শুধুমাত্র general ইউজার থেকে রোল অ্যাসাইন
    user = db.query(User).filter(User.id == user_id, User.role == "general").first()
    if not user:
        return {"error": "User not found or not general"}
    
    user.role = role
    db.commit()
    db.refresh(user)
    return user

def get_general_users(db: Session):
    return db.query(User).filter(User.role == "general").all()
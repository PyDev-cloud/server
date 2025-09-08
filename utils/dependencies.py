from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user_model import User

# dependencies.py
from models.user_model import User
from sqlalchemy.orm import Session
from database import get_db

def get_current_user(db: Session = Depends(get_db)) -> User:
    # প্রথম ইউজারকে রিটার্ন করবে, শুধু ডেভেলপমেন্ট বা টেস্টের জন্য
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=404, detail="No users found")
    return user

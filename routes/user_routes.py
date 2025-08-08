from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from services import user_service
from schemas.user_schema import UserCreate, UserResponse
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user.name)

@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get("/users/general", response_model=List[UserResponse])
def list_general_users(db: Session = Depends(get_db)):
    return user_service.get_general_users(db)

@router.post("/users/{user_id}/assign/{role}", response_model=UserResponse)
def assign_role(user_id: int, role: str, db: Session = Depends(get_db)):
    result = user_service.assign_role(db, user_id, role)
    if isinstance(result, dict) and "error" in result:
        return result

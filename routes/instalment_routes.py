from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.Instalment_schema import InstalmentCreate, InstalmentSchema
from services.instalment_service import create_instalment, instalment_get_id
from typing import List

router = APIRouter(
    prefix="/instalment",
    tags=["Instalment"]
)


@router.post("/", response_model=dict)
def add_instalment(data: InstalmentCreate, db: Session = Depends(get_db)):
    """
    Create an instalment for a user or all users.
    Returns a message and optionally created IDs.
    """
    result = create_instalment(db, data)
    return result


@router.get("/user/{user_id}", response_model=List[InstalmentSchema])
def get_user_instalments_api(user_id: int, db: Session = Depends(get_db)):
    """
    Get all instalments for a specific user.
    """
    instalments = instalment_get_id(db, user_id)
    if not instalments:
        raise HTTPException(status_code=404, detail="No instalments found for this user")
    return instalments

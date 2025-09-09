# routes/instalment_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas.Instalment_schema import InstalmentCreate
from services.instalment_service import create_instalments, create_dues_for_new_user

router = APIRouter(prefix="/instalments", tags=["Instalments"])

@router.post("/create/")
def create_instalment_route(data: InstalmentCreate, db: Session = Depends(get_db)):
    return create_instalments(db, data)


@router.post("/new_user_dues/{user_id}")
def new_user_dues_route(
    user_id: int,
    months_back: int,
    amount_due: float,
    db: Session = Depends(get_db)
):
    """
    Create past dues for a newly joined user.
    - user_id: ID of the new user
    - months_back: how many previous months to create
    - amount_due: amount for each month
    """
    try:
        result = create_dues_for_new_user(db, user_id, months_back, amount_due)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
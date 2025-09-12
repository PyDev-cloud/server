from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from database import get_db
from models.user_model import User
from models.instalment_model import Instalment
from schemas.Instalment_schema import (
    InstalmentCreate,
    InstalmentRead,
    InstalmentUpdate,
)
from services.instalment_service import (
    create_instalments,
    create_full_dues_for_user,
    get_instalments,
    update_instalment,
    delete_instalment
)
from utils.dependencies import get_current_user  # <-- make sure this is correctly implemented

router = APIRouter(prefix="/instalments", tags=["Instalments"])

# ✅ Create Instalments
@router.post("/create/")
def create_instalment_route(
    data: InstalmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_instalments(db, data, current_user)


# ✅ Create Full Dues for a New User
@router.post("/new_user_dues/{user_id}")
def new_user_dues_route(
    user_id: int,
    months_back: int,
    amount_due: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create past dues for a newly joined user.
    - user_id: ID of the new user
    - months_back: how many previous months to create
    - amount_due: amount for each month
    """
    try:
        # Build dues_dict for past `months_back` months with same amount
        from datetime import datetime
        from dateutil.relativedelta import relativedelta

        dues_dict = {}
        today = datetime.today()
        for i in range(months_back):
            date = today - relativedelta(months=i)
            dues_dict[date.month] = amount_due

        return create_full_dues_for_user(db, user_id, dues_dict, current_user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ✅ List Instalments
@router.get("/", response_model=List[InstalmentRead])
def list_instalments(
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return get_instalments(db, user_id)


# ✅ Update Instalment
@router.put("/{instalment_id}", response_model=InstalmentRead)
def update_instalment_route(
    instalment_id: int,
    data: InstalmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_instalment(db, instalment_id, data, current_user)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))


# ✅ Delete Instalment
@router.delete("/{instalment_id}")
def delete_instalment_route(
    instalment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return delete_instalment(db, instalment_id, current_user)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))

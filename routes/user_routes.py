from fastapi import APIRouter, Depends, HTTPException, Query,Body
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from database import get_db  # Your DB dependency
from models.user_model import User, UserProfile, OccupationInfo, Nominee, Kid, Document
from schemas.user_schema import (
    UserCreate,
    UserUpdate,
    UserProfileCreate,
    UserProfileUpdate,
    OccupationCreate,
    OccupationUpdate,
    NomineeCreate,
    NomineeUpdate,
    KidCreate,
    KidUpdate,
    DocumentCreate,
    DocumentUpdate,
    DraftUserUpdateRequest,
    UserOut,
    NomineeOut,
    UserProfileOut,
    KidOut,
    DocumentOut,
    OccupationOut,
)
from services.user_service import (
    create_user,
    add_profile,
    add_occupation,
    add_nominee,
    add_kid,
    add_document,
    finalize_user,
    update_draft_user_all,
    get_all_users,
    get_users_by_role,
    get_general_users,
    delete_user,
    assign_role,
    activate_user,
    deactivate_user,
)

router = APIRouter(prefix="/users", tags=["Users"])

# -----------------------
# Create draft user
# -----------------------
@router.post("/draft", summary="Create draft user")
def api_create_user(user_data: UserCreate = Body(...), db: Session = Depends(get_db)):
    user_dict = create_user(db, user_data)
    return {"message": "Draft user created, check email for activation link", "user_id": user_dict["id"],"token": user_dict["token"]}


# -----------------------
# Add draft data
# -----------------------
@router.post("/draft/profile", summary="Add draft user profile")
def add_draft_profile(
    token: str = Query(...),
    profile: Optional[UserProfileCreate] = Body(default=None),
    db: Session = Depends(get_db)
):
    if profile is None:
        return {"detail": "No profile data provided"}
    return add_profile(db, token, profile)


@router.post("/draft/occupation", summary="Add draft user occupation")
def add_draft_occupation(
    token: str = Query(...),
    occupation: Optional[OccupationCreate] = Body(default=None),
    db: Session = Depends(get_db)
):
    if occupation is None:
        return {"detail": "No occupation data provided"}
    return add_occupation(db, token, occupation)


@router.post("/draft/nominee", summary="Add draft user nominee")
def add_draft_nominee(
    token: str = Query(...),
    nominee: Optional[NomineeCreate] = Body(default=None),
    db: Session = Depends(get_db)
):
    if nominee is None:
        return {"detail": "No nominee data provided"}
    return add_nominee(db, token, nominee)


@router.post("/draft/kid", summary="Add draft user kid")
def add_draft_kid(
    token: str = Query(...),
    kid: Optional[KidCreate] = Body(default=None),
    db: Session = Depends(get_db)
):
    if kid is None:
        return {"detail": "No kid data provided"}
    return add_kid(db, token, kid)


@router.post("/draft/document", summary="Add draft user document")
def add_draft_document(
    token: str = Query(...),
    document: Optional[DocumentCreate] = Body(default=None),
    db: Session = Depends(get_db)
):
    if document is None:
        return {"detail": "No document data provided"}
    return add_document(db, token, document)


# -----------------------
# Finalize draft user
# -----------------------
@router.post("/draft/finalize", summary="Finalize draft user")
def finalize_draft_user(token: str = Query(...), db: Session = Depends(get_db)):
    return finalize_user(db, token)


# -----------------------
# Update draft user (multi-table) by user_id
# -----------------------

# Get all Data for user 
@router.get("/users/draft/{user_id}", response_model=UserOut, summary="Get draft user details")
def get_draft_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    nominees = db.query(Nominee).filter(Nominee.user_id == user.id).all()
    kids = db.query(Kid).filter(Kid.user_id == user.id).all()
    documents = db.query(Document).filter(Document.user_id == user.id).all()

    return {
        "id": user.id,
        "name": user.name,
        "phone": user.phone,
        "alternative_phone": user.alternative_phone,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "profile": user.profile,
        "occupation": user.occupation,
        "nominees": nominees,
        "kids": kids,
        "documents": documents,
    }

# User Update 

@router.put("/users/draft/{user_id}", response_model=UserOut, summary="Get or update draft user")
def get_or_update_draft_user(
    user_id: int,
    data: DraftUserUpdateRequest = Body(None),  # optional
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 1️⃣ If no body is sent, return current data
    if data is None:
        nominees = db.query(Nominee).filter(Nominee.user_id == user.id).all()
        kids = db.query(Kid).filter(Kid.user_id == user.id).all()
        documents = db.query(Document).filter(Document.user_id == user.id).all()
        return UserOut(
            id=user.id,
            name=user.name,
            phone=user.phone,
            alternative_phone=user.alternative_phone,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            profile=user.profile,
            occupation=user.occupation,
            nominees=nominees,
            kids=kids,
            documents=documents
        )

    # 2️⃣ If body is sent, update user
    return update_draft_user_all(
        db=db,
        user_id=user_id,
        user_data=data.user,
        profile_data=data.profile,
        occupation_data=data.occupation,
        nominees_data=data.nominees,
        kids_data=data.kids,
        documents_data=data.documents
    )


# -----------------------
# Normal user management
# -----------------------
@router.get("/", summary="Get all users")
def list_all_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.get("/role/{role}", summary="Get users by role")
def list_users_by_role(role: str, db: Session = Depends(get_db)):
    return get_users_by_role(db, role)


@router.get("/general", summary="Get general users")
def list_general_users(db: Session = Depends(get_db)):
    return get_general_users(db)


@router.delete("/{user_id}", summary="Delete user")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)


@router.put("/role/{user_id}", summary="Assign role to user")
def set_user_role(user_id: int, role: str, db: Session = Depends(get_db)):
    return assign_role(db, user_id, role)


@router.put("/activate/{user_id}", summary="Activate user")
def activate_user_account(user_id: int, db: Session = Depends(get_db)):
    return activate_user(db, user_id)


@router.put("/deactivate/{user_id}", summary="Deactivate user")
def deactivate_user_account(user_id: int, db: Session = Depends(get_db)):
    return deactivate_user(db, user_id)

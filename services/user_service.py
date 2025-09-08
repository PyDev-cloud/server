import uuid
from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.user_model import User, UserProfile, OccupationInfo, Nominee, Kid, Document
from services.auth_service import create_activation
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
)

# Role constraints
ROLE_LIMITS = {
    "president": 1,
    "finance": 1,
    "expense": 1,
    "member": 5,
}


# -------------------
# Helpers
# -------------------
def get_user_by_token(db: Session, token: str) -> User:
    user = db.query(User).filter(User.temp_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Draft user not found")
    return user


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -------------------
# Draft User Creation Flow
# -------------------
def create_user(db: Session, user_data: UserCreate) -> dict:
    import uuid
    token = str(uuid.uuid4())
    user = User(**user_data.dict(), is_active=False, temp_token=token)
    db.add(user)
    db.commit()
    db.refresh(user)
    create_activation(db, user)
    return {"token": token, "user_name": user.name, "id": user.id}  # id include করা



def add_profile(db: Session, token: str, profile_data: UserProfileCreate) -> UserProfile:
    user = get_user_by_token(db, token)
    profile = UserProfile(user_id=user.id, **profile_data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def add_occupation(db: Session, token: str, occupation_data: OccupationCreate) -> OccupationInfo:
    user = get_user_by_token(db, token)
    occupation = OccupationInfo(user_id=user.id, **occupation_data.dict())
    db.add(occupation)
    db.commit()
    db.refresh(occupation)
    return occupation


def add_nominee(db: Session, token: str, nominee_data: NomineeCreate) -> Nominee:
    user = get_user_by_token(db, token)
    nominee = Nominee(user_id=user.id, **nominee_data.dict())
    db.add(nominee)
    db.commit()
    db.refresh(nominee)
    return nominee


def add_kid(db: Session, token: str, kid_data: KidCreate) -> Kid:
    user = get_user_by_token(db, token)
    kid = Kid(user_id=user.id, **kid_data.dict())
    db.add(kid)
    db.commit()
    db.refresh(kid)
    return kid


def add_document(db: Session, token: str, document_data: DocumentCreate) -> Document:
    user = get_user_by_token(db, token)
    document = Document(user_id=user.id, **document_data.dict())
    db.add(document)
    db.commit()
    db.refresh(document)
    return document


def finalize_user(db: Session, token: str) -> User:
    user = get_user_by_token(db, token)
    user.is_active = False
    user.temp_token = None
    db.commit()
    db.refresh(user)
    return user


# -------------------
# Multi-table Draft User Update via user_id
# -------------------
def update_draft_user_all(
    db: Session,
    user_id: int,
    user_data: Optional[UserUpdate] = None,
    profile_data: Optional[UserProfileUpdate] = None,
    occupation_data: Optional[OccupationUpdate] = None,
    nominees_data: Optional[List[NomineeUpdate]] = None,
    kids_data: Optional[List[KidUpdate]] = None,
    documents_data: Optional[List[DocumentUpdate]] = None,
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ---- Update main user ----
    if user_data:
        for field, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

    # ---- Update profile ----
    if profile_data:
        if user.profile:
            for field, value in profile_data.model_dump(exclude_unset=True).items():
                setattr(user.profile, field, value)
        else:
            profile = UserProfile(user_id=user.id, **profile_data.model_dump())
            db.add(profile)

    # ---- Update occupation ----
    if occupation_data:
        if user.occupation:
            for field, value in occupation_data.model_dump(exclude_unset=True).items():
                setattr(user.occupation, field, value)
        else:
            occupation = OccupationInfo(user_id=user.id, **occupation_data.model_dump())
            db.add(occupation)

    # ---- Update/Add nominees ----
    if nominees_data:
        for nominee in nominees_data:
            if nominee.id:
                existing = db.query(Nominee).filter(Nominee.id == nominee.id, Nominee.user_id == user.id).first()
                if not existing:
                    raise HTTPException(status_code=404, detail=f"Nominee {nominee.id} not found")
                for field, value in nominee.model_dump(exclude={"id"}, exclude_unset=True).items():
                    setattr(existing, field, value)
            else:
                new_nominee = Nominee(user_id=user.id, **nominee.model_dump(exclude={"id"}))
                db.add(new_nominee)

    # ---- Update/Add kids ----
    if kids_data:
        for kid in kids_data:
            if kid.id:
                existing = db.query(Kid).filter(Kid.id == kid.id, Kid.user_id == user.id).first()
                if not existing:
                    raise HTTPException(status_code=404, detail=f"Kid {kid.id} not found")
                for field, value in kid.model_dump(exclude={"id"}, exclude_unset=True).items():
                    setattr(existing, field, value)
            else:
                new_kid = Kid(user_id=user.id, **kid.model_dump(exclude={"id"}))
                db.add(new_kid)

    # ---- Update/Add documents ----
    if documents_data:
        for doc in documents_data:
            if doc.id:
                existing = db.query(Document).filter(Document.id == doc.id, Document.user_id == user.id).first()
                if not existing:
                    raise HTTPException(status_code=404, detail=f"Document {doc.id} not found")
                for field, value in doc.model_dump(exclude={"id"}, exclude_unset=True).items():
                    setattr(existing, field, value)
            else:
                new_doc = Document(user_id=user.id, **doc.model_dump(exclude={"id"}))
                db.add(new_doc)

    db.commit()
    db.refresh(user)
    return user



# -------------------
# Normal User Management
# -------------------
def get_all_users(db: Session):
    return db.query(User).all()


def get_users_by_role(db: Session, role: str):
    return db.query(User).filter(User.role == role).all()


def get_general_users(db: Session):
    return db.query(User).filter(User.role == "general").all()


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
    return True


def assign_role(db: Session, user_id: int, role: str):
    if role not in ROLE_LIMITS:
        raise HTTPException(status_code=400, detail="Invalid role")
    current_count = db.query(User).filter(User.role == role).count()
    if current_count >= ROLE_LIMITS[role]:
        raise HTTPException(status_code=400, detail=f"{role} role is already full")
    user = db.query(User).filter(User.id == user_id, User.role == "general").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not general")
    user.role = role
    db.commit()
    db.refresh(user)
    return user


def activate_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user

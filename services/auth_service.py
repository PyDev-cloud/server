import secrets
from sqlalchemy.orm import Session
from models.user_model import User
from models.auth_model import UserActivation
from utils.security import hash_password, generate_token, get_expiry,verify_password,create_access_token
from utils.email_service import send_email
from fastapi import HTTPException
from datetime import datetime

def create_activation(db: Session, user: User) -> str:
    token = generate_token()
    activation = UserActivation(
        user_id=user.id,
        token=token,
        expires_at=get_expiry(hours=24)
    )
    db.add(activation)
    db.commit()
    db.refresh(activation)

    # Safely extract email
    user_email = getattr(user, "email", None)
    if not user_email or not isinstance(user_email, str):
        raise HTTPException(status_code=400, detail="User email not found or invalid")

    # Send email with magic link
    activation_link = f"http://localhost:8000/auth/set-password?token={token}"
    send_email(
        to_email=user_email,
        subject="Activate Your Account",
        body=f"""
        <h3>Hi {user.name},</h3>
        <p>Please click the link below to set your password:</p>
        <a href="{activation_link}">{activation_link}</a>
        """
    )
    return token



def set_password(db: Session, token: str, password: str):
    activation = db.query(UserActivation).filter(
        UserActivation.token == token,
        UserActivation.is_used == False,
        UserActivation.expires_at > datetime.utcnow()
    ).first()

    if not activation:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == activation.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.hashed_password = hash_password(password)
    user.is_active = True
    activation.is_used = True
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str) -> str:
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User is not active")

    # Null-safe hashed password check
    hashed_password = user.hashed_password or ""
    if not verify_password(password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate JWT token
    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "role": user.role
    })
    return access_token




def logout_user(token: str):
 
    # Exm: any blacklist logic
    # add_token_to_blacklist(token)
    
    return True





def register_user(db: Session, name: str, email: str):
    # Generate activation token
    token = secrets.token_hex(16)

    # Create user
    user = User(name=name, email=email, token=token)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Send activation email
    activation_link = f"http://localhost:3000/set-password?token={token}"  # React frontend
    body = f"""
        <h3>Hi {name},</h3>
        <p>Click the link below to set your password:</p>
        <a href="{activation_link}">{activation_link}</a>
    """
    send_email(email, "Activate your account", body)

    return user
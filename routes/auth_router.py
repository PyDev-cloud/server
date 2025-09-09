from fastapi import APIRouter, Depends, HTTPException, Request, Body
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import set_password, login_user,logout_user # make sure login_user returns JWT
from utils.security import verify_jwt_token
from schemas.auth_schema import SetPasswordRequest, PasswordSetResponse
from schemas.auth_schema import LoginRequest, TokenResponse
from models.auth_model import UserActivation

router = APIRouter()
templates = Jinja2Templates(directory="templates")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# -----------------------------
# GET HTML form for setting password
# -----------------------------
@router.get("/auth/set-password", response_class=HTMLResponse)
async def get_set_password(request: Request, token: str):
    return templates.TemplateResponse("set_password.html", {"request": request, "token": token})


# -----------------------------
# POST API to set password
# -----------------------------
@router.post("/auth/set-password", response_model=PasswordSetResponse)
async def api_set_password(request: SetPasswordRequest, db: Session = Depends(get_db)):
    user = set_password(db, request.token, request.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    return {"message": "Password set successfully", "user_id": user.id}


# -----------------------------
# POST API for login
# -----------------------------
@router.post("/auth/login", response_model=TokenResponse)
async def api_login(request: LoginRequest = Body(...), db: Session = Depends(get_db)):
    token = login_user(db, request.email, request.password)
    if not token:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"token": token, "message": "Login successful"}


# -----------------------------
# Protected route example
# -----------------------------
@router.get("/users/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = verify_jwt_token(token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user



@router.post("/auth/logout")
async def api_logout(token: str = Depends(oauth2_scheme)):
    logout_user(token)
    return {"message": "Logout successful"}
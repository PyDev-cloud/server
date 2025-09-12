from fastapi import Depends, HTTPException, status
from models.user_model import User
from utils.dependencies import get_current_user

def require_roles(*roles: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.is_super_admin:
            return current_user  # ✅ Super Admin bypasses role check

        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of the roles: {', '.join(roles)}"
            )
        return current_user
    return role_checker

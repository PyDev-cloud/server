from fastapi import HTTPException
from functools import wraps

def require_role(role: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("user")
            if not user or user.role != role:
                raise HTTPException(status_code=403, detail="Not authorized")
            return func(*args, **kwargs)
        return wrapper
    return decorator

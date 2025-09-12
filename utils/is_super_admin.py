from models.user_model import User

def skip_for_super_admin(func):
    def wrapper(current_user: User, *args, **kwargs):
        if current_user.is_super_admin:
            return {"message": "Super Admin — logic skipped"}
        return func(current_user, *args, **kwargs)
    return wrapper

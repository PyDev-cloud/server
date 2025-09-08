# services/instalment_service.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.instalment_model import Instalment
from models.user_model import User
from schemas.Instalment_schema import InstalmentCreate


def create_instalment(db: Session, instalment_data: InstalmentCreate):
    """
    Create instalment for a specific user or all users.
    If user_id is provided, creates for that user.
    Otherwise, creates for all users.
    """
    if instalment_data.user_id:
        # Check if instalment exists for this user & month
        exist = db.query(Instalment).filter(
            and_(
                Instalment.user_id == instalment_data.user_id,
                Instalment.month == instalment_data.month
            )
        ).first()

        if exist:
            return {"message": "Instalment already created for this month"}

        # Create instalment
        instalment = Instalment(
            user_id=instalment_data.user_id,
            month=instalment_data.month,
            amount_due=instalment_data.amount_due
        )
        db.add(instalment)
        db.commit()
        db.refresh(instalment)
        return {"message": "Instalment created successfully", "instalment_id": instalment.id}

    else:
        # Check if instalment exists for all users for this month
        users = db.query(User).all()
        existing_users = db.query(Instalment.user_id).filter(
            Instalment.month == instalment_data.month
        ).all()
        existing_user_ids = {uid for (uid,) in existing_users}

        created_count = 0
        for user in users:
            if user.id in existing_user_ids:
                continue
            instalment = Instalment(
                user_id=user.id,
                month=instalment_data.month,
                amount_due=instalment_data.amount_due
            )
            db.add(instalment)
            created_count += 1

        if created_count == 0:
            return {"error": "Instalment already created for this month for all users"}

        db.commit()
        return {"message": f"Instalments created successfully for {created_count} users"}


def instalment_get_id(db: Session, user_id: int):
    """
    Get all instalments for a specific user
    """
    instalments = db.query(Instalment).filter_by(user_id=user_id).all()
    return instalments

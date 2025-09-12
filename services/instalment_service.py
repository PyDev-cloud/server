from sqlalchemy.orm import Session
from models.user_model import User
from models.instalment_model import Instalment
from models.ledger_model import Ledger, LedgerCategory
from schemas.Instalment_schema import InstalmentCreate
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional
from fastapi import HTTPException, status


# Utility function for role-based access control
def require_roles(user: User, roles: list[str]):
    if user.role not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied: Requires role(s): {', '.join(roles)}"
        )


def create_instalments(db: Session, data: InstalmentCreate, current_user: User):
    require_roles(current_user, ["Finance Secretary", "President"])

    users = []
    if data.user_id:
        user = db.query(User).filter_by(id=data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_super_admin:
            raise HTTPException(status_code=400, detail="Cannot create instalment for Super Admin")
        users.append(user)
    else:
        users = db.query(User).filter(User.is_super_admin == False).all()

    created_count = 0
    today = datetime.today()

    for user in users:
        for month in data.months:
            year = today.year

            exist = db.query(Instalment).filter_by(user_id=user.id, month=month).first()
            if exist:
                continue

            category = db.query(LedgerCategory).filter_by(type="income", month=month).first()
            if not category:
                category = LedgerCategory(
                    name=datetime(year, month, 1).strftime("%B"),
                    type="income",
                    month=month
                )
                db.add(category)
                db.commit()
                db.refresh(category)

            ledger = Ledger(
                user_id=user.id,
                category_id=category.id,
                amount=data.amount_due,
                year=year,
                month=month,
                status="due",
                description=f"{category.name} instalment for {user.name}"
            )
            db.add(ledger)
            db.commit()
            db.refresh(ledger)

            inst = Instalment(
                user_id=user.id,
                ledger_id=ledger.id,
                month=month,
                amount_due=data.amount_due,
                status="due",
                category_id=category.id
            )
            db.add(inst)
            created_count += 1

    db.commit()
    return {"message": f"{created_count} instalments created"}


def create_full_dues_for_user(db: Session, user_id: int, dues_dict: dict, current_user: User):
    require_roles(current_user, ["Finance Secretary", "President"])

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    first_inst = db.query(Instalment)\
        .filter_by(user_id=user.id)\
        .order_by(Instalment.year.asc(), Instalment.month.asc())\
        .first()

    if first_inst:
        start_year = int(first_inst.year)
        start_month = int(first_inst.month)
    else:
        today = datetime.today()
        start_year = today.year
        start_month = today.month

    today = datetime.today()
    current = datetime(start_year, start_month, 1)
    created_count = 0

    while current <= today:
        month = current.month
        year = current.year
        amount_due = dues_dict.get(month, 5000)

        exist_inst = db.query(Instalment).filter_by(user_id=user.id, month=month, year=year).first()
        if not exist_inst:
            inst = Instalment(
                user_id=user.id,
                month=month,
                year=year,
                amount_due=amount_due,
                status="due"
            )
            db.add(inst)
            db.commit()
            db.refresh(inst)
            created_count += 1

            category = db.query(LedgerCategory).filter_by(type="income", month=month).first()
            if not category:
                category = LedgerCategory(
                    name=current.strftime("%B"),
                    type="income",
                    month=month
                )
                db.add(category)
                db.commit()
                db.refresh(category)

            ledger = Ledger(
                user_id=user.id,
                category_id=category.id,
                amount=amount_due,
                year=year,
                month=month,
                status="due",
                description=f"{category.name} instalment for {user.name}"
            )
            db.add(ledger)

        current += relativedelta(months=1)

    db.commit()
    return {"message": f"{created_count} dues created for user {user.name}"}


def get_instalments(db: Session, user_id: Optional[int] = None):
    if user_id:
        return db.query(Instalment).filter(Instalment.user_id == user_id).all()
    return db.query(Instalment).all()


def update_instalment(db: Session, instalment_id: int, data, current_user: User):
    require_roles(current_user, ["Finance Secretary", "President"])

    inst = db.query(Instalment).filter(Instalment.id == instalment_id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instalment not found")

    if data.user_id is not None:
        inst.user_id = data.user_id
    if data.ledger_id is not None:
        inst.ledger_id = data.ledger_id
    if data.amount_due is not None:
        inst.amount_due = data.amount_due
    if data.status is not None:
        inst.status = data.status
    if data.category_id is not None:
        inst.category_id = data.category_id
    if data.month is not None:
        inst.month = data.month

    db.commit()
    db.refresh(inst)
    return inst


def delete_instalment(db: Session, instalment_id: int, current_user: User):
    require_roles(current_user, ["President"])

    inst = db.query(Instalment).filter(Instalment.id == instalment_id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="Instalment not found")

    db.delete(inst)
    db.commit()
    return {"message": "Instalment deleted successfully"}

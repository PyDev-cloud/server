# services/instalment_service.py
from sqlalchemy.orm import Session
from models.user_model import User
from models.instalment_model import Instalment
from models.ledger_model import Ledger,LedgerCategory
from datetime import datetime, timedelta
from schemas.Instalment_schema import InstalmentCreate
from datetime import datetime
from dateutil.relativedelta import relativedelta

from datetime import datetime, timedelta

def create_instalments(db: Session, data: InstalmentCreate):
    users = []
    if data.user_id:
        user = db.query(User).filter_by(id=data.user_id).first()
        if not user:
            raise Exception("User not found")
        users.append(user)
    else:
        users = db.query(User).all()

    created_count = 0
    today = datetime.today()

    for user in users:
        for month in data.months:
            year = today.year

            # একই ইউজার একই মাস, একই বছরে ইন্সটলমেন্ট আছে কিনা চেক
            exist = db.query(Instalment).filter_by(user_id=user.id, month=month).first()
            if exist:
                continue

            # ক্যাটাগরি নিশ্চিত করা
            category = db.query(LedgerCategory).filter_by(type="income", month=month).first()
            if not category:
                category = LedgerCategory(name=datetime(year, month, 1).strftime("%B"), type="income", month=month)
                db.add(category)
                db.commit()
                db.refresh(category)

            # লেজার তৈরি, ইউজার আইডি সহ
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

            # ইন্সটলমেন্ট তৈরি, লেজার আইডি সহ
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








def create_full_dues_for_user(db: Session, user_id: int, dues_dict: dict):
    """
    Auto-create instalments & ledger for a user from their first instalment until now.
    - dues_dict: {month:int -> amount:float}
    """
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise Exception("User not found")

    # প্রথম instalment date বের করা
    first_inst = db.query(Instalment)\
               .filter_by(user_id=user.id)\
               .order_by(Instalment.year.asc(), Instalment.month.asc())\
               .first()
    if first_inst:
        # Column থেকে value নেওয়ার সময় int cast করা
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
        amount_due = dues_dict.get(month, 5000)  # মাস অনুযায়ী default dues

        # Instalment create
        exist_inst = db.query(Instalment).filter_by(user_id=user.id, month=month, year=year).first()
        if not exist_inst:
            inst = Instalment(user_id=user.id, month=month, year=year,
                              amount_due=amount_due, status="due")
            db.add(inst)
            db.commit()
            db.refresh(inst)
            created_count += 1

            # LedgerCategory create if not exists
            category = db.query(LedgerCategory).filter_by(type="income", month=month).first()
            if not category:
                category = LedgerCategory(name=current.strftime("%B"), type="income", month=month)
                db.add(category)
                db.commit()
                db.refresh(category)

            # Ledger create
            ledger = Ledger(user_id=user.id, category_id=category.id, amount=amount_due,
                            year=year, month=month, status="due",
                            description=f"{category.name} instalment for {user.name}")
            db.add(ledger)

        # next month
        current += relativedelta(months=1)

    db.commit()
    return {"message": f"{created_count} dues created for user {user.name}"}

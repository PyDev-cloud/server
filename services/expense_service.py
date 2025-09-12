# services/expense_service.py

from sqlalchemy.orm import Session
from models.expense_model import Expense
from models.ledger_model import LedgerCategory
from models.user_model import User
from schemas.expense_schema import ExpenseCreate
from models.companyAccount_model import CompanyAccount

def create_expense(db: Session, user: User, data: ExpenseCreate):
    if user.role != "Office Admin":
        raise Exception("Only expense managers can create expenses.")

    category = db.query(LedgerCategory).filter_by(id=data.category_id, type="expense").first()
    if not category:
        raise Exception("Invalid expense category.")

    expense = Expense(
        user_id=user.id,
        category_id=data.category_id,
        amount=data.amount,
        description=data.description,
        year=data.year,
        month=data.month,
        status="pending"
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

def approve_by_finance(db: Session, user: User, expense_id: int):
    if user.role != "Finance Secretary":
        raise Exception("Only finance Secretary can approve.")

    expense = db.query(Expense).filter_by(id=expense_id).first()
    if not expense or expense.status != "pending":
        raise Exception("Invalid or already approved expense.")

    expense.status = "finance_approved"
    expense.approved_by_finance = user.id
    db.commit()
    return {"message": "Expense approved by finance manager."}

def approve_by_manager(db: Session, user: User, expense_id: int):
    if user.role != "President":
        raise Exception("Only President can approve.")

    expense = db.query(Expense).filter_by(id=expense_id).first()
    if not expense or expense.status != "finance_approved":
        raise Exception("Expense is not approved by finance yet.")

    # ✅ Company account থেকে ব্যালেন্স কমানো
    company_account = db.query(CompanyAccount).filter_by(id=1).first()
    if not company_account:
        raise Exception("Company account not found")

    if company_account.balance < expense.amount:
        raise Exception("Insufficient company balance.")

    company_account.balance -= expense.amount

    # ✅ Expense status আপডেট
    expense.status = "President_approved"
    expense.approved_by_manager = user.id

    db.commit()
    return {"message": "Expense approved by manager and amount deducted from company account."}

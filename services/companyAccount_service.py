from sqlalchemy.orm import Session
from models.companyAccount_model import CompanyAccount
from schemas.companyAccount_schema import CompanyAccountCreate

def create_company_account(db: Session, data: CompanyAccountCreate):
    account = CompanyAccount(
        account_name=data.account_name,
        bank_name=data.bank_name,
        routing_number=data.routing_number,
        account_number=data.account_number,
        balance=data.balance
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_company_account(db: Session, account_id: int = 1):
    return db.query(CompanyAccount).filter(CompanyAccount.id == account_id).first()

def update_company_balance(db: Session, amount: float, increase: bool = True, account_id: int = 1):
    account = db.query(CompanyAccount).filter_by(id=account_id).first()
    if not account:
        raise Exception("Company account not found")

    if increase:
        account.balance += amount
    else:
        if account.balance < amount:
            raise Exception("Insufficient balance")
        account.balance -= amount

    db.commit()
    db.refresh(account)
    return account

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.bank_account import BankAccount, BankAccountCreate, BankAccountUpdate
from app.crud import bank_account

router = APIRouter(prefix="/bank_accounts", tags=["Banka Hesapları"])

@router.post("/", response_model=BankAccount)
def create_bank_account(account_in: BankAccountCreate, db: Session = Depends(get_db)):
    return bank_account.create(db=db, obj_in=account_in)

@router.get("/", response_model=List[BankAccount])
def list_bank_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return bank_account.get_multi(db=db, skip=skip, limit=limit)

@router.patch("/{account_id}", response_model=BankAccount)
def update_bank_account(account_id: int, account_in: BankAccountUpdate, db: Session = Depends(get_db)):
    db_obj = bank_account.get(db=db, obj_id=account_id)
    return bank_account.update(db=db, db_obj=db_obj, obj_in=account_in)

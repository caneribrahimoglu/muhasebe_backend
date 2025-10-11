from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.cash_account import CashAccount, CashAccountCreate, CashAccountUpdate
from app.crud import cash_account

router = APIRouter(prefix="/cash_accounts", tags=["Kasa Hesapları"])

@router.post("/", response_model=CashAccount)
def create_cash_account(account_in: CashAccountCreate, db: Session = Depends(get_db)):
    return cash_account.create(db=db, obj_in=account_in)

@router.get("/", response_model=List[CashAccount])
def list_cash_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return cash_account.get_multi(db=db, skip=skip, limit=limit)

@router.patch("/{account_id}", response_model=CashAccount)
def update_cash_account(account_id: int, account_in: CashAccountUpdate, db: Session = Depends(get_db)):
    db_obj = cash_account.get(db=db, obj_id=account_id)
    return cash_account.update(db=db, db_obj=db_obj, obj_in=account_in)

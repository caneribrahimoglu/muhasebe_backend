from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.cash_transaction import CashTransaction, CashTransactionCreate
from app.services import cash_service

router = APIRouter(prefix="/cash_transactions", tags=["Kasa Hareketleri"])

@router.post("/", response_model=CashTransaction)
def create_cash_transaction(transaction_in: CashTransactionCreate, db: Session = Depends(get_db)):
    """
    Yeni bir kasa hareketi ekler.
    Bakiye güncellemesi service katmanında otomatik yapılır.
    """
    return cash_service.create_cash_transaction(db=db, transaction_in=transaction_in)


@router.get("/", response_model=List[CashTransaction])
def list_cash_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Tüm kasa hareketlerini listeler.
    """
    return cash_service.get_cash_transactions(db=db, skip=skip, limit=limit)

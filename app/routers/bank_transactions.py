from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.bank_transaction import BankTransaction, BankTransactionCreate
from app.services import bank_service

router = APIRouter(prefix="/bank_transactions", tags=["Banka Hareketleri"])

@router.post("/", response_model=BankTransaction)
def create_bank_transaction(transaction_in: BankTransactionCreate, db: Session = Depends(get_db)):
    """
    Yeni bir banka hareketi oluşturur.
    Bakiye güncellemesi service katmanında yapılır.
    """
    return bank_service.create_bank_transaction(db=db, transaction_in=transaction_in)


@router.get("/", response_model=List[BankTransaction])
def list_bank_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Tüm banka hareketlerini listeler.
    """
    return bank_service.get_bank_transactions(db=db, skip=skip, limit=limit)

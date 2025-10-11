from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.bank_transaction import BankDirection
from app.models.bank_account import BankAccount
from app.schemas.bank_transaction import BankTransactionCreate
from app.crud import bank_transaction, bank_account

def create_bank_transaction(db: Session, transaction_in: BankTransactionCreate):
    """
    Yeni bir banka hareketi oluşturur.
    İş mantığı:
      - GİRİŞ -> hesaba para eklenir
      - ÇIKIŞ -> hesaptan para çıkarılır
    """
    banka = bank_account.get(db, obj_id=transaction_in.bank_account_id)
    if not banka:
        raise HTTPException(status_code=404, detail="Banka hesabı bulunamadı.")

    if transaction_in.direction == BankDirection.CIKIS and banka.balance < transaction_in.amount:
        raise HTTPException(status_code=400, detail="Yetersiz banka bakiyesi.")

    db_txn = bank_transaction.create(db=db, obj_in=transaction_in)

    if transaction_in.direction == BankDirection.GIRIS:
        banka.balance += transaction_in.amount
    else:
        banka.balance -= transaction_in.amount

    db.add(banka)
    db.commit()
    db.refresh(db_txn)
    return db_txn


def get_bank_transactions(db: Session, skip: int = 0, limit: int = 100):
    """
    Tüm banka hareketlerini getirir.
    """
    return bank_transaction.get_multi(db, skip=skip, limit=limit)

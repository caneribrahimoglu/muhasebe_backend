from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.bank_transaction import BankTransaction, BankDirection
from app.models.bank_account import BankAccount
from app.schemas.bank_transaction import BankTransactionCreate
from app.crud import bank_transaction, bank_account

def create_bank_transaction(db: Session, transaction_in: BankTransactionCreate):
    """
    Yeni bir banka hareketi oluşturur.
    - GİRİŞ: hesaba para eklenir
    - ÇIKIŞ: hesaptan para çıkarılır
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
    return bank_transaction.get_multi(db, skip=skip, limit=limit)


def get_bank_transaction_by_id(db: Session, obj_id: int):
    txn = bank_transaction.get(db, obj_id=obj_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Banka hareketi bulunamadı.")
    return txn


def update_bank_transaction(db: Session, obj_id: int, obj_in: BankTransactionCreate):
    db_obj = bank_transaction.get(db, obj_id=obj_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Banka hareketi bulunamadı.")

    banka = bank_account.get(db, obj_id=db_obj.bank_account_id)
    if not banka:
        raise HTTPException(status_code=404, detail="Banka hesabı bulunamadı.")

    # Eski işlemi geri al
    if db_obj.direction == BankDirection.GIRIS:
        banka.balance -= db_obj.amount
    else:
        banka.balance += db_obj.amount

    # Yeni işlemi uygula
    updated_txn = bank_transaction.update(db=db, db_obj=db_obj, obj_in=obj_in)
    if obj_in.direction == BankDirection.GIRIS:
        banka.balance += obj_in.amount
    else:
        banka.balance -= obj_in.amount

    db.add(banka)
    db.commit()
    db.refresh(updated_txn)
    return updated_txn


def delete_bank_transaction(db: Session, obj_id: int):
    txn = bank_transaction.get(db, obj_id=obj_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Banka hareketi bulunamadı.")

    banka = bank_account.get(db, obj_id=txn.bank_account_id)
    if not banka:
        raise HTTPException(status_code=404, detail="Banka hesabı bulunamadı.")

    # Silinen işlemin etkisini geri al
    if txn.direction == BankDirection.GIRIS:
        banka.balance -= txn.amount
    else:
        banka.balance += txn.amount

    bank_transaction.remove(db, obj_id=obj_id)
    db.add(banka)
    db.commit()
    return {"message": "Banka hareketi silindi ve bakiye güncellendi."}

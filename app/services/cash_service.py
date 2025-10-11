from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cash_transaction import CashTransaction, CashDirection
from app.models.cash_account import CashAccount
from app.schemas.cash_transaction import CashTransactionCreate
from app.crud import cash_transaction, cash_account

def create_cash_transaction(db: Session, transaction_in: CashTransactionCreate):
    """
    Yeni bir kasa hareketi oluşturur.
    - GİRİŞ: kasaya para girer -> bakiye artar
    - ÇIKIŞ: kasadan para çıkar -> bakiye azalır
    """
    kasa = cash_account.get(db, obj_id=transaction_in.cash_account_id)
    if not kasa:
        raise HTTPException(status_code=404, detail="Kasa bulunamadı.")

    if transaction_in.direction == CashDirection.CIKIS and kasa.balance < transaction_in.amount:
        raise HTTPException(status_code=400, detail="Yetersiz kasa bakiyesi.")

    db_txn = cash_transaction.create(db=db, obj_in=transaction_in)

    if transaction_in.direction == CashDirection.GIRIS:
        kasa.balance += transaction_in.amount
    else:
        kasa.balance -= transaction_in.amount

    db.add(kasa)
    db.commit()
    db.refresh(db_txn)
    return db_txn


def get_cash_transactions(db: Session, skip: int = 0, limit: int = 100):
    """Tüm kasa hareketlerini döner."""
    return cash_transaction.get_multi(db, skip=skip, limit=limit)


def get_cash_transaction_by_id(db: Session, obj_id: int):
    """Tek bir kasa hareketini getirir."""
    txn = cash_transaction.get(db, obj_id=obj_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Kasa hareketi bulunamadı.")
    return txn


def update_cash_transaction(db: Session, obj_id: int, obj_in: CashTransactionCreate):
    """
    Kasa hareketini günceller.
    Güncellenen tutar veya yön değişirse kasa bakiyesi de düzeltilir.
    """
    db_obj = cash_transaction.get(db, obj_id=obj_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Kasa hareketi bulunamadı.")

    kasa = cash_account.get(db, obj_id=db_obj.cash_account_id)
    if not kasa:
        raise HTTPException(status_code=404, detail="Kasa bulunamadı.")

    # Eski bakiyeyi geri al
    if db_obj.direction == CashDirection.GIRIS:
        kasa.balance -= db_obj.amount
    else:
        kasa.balance += db_obj.amount

    # Yeni verilerle güncelle
    updated_txn = cash_transaction.update(db=db, db_obj=db_obj, obj_in=obj_in)

    # Yeni bakiyeyi uygula
    if obj_in.direction == CashDirection.GIRIS:
        kasa.balance += obj_in.amount
    else:
        kasa.balance -= obj_in.amount

    db.add(kasa)
    db.commit()
    db.refresh(updated_txn)
    return updated_txn


def delete_cash_transaction(db: Session, obj_id: int):
    """
    Kasa hareketini siler.
    Silerken bakiyeyi eski haline getirir.
    """
    txn = cash_transaction.get(db, obj_id=obj_id)
    if not txn:
        raise HTTPException(status_code=404, detail="Kasa hareketi bulunamadı.")

    kasa = cash_account.get(db, obj_id=txn.cash_account_id)
    if not kasa:
        raise HTTPException(status_code=404, detail="Kasa bulunamadı.")

    # Silinen hareketin etkisini geri al
    if txn.direction == CashDirection.GIRIS:
        kasa.balance -= txn.amount
    else:
        kasa.balance += txn.amount

    cash_transaction.remove(db, obj_id=obj_id)
    db.add(kasa)
    db.commit()
    return {"message": "Kasa hareketi silindi ve bakiye güncellendi."}

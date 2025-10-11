from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.cash_transaction import CashDirection
from app.models.cash_account import CashAccount
from app.schemas.cash_transaction import CashTransactionCreate
from app.crud import cash_transaction, cash_account

def create_cash_transaction(db: Session, transaction_in: CashTransactionCreate):
    """
    Yeni bir kasa hareketi oluşturur.
    İş mantığı:
      - Eğer yön GİRİŞ -> kasaya para girer, bakiye artar
      - Eğer yön ÇIKIŞ -> kasadan para çıkar, bakiye azalır
    """
    # İlgili kasayı getir
    kasa = cash_account.get(db, obj_id=transaction_in.cash_account_id)
    if not kasa:
        raise HTTPException(status_code=404, detail="Kasa bulunamadı.")

    # Eğer çıkışsa, bakiye yeterli mi kontrol et
    if transaction_in.direction == CashDirection.CIKIS and kasa.balance < transaction_in.amount:
        raise HTTPException(status_code=400, detail="Yetersiz kasa bakiyesi.")

    # Yeni hareketi oluştur (sadece DB kaydı, iş mantığı değil)
    db_txn = cash_transaction.create(db=db, obj_in=transaction_in)

    # Şimdi bakiyeyi güncelle (iş mantığı burada)
    if transaction_in.direction == CashDirection.GIRIS:
        kasa.balance += transaction_in.amount
    else:
        kasa.balance -= transaction_in.amount

    db.add(kasa)
    db.commit()
    db.refresh(db_txn)
    return db_txn


def get_cash_transactions(db: Session, skip: int = 0, limit: int = 100):
    """
    Tüm kasa hareketlerini getirir.
    """
    return cash_transaction.get_multi(db, skip=skip, limit=limit)

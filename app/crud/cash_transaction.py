from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.cash_transaction import CashTransaction
from app.schemas.cash_transaction import CashTransactionCreate
# Not: Ayrı bir Update şeman yoksa, generic'te Create'i ikinci kez kullanmak PATCH için yeterlidir.
from typing import cast


class CRUDCashTransaction(
    CRUDBase[CashTransaction, CashTransactionCreate, CashTransactionCreate]
):
    """
    Kasa hareketleri için sade CRUD katmanı.
    - İş mantığı (bakiye güncelleme, doğrulama vb.) service katmanında yapılır.
    - Burada sadece ham veritabanı erişimi vardır.
    """

    def get_by_account(self, db: Session, cash_account_id: int) -> list[CashTransaction]:
        result = (
            db.query(self.model)
            .filter(self.model.cash_account_id == cash_account_id)
            .all()
        )
        # IDE'ye iki aşamalı olarak "bilinçli cast" yapıldığını anlatıyoruz
        return cast(list[CashTransaction], cast(object, result))


# IDE'nin metodları (create/get/update/remove) görmesi için instance'ı dosya sonunda, dosya adıyla aynı isimde veriyoruz.
cash_transaction = CRUDCashTransaction(CashTransaction)

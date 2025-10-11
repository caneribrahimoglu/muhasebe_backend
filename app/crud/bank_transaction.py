from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.bank_transaction import BankTransaction
from app.schemas.bank_transaction import BankTransactionCreate
# Not: Ayrı bir Update şeman yoksa, generic'te Create'i ikinci kez kullanmak PATCH için yeterlidir.
from typing import cast


class CRUDBankTransaction(
    CRUDBase[BankTransaction, BankTransactionCreate, BankTransactionCreate]
):
    """
    Banka hareketleri için sade CRUD katmanı.
    - İş mantığı (bakiye güncelleme, doğrulama vb.) service katmanında yapılır.
    - Burada sadece ham veritabanı erişimi vardır.
    """

    def get_by_account(self, db: Session, bank_account_id: int) -> List[BankTransaction]:
        """
        Belirli bir banka hesabına ait tüm hareketleri döndürür.
        Service katmanı raporlama/filtreleme için kullanabilir.
        """
        return cast(
            list[BankTransaction],
            cast(object, db.query(self.model)
                 .filter(self.model.bank_account_id == bank_account_id)
                 .all())
        )


# IDE uyumu ve tutarlılık için instance ismi dosya adıyla aynı.
bank_transaction = CRUDBankTransaction(BankTransaction)

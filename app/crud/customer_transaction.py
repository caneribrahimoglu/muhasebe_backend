from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.customer_transaction import CustomerTransaction
from app.schemas.customer_transaction import (
    CustomerTransactionCreate,
    CustomerTransactionUpdate,
)


class CRUDCustomerTransaction(
    CRUDBase[CustomerTransaction, CustomerTransactionCreate, CustomerTransactionUpdate]
):
    """
    Müşteri hareketleri (borç/alacak) için özel CRUD işlemleri.
    Temel CRUDBase metodlarını (create, get, update, remove) devralır.
    Ayrıca referansa göre hareketleri listelemek için özel metotlar içerir.
    """

    def get_by_reference(self, db: Session, reference_type: str, reference_id: int):
        """
        Belirli bir referansa (örneğin Fatura, Ödeme) bağlı tüm müşteri hareketlerini getirir.
        """
        return (
            db.query(self.model)
            .filter(
                self.model.reference_type == reference_type,
                self.model.reference_id == reference_id,
            )
            .all()
        )


# ✅ CRUD instance
customer_transaction = CRUDCustomerTransaction(CustomerTransaction)

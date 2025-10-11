from app.crud.base import CRUDBase
from app.models.cash_transaction import CashTransaction
from app.schemas.cash_transaction import CashTransactionCreate


class CRUDCashTransaction(CRUDBase[CashTransaction, CashTransactionCreate, CashTransactionCreate]):
    """
    Kasa hareketleri için temel CRUD işlemleri.
    Herhangi bir iş mantığı içermez.
    """
    pass


cash_transaction = CRUDCashTransaction(CashTransaction)

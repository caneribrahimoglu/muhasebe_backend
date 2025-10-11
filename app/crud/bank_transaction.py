from app.crud.base import CRUDBase
from app.models.bank_transaction import BankTransaction
from app.schemas.bank_transaction import BankTransactionCreate


class CRUDBankTransaction(CRUDBase[BankTransaction, BankTransactionCreate, BankTransactionCreate]):
    """
    Banka hareketleri için temel CRUD işlemleri.
    """
    pass


bank_transaction = CRUDBankTransaction(BankTransaction)

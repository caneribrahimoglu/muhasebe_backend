from app.crud.base import CRUDBase
from app.models.bank_account import BankAccount
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate


class CRUDBankAccount(CRUDBase[BankAccount, BankAccountCreate, BankAccountUpdate]):
    """
    Banka hesapları için temel CRUD işlemleri.
    """
    pass


bank_account = CRUDBankAccount(BankAccount)

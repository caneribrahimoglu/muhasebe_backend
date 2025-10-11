from app.crud.base import CRUDBase
from app.models.cash_account import CashAccount
from app.schemas.cash_account import CashAccountCreate, CashAccountUpdate


class CRUDCashAccount(CRUDBase[CashAccount, CashAccountCreate, CashAccountUpdate]):
    """
    Kasa hesapları için temel CRUD işlemleri.
    İş mantığı (örneğin bakiye değişimi) services katmanında yapılır.
    """
    pass


cash_account = CRUDCashAccount(CashAccount)

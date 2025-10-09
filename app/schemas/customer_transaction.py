from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TransactionDirection(str, Enum):
    BORC = "BORC"
    ALACAK = "ALACAK"

class TransactionReference(str, Enum):
    FATURA = "FATURA"
    ODEME = "ODEME"
    IADE = "IADE"


class CustomerTransactionBase(BaseModel):
    customer_id: int
    description: str | None = None
    amount: float
    direction: TransactionDirection
    reference_type: TransactionReference
    reference_id: int | None = None
    balance_after: float | None = None

class CustomerTransactionCreate(CustomerTransactionBase):
    pass

class CustomerTransactionUpdate(CustomerTransactionBase):
    pass

class CustomerTransactionRead(CustomerTransactionBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True

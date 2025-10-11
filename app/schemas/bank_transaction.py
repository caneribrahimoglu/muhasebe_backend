from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.bank_transaction import BankDirection

class BankTransactionBase(BaseModel):
    bank_account_id: int
    direction: BankDirection
    amount: float
    description: Optional[str] = None

class BankTransactionCreate(BankTransactionBase):
    pass

class BankTransaction(BankTransactionBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True

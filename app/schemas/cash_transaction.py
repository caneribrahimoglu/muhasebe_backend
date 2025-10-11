from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.cash_transaction import CashDirection

class CashTransactionBase(BaseModel):
    cash_account_id: int
    direction: CashDirection
    amount: float
    description: Optional[str] = None

class CashTransactionCreate(CashTransactionBase):
    pass

class CashTransaction(CashTransactionBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional

class BankAccountBase(BaseModel):
    bank_name: str
    account_name: str
    iban: Optional[str] = None
    currency: str = "TRY"
    balance: float = 0.0
    is_active: bool = True

class BankAccountCreate(BankAccountBase):
    pass

class BankAccountUpdate(BaseModel):
    bank_name: Optional[str] = None
    account_name: Optional[str] = None
    is_active: Optional[bool] = None

class BankAccount(BankAccountBase):
    id: int

    class Config:
        from_attributes = True

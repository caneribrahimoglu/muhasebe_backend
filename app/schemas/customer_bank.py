from pydantic import BaseModel
from typing import Optional


class CustomerBankBase(BaseModel):
    iban: Optional[str] = None
    bank_name: Optional[str] = None
    branch_name: Optional[str] = None
    branch_code: Optional[str] = None
    account_no: Optional[str] = None


class CustomerBankCreate(CustomerBankBase):
    pass


class CustomerBankUpdate(CustomerBankBase):
    pass


class CustomerBankRead(CustomerBankBase):
    id: int

    model_config = {"from_attributes": True}

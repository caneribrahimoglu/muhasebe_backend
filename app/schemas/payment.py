from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional


class PaymentType(str, Enum):
    TAHSILAT = "TAHSILAT"
    ODEME = "ODEME"


class PaymentMethod(str, Enum):
    NAKIT = "NAKIT"
    HAVALE = "HAVALE"
    KREDI_KARTI = "KREDI_KARTI"
    CEK = "CEK"
    DIGER = "DIGER"


class PaymentBase(BaseModel):
    invoice_id: Optional[int] = None
    customer_id: Optional[int] = None
    amount: float
    payment_type: PaymentType
    method: PaymentMethod = PaymentMethod.NAKIT
    date: Optional[date] = None
    description: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(PaymentBase):
    pass


class PaymentRead(PaymentBase):
    id: int

    model_config = {"from_attributes": True}

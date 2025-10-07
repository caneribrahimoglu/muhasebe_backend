from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from enum import Enum
from app.schemas.invoice_item import InvoiceItemCreate, InvoiceItemRead


class InvoiceType(str, Enum):
    SATIS = "SATIS"
    ALIS = "ALIS"
    IADE = "IADE"


class InvoiceBase(BaseModel):
    invoice_no: Optional[str] = None
    invoice_type: InvoiceType = InvoiceType.SATIS
    customer_id: Optional[int] = None
    date: Optional[date] = None
    currency: str = "TRY"
    description: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate]


class InvoiceUpdate(InvoiceBase):
    items: Optional[List[InvoiceItemCreate]] = []


class InvoiceRead(InvoiceBase):
    id: int
    total_amount: float
    tax_amount: float
    grand_total: float
    items: List[InvoiceItemRead] = []

    model_config = {"from_attributes": True}


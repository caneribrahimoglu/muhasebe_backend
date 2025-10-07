from pydantic import BaseModel
from typing import Optional


class InvoiceItemBase(BaseModel):
    product_id: Optional[int] = None
    quantity: float = 1
    unit_price: float = 0
    vat_rate: float = 0
    total: float = 0


class InvoiceItemCreate(InvoiceItemBase):
    pass


class InvoiceItemRead(InvoiceItemBase):
    id: int
    invoice_id: int

    model_config = {"from_attributes": True}

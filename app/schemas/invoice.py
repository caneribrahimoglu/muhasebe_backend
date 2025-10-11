from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from app.models.invoice import InvoiceType


# --- InvoiceItem (kalem) şeması ---
class InvoiceItemBase(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    vat_rate: float = 20


class InvoiceItemCreate(InvoiceItemBase):
    pass


class InvoiceItemRead(InvoiceItemBase):
    id: int
    total: Optional[float] = 0

    class Config:
        from_attributes = True


# --- Invoice (fatura) şeması ---
class InvoiceBase(BaseModel):
    invoice_no: Optional[str] = None
    invoice_type: InvoiceType                     # SATIS veya ALIS
    customer_id: Optional[int] = None
    date: Optional[date] = None
    currency: str = "TRY"
    description: Optional[str] = None


class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate]
    total_amount: float                            # Faturanın toplam tutarı (vergi dahil)
    payment_method: Optional[str] = None           # "CASH", "BANK" veya None
    cash_account_id: Optional[int] = None          # Ödeme kasaya ise
    bank_account_id: Optional[int] = None          # Ödeme bankaya ise


class InvoiceUpdate(InvoiceBase):
    items: Optional[List[InvoiceItemCreate]] = None
    total_amount: Optional[float] = None
    payment_method: Optional[str] = None
    cash_account_id: Optional[int] = None
    bank_account_id: Optional[int] = None


class InvoiceRead(InvoiceBase):
    id: int
    total_amount: float
    tax_amount: float
    grand_total: float
    balance: float
    items: List[InvoiceItemRead]

    class Config:
        from_attributes = True

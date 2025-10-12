from sqlalchemy import Column, Integer, String, Date, Enum, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
import enum


class InvoiceType(enum.Enum):
    SATIS = "SATIS"
    ALIS = "ALIS"
    IADE = "IADE"


class Invoice(BaseModel):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String(50), unique=True, index=True)
    invoice_type = Column(Enum(InvoiceType), default=InvoiceType.SATIS)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"))
    date = Column(Date)
    currency = Column(String(10), default="TRY")
    total_amount = Column(Float, default=0)
    tax_amount = Column(Float, default=0)
    grand_total = Column(Float, default=0)
    balance = Column(Float, default=0)
    description = Column(String(255))
    payment_method = Column(String, nullable=True)

    customer = relationship("Customer")

    # 🔹 Fatura kalemleri ilişkisi
    items = relationship(
        "InvoiceItem",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

    # 🔹 Stok hareketleri ilişkisi
    stock_movements = relationship(
        "StockMovement",
        back_populates="invoice",
        cascade="all, delete-orphan"
    )

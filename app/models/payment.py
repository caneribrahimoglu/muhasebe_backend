from sqlalchemy import Column, Integer, Float, ForeignKey, Enum, String, Date
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
import enum


class PaymentType(enum.Enum):
    TAHSILAT = "TAHSILAT"
    ODEME = "ODEME"


class PaymentMethod(enum.Enum):
    NAKIT = "NAKIT"
    HAVALE = "HAVALE"
    KREDI_KARTI = "KREDI_KARTI"
    CEK = "CEK"
    DIGER = "DIGER"


class Payment(BaseModel):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="SET NULL"))
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"))
    amount = Column(Float, nullable=False)
    payment_type = Column(Enum(PaymentType), nullable=False)
    method = Column(Enum(PaymentMethod), default=PaymentMethod.NAKIT)
    date = Column(Date)
    description = Column(String(255))

    invoice = relationship("Invoice")
    customer = relationship("Customer")

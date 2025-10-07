from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base_model import BaseModel
import enum


class MovementType(enum.Enum):
    GIRIS = "GIRIS"
    CIKIS = "CIKIS"


class StockMovement(BaseModel):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="SET NULL"))
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"))
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="SET NULL"))

    movement_type = Column(Enum(MovementType))
    quantity = Column(Float, default=0)
    stock_after = Column(Float, default=0)
    description = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product")
    invoice = relationship("Invoice")

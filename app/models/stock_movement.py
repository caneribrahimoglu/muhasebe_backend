from sqlalchemy import Column, Integer, Float, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class MovementType(str, enum.Enum):
    GIRIS = "GIRIS"
    CIKIS = "CIKIS"


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    movement_type = Column(Enum(MovementType), nullable=False)
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    currency = Column(String(10), nullable=False)
    note = Column(String(255))
    stock_after = Column(Float)
    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="SET NULL"))

    invoice = relationship("Invoice", back_populates="stock_movements")

    product = relationship("Product", back_populates="stock_movements")

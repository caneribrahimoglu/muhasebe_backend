from pydantic import BaseModel
from typing import Optional
from enum import Enum


class MovementType(str, Enum):
    GIRIS = "GIRIS"
    CIKIS = "CIKIS"


class StockMovementBase(BaseModel):
    product_id: int
    movement_type: MovementType
    quantity: float
    unit_price: float
    currency: str
    note: Optional[str] = None
    invoice_id: Optional[int] = None  # Artık opsiyonel
    stock_after: Optional[float] = None  # Otomatik hesaplanır


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementRead(StockMovementBase):
    id: int

    class Config:
        from_attributes = True

class StockMovementUpdate(BaseModel):
    """
    Kısmi güncellemeler için şema (PATCH).
    Her alan optional olmalı.
    """
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    movement_type: Optional[MovementType] = None
    reference_type: Optional[str] = None
    reference_id: Optional[int] = None
    description: Optional[str] = None
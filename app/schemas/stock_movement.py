from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


class MovementType(str, Enum):
    GIRIS = "GIRIS"
    CIKIS = "CIKIS"


class StockMovementBase(BaseModel):
    product_id: int
    invoice_id: int
    customer_id: Optional[int] = None
    movement_type: MovementType
    quantity: float
    stock_after: float
    description: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementRead(StockMovementBase):
    id: int
    timestamp: datetime

    model_config = {"from_attributes": True}

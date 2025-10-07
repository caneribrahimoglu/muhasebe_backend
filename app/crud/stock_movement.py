from app.crud.base import CRUDBase
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import StockMovementCreate


class CRUDStockMovement(CRUDBase[StockMovement, StockMovementCreate, StockMovementCreate]):
    pass


crud_stock_movement = CRUDStockMovement(StockMovement)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.stock_movement import StockMovementRead
from app.crud.stock_movement import crud_stock_movement

router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


@router.get("/", response_model=list[StockMovementRead])
def get_all_stock_movements(db: Session = Depends(get_db)):
    return crud_stock_movement.get_multi(db=db)

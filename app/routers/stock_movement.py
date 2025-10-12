from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.stock_movement import StockMovementCreate, StockMovementRead
from app.crud.stock_movement import stock_movement
from app.crud.product import product


router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


@router.post("/", response_model=StockMovementRead)
def create_stock_movement(movement_in: StockMovementCreate, db: Session = Depends(get_db)):
    products = product.get(db, movement_in.product_id)
    if not products:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    qty = movement_in.quantity
    if movement_in.movement_type == "CIKIS":
        if product.stock_amount - qty < 0:
            raise HTTPException(status_code=400, detail="Yetersiz stok")
        product.stock_amount -= qty
    elif movement_in.movement_type == "GIRIS":
        product.stock_amount += qty

    db.commit()
    db.refresh(product)

    # Güncel stok miktarını hareket kaydına da ekleyelim
    movement_data = movement_in.model_dump()
    movement_data["stock_after"] = product.stock_amount

    db_obj = stock_movement.create(db, obj_in=StockMovementCreate(**movement_data))
    return db_obj




@router.get("/", response_model=list[StockMovementRead])
def get_all_stock_movements(db: Session = Depends(get_db)):
    return stock_movement.get_multi(db=db)

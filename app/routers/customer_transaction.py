from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/customer-transactions", tags=["Customer Transactions"])

@router.get("/", response_model=list[schemas.CustomerTransactionRead])
def get_all_transactions(db: Session = Depends(get_db)):
    """
    Tüm cari hareket kayıtlarını döner.
    """
    return crud.crud_customer_transaction.get_multi(db=db)

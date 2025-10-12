from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.customer_transaction import CustomerTransactionRead
from app.crud.customer_transaction import customer_transaction  # ✅ doğru import

router = APIRouter(prefix="/customer-transactions", tags=["Customer Transactions"])


@router.get("/", response_model=list[CustomerTransactionRead])
def get_all_transactions(db: Session = Depends(get_db)):
    """Tüm cari hareketleri döndürür."""
    return customer_transaction.get_multi(db=db)

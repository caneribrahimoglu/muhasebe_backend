from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentRead
from app.crud.payment import crud_payment

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentRead)
def create_payment(payment_in: PaymentCreate, db: Session = Depends(get_db)):
    try:
        return crud_payment.create(db=db, obj_in=payment_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[PaymentRead])
def get_all_payments(db: Session = Depends(get_db)):
    return crud_payment.get_multi(db=db)

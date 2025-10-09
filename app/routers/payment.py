from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.payment import PaymentCreate, PaymentRead
from app.services.payment_service import PaymentService  # ✅ Service katmanını çağıracağız

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentRead)
def create_payment(payment_in: PaymentCreate, db: Session = Depends(get_db)):
    try:
        service = PaymentService(db)
        return service.create_payment(payment_in)  # ✅ artık service katmanı çağrılıyor
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[PaymentRead])
def get_all_payments(db: Session = Depends(get_db)):
    # Bu kısım CRUD çağırmaya devam edebilir çünkü sadece listeleme
    service = PaymentService(db)
    return service.db.query(service.db_model).all()

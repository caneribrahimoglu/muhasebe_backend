from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud._old_customers import customer_crud
from app.schemas import customer as schemas
from app.database import SessionLocal

router = APIRouter(prefix="/customers", tags=["Customers"])


# 🔹 DB bağlantısı (dependency)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Tüm müşterileri getir
@router.get("/", response_model=list[schemas.Customer])
def read_customers(db: Session = Depends(get_db)):
    return customer_crud.get_multi(db)


# 🔹 Tek bir müşteri getir
@router.get("/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = customer_crud.get(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customer


# 🔹 Yeni müşteri oluştur
@router.post("/", response_model=schemas.Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return customer_crud.create(db, customer)


# 🔹 Müşteri güncelle
@router.put("/{customer_id}", response_model=schemas.Customer)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = customer_crud.get(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_crud.update(db, db_customer, customer)


# 🔹 Müşteri sil
@router.delete("/{customer_id}", response_model=schemas.Customer)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    deleted = customer_crud.remove(db, customer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return deleted

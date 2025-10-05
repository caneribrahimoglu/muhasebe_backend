from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.database import get_db
from app.crud import customer as crud_customer

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post("/", response_model=schemas.CustomerRead)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud_customer.create_customer(db=db, customer=customer)


@router.get("/", response_model=List[schemas.CustomerRead])
def get_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = crud_customer.get_customers(db, skip=skip, limit=limit)
    return customers


@router.get("/{customer_id}", response_model=schemas.CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.get_customer(db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.put("/{customer_id}", response_model=schemas.CustomerRead)
def update_customer(customer_id: int, customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud_customer.update_customer(db, customer_id=customer_id, customer=customer)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud_customer.delete_customer(db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"detail": f"Customer {customer_id} deleted successfully"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas, database


router = APIRouter(
    prefix="/customer",
    tags=["customer"]
)

@router.get("/", response_model=list[schemas.Customer])
def read_customers(db: Session = Depends(database.get_db)):
    return crud.get_customers(db)

@router.post("/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(database.get_db)):
    return crud.create_customer(db=db, customer=customer)


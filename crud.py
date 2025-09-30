from sqlalchemy.orm import Session
import models, schemas



def get_customers(db: Session) -> list[models.Customer]:
    return db.query(models.Customer).all()


def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

from sqlalchemy.orm import Session
from app import models, schemas


def create_customer_address(db: Session, customer_id: int, address: schemas.CustomerAddressCreate):
    db_address = models.CustomerAddress(**address.model_dump(), customer_id=customer_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_customer_addresses(db: Session, customer_id: int):
    return db.query(models.CustomerAddress).filter(models.CustomerAddress.customer_id == customer_id).all()


def update_customer_address(db: Session, address_id: int, address: schemas.CustomerAddressUpdate):
    db_address = db.query(models.CustomerAddress).filter(models.CustomerAddress.id == address_id).first()
    if not db_address:
        return None
    for key, value in address.model_dump(exclude_unset=True).items():
        setattr(db_address, key, value)
    db.commit()
    db.refresh(db_address)
    return db_address


def delete_customer_address(db: Session, address_id: int):
    db_address = db.query(models.CustomerAddress).filter(models.CustomerAddress.id == address_id).first()
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address

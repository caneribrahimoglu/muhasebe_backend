from sqlalchemy.orm import Session
from app import models, schemas


def create_customer_bank(db: Session, customer_id: int, bank: schemas.CustomerBankCreate):
    db_bank = models.CustomerBank(**bank.model_dump(), customer_id=customer_id)
    db.add(db_bank)
    db.commit()
    db.refresh(db_bank)
    return db_bank


def get_customer_banks(db: Session, customer_id: int):
    return db.query(models.CustomerBank).filter(models.CustomerBank.customer_id == customer_id).all()


def update_customer_bank(db: Session, bank_id: int, bank: schemas.CustomerBankUpdate):
    db_bank = db.query(models.CustomerBank).filter(models.CustomerBank.id == bank_id).first()
    if not db_bank:
        return None
    for key, value in bank.model_dump(exclude_unset=True).items():
        setattr(db_bank, key, value)
    db.commit()
    db.refresh(db_bank)
    return db_bank


def delete_customer_bank(db: Session, bank_id: int):
    db_bank = db.query(models.CustomerBank).filter(models.CustomerBank.id == bank_id).first()
    if db_bank:
        db.delete(db_bank)
        db.commit()
    return db_bank


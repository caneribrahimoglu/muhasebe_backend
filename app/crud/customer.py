from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app import models, schemas


class CRUDCustomer(CRUDBase[models.Customer, schemas.CustomerCreate, schemas.CustomerUpdate]):
    def create(self, db: Session, obj_in: schemas.CustomerCreate):
        # 1️⃣ Pydantic objesini dict’e çevir, alt ilişkileri ayıkla
        obj_data = obj_in.model_dump(exclude={"addresses", "banks"})

        # 2️⃣ Ana müşteri kaydını oluştur
        db_customer = models.Customer(**obj_data)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)

        # 3️⃣ Alt ilişkileri oluştur
        if obj_in.addresses:
            for addr in obj_in.addresses:
                db_address = models.CustomerAddress(**addr.model_dump(), customer_id=db_customer.id)
                db.add(db_address)

        if obj_in.banks:
            for bank in obj_in.banks:
                db_bank = models.CustomerBank(**bank.model_dump(), customer_id=db_customer.id)
                db.add(db_bank)

        db.commit()
        db.refresh(db_customer)
        return db_customer

    def update(self, db: Session, db_obj: models.Customer, obj_in: schemas.CustomerUpdate):
        # 1️⃣ Ana müşteri alanlarını güncelle
        update_data = obj_in.model_dump(exclude_unset=True, exclude={"addresses", "banks"})
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        # 2️⃣ Adresleri yönet
        if obj_in.addresses is not None:
            existing_addresses = {addr.id: addr for addr in db_obj.addresses if addr.id}
            new_addresses = []

            for addr_in in obj_in.addresses:
                if addr_in.id and addr_in.id in existing_addresses:
                    # Güncelle
                    db_addr = existing_addresses[addr_in.id]
                    for key, value in addr_in.model_dump(exclude_unset=True).items():
                        setattr(db_addr, key, value)
                else:
                    # Yeni adres
                    new_addr = models.CustomerAddress(**addr_in.model_dump(), customer_id=db_obj.id)
                    new_addresses.append(new_addr)

            # Silinmeyen ID'leri belirle
            incoming_ids = {a.id for a in obj_in.addresses if a.id}
            for addr in db_obj.addresses[:]:
                if addr.id not in incoming_ids:
                    db.delete(addr)

            db_obj.addresses.extend(new_addresses)

        # 3️⃣ Bankaları yönet
        if obj_in.banks is not None:
            existing_banks = {bank.id: bank for bank in db_obj.banks if bank.id}
            new_banks = []

            for bank_in in obj_in.banks:
                if bank_in.id and bank_in.id in existing_banks:
                    # Güncelle
                    db_bank = existing_banks[bank_in.id]
                    for key, value in bank_in.model_dump(exclude_unset=True).items():
                        setattr(db_bank, key, value)
                else:
                    # Yeni banka
                    new_bank = models.CustomerBank(**bank_in.model_dump(), customer_id=db_obj.id)
                    new_banks.append(new_bank)

            incoming_bank_ids = {b.id for b in obj_in.banks if b.id}
            for bank in db_obj.banks[:]:
                if bank.id not in incoming_bank_ids:
                    db.delete(bank)

            db_obj.banks.extend(new_banks)

        db.commit()
        db.refresh(db_obj)
        return db_obj


# Dışa aktarılan CRUD nesnesi
customer = CRUDCustomer(models.Customer)

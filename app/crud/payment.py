from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate
from app.models.invoice import Invoice
from sqlalchemy import func



class CRUDPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):
    def create(self, db: Session, obj_in: PaymentCreate):
        # Fatura ve müşteri doğrulaması
        if obj_in.invoice_id:
            invoice = db.query(Invoice).get(obj_in.invoice_id)
            if not invoice:
                raise ValueError("İlgili fatura bulunamadı.")
            obj_in.customer_id = invoice.customer_id

        db_obj = self.model(**obj_in.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        # Fatura bakiyesi güncelle
        if obj_in.invoice_id:
            total_paid = (
                db.query(self.model)
                .filter(Payment.invoice_id == obj_in.invoice_id)
                .with_entities(func.sum(Payment.amount))
                .scalar()
                or 0
            )
            invoice.balance = max(invoice.grand_total - total_paid, 0)
            db.add(invoice)
            db.commit()

        return db_obj



payment = CRUDPayment(Payment)

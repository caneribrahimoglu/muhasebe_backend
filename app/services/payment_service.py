from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.crud.payment import payment
from app.crud.customer_transaction import customer_transaction
from app.crud.cash_transaction import cash_transaction
from app.crud.bank_transaction import bank_transaction
from app.crud.invoice import invoice

from app.models.customer_transaction import TransactionDirection
from app.models.cash_transaction import CashDirection
from app.models.bank_transaction import BankDirection
from app.schemas.payment import PaymentCreate


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    def create_payment(self, payment_in: PaymentCreate):
        """Yeni ödeme/tahsilat oluşturur ve ilgili hesapları günceller."""
        try:
            # --- 1️⃣ Ödemeyi kaydet ---
            db_payment = payment.create(db=self.db, obj_in=payment_in)

            # --- 2️⃣ Cari hareket oluştur ---
            customer_data = {
                "customer_id": payment_in.customer_id,
                "amount": payment_in.amount,
                "direction": (
                    TransactionDirection.ALACAK
                    if payment_in.is_collection
                    else TransactionDirection.BORC
                ),
                "reference_type": "ODEME",
                "reference_id": db_payment.id,
                "description": f"Ödeme #{db_payment.id}",
            }
            customer_transaction.create(db=self.db, obj_in=customer_data)

            # --- 3️⃣ Kasa veya Banka hareketi oluştur ---
            if payment_in.cash_account_id:
                cash_data = {
                    "cash_account_id": payment_in.cash_account_id,
                    "amount": payment_in.amount,
                    "direction": (
                        CashDirection.GIRIS
                        if payment_in.is_collection
                        else CashDirection.CIKIS
                    ),
                    "reference_type": "ODEME",
                    "reference_id": db_payment.id,
                    "description": f"Kasa hareketi (Ödeme #{db_payment.id})",
                }
                cash_transaction.create(db=self.db, obj_in=cash_data)

            elif payment_in.bank_account_id:
                bank_data = {
                    "bank_account_id": payment_in.bank_account_id,
                    "amount": payment_in.amount,
                    "direction": (
                        BankDirection.GIRIS
                        if payment_in.is_collection
                        else BankDirection.CIKIS
                    ),
                    "reference_type": "ODEME",
                    "reference_id": db_payment.id,
                    "description": f"Banka hareketi (Ödeme #{db_payment.id})",
                }
                bank_transaction.create(db=self.db, obj_in=bank_data)

            # --- 4️⃣ Fatura bakiyesini güncelle ---
            if payment_in.invoice_id:
                db_invoice = invoice.get(self.db, payment_in.invoice_id)
                if db_invoice:
                    total_paid = (
                        self.db.query(payment.model.amount)
                        .filter(payment.model.invoice_id == db_invoice.id)
                        .all()
                    )
                    total_paid_sum = sum(p[0] for p in total_paid)
                    db_invoice.balance = max(db_invoice.grand_total - total_paid_sum, 0)
                    self.db.add(db_invoice)

            # --- 5️⃣ Commit ---
            self.db.commit()
            self.db.refresh(db_payment)
            return db_payment

        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Ödeme oluşturulurken hata: {str(e)}") from e

    def get_all_payments(self, skip: int = 0, limit: int = 100):
        """Tüm ödemeleri döndürür."""
        return payment.get_multi(db=self.db, skip=skip, limit=limit)

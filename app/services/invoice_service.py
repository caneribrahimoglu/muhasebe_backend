from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceType
from app.crud import (
    invoice,
    stock_movement,
    customer_transaction,
    payment,
)
from app.models.stock_movement import MovementType
from app.models.customer_transaction import TransactionDirection


class InvoiceService:
    def __init__(self, db: Session):
        self.db = db

    # -------------------- CREATE --------------------
    def create_invoice(self, invoice_in: InvoiceCreate) -> InvoiceRead:
        """Yeni fatura oluşturur ve bağlı stok/cari hareketlerini kaydeder."""
        try:
            db_invoice = invoice.create(db=self.db, obj_in=invoice_in)

            # --- Stok hareketleri ---
            for item in invoice_in.items:
                stock_data = {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "movement_type": (
                        MovementType.CIKIS if invoice_in.invoice_type == InvoiceType.SATIS else MovementType.GIRIS
                    ),
                    "reference_type": "FATURA",
                    "reference_id": db_invoice.id,
                    "description": f"Fatura #{db_invoice.id} ({invoice_in.invoice_type.value})",
                }
                stock_movement.create(db=self.db, obj_in=stock_data)

            # --- Cari hareketi ---
            customer_data = {
                "customer_id": invoice_in.customer_id,
                "amount": sum(item.quantity * item.unit_price for item in invoice_in.items),
                "direction": (
                    TransactionDirection.BORC if invoice_in.invoice_type == InvoiceType.SATIS
                    else TransactionDirection.ALACAK
                ),
                "reference_type": "FATURA",
                "reference_id": db_invoice.id,
                "description": f"Fatura #{db_invoice.id}",
            }
            customer_transaction.create(db=self.db, obj_in=customer_data)

            self.db.commit()
            self.db.refresh(db_invoice)
            return db_invoice

        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Fatura oluşturulurken hata: {str(e)}") from e

    # -------------------- DELETE --------------------
    def delete_invoice(self, invoice_id: int) -> bool:
        """Faturayı ve ona bağlı tüm hareketleri güvenli şekilde siler."""
        try:
            db_invoice = invoice.get(self.db, invoice_id)
            if not db_invoice:
                return False

            # --- 1️⃣ İlişkili stok hareketlerini sil ---
            stock_moves = stock_movement.get_by_reference(
                db=self.db, reference_type="FATURA", reference_id=invoice_id
            )
            for sm in stock_moves:
                self.db.delete(sm)

            # --- 2️⃣ İlişkili cari hareketlerini sil ---
            cust_tx = customer_transaction.get_by_reference(
                db=self.db, reference_type="FATURA", reference_id=invoice_id
            )
            for ct in cust_tx:
                self.db.delete(ct)

            # --- 3️⃣ İlişkili ödemeleri sil (ve bağlı hareketler cascade ise onlar da gider) ---
            payments = (
                self.db.query(payment.model)
                .filter(payment.model.invoice_id == invoice_id)
                .all()
            )
            for p in payments:
                self.db.delete(p)

            # --- 4️⃣ Faturayı sil ---
            self.db.delete(db_invoice)

            # --- 5️⃣ Commit ---
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Fatura silinirken hata: {str(e)}") from e

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app import models
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceType
from app.models.stock_movement import MovementType
from app.models.customer_transaction import TransactionDirection
from app.crud.invoice import invoice
from app.crud.payment import payment


class InvoiceService:
    def __init__(self, db: Session):
        self.db = db

    # -------------------- Fatura No Üretici --------------------
    def _generate_invoice_no(self) -> str:
        """Otomatik, benzersiz fatura numarası üretir (örnek: FTR-20251012-0003)."""
        today_str = datetime.now().strftime("%Y%m%d")

        last_invoice = (
            self.db.query(models.Invoice)
            .filter(models.Invoice.invoice_no.like(f"FTR-{today_str}-%"))
            .order_by(models.Invoice.id.desc())
            .first()
        )

        if last_invoice and last_invoice.invoice_no:
            try:
                last_number = int(last_invoice.invoice_no.split("-")[-1])
            except ValueError:
                last_number = 0
        else:
            last_number = 0

        new_number = last_number + 1
        return f"FTR-{today_str}-{new_number:04d}"

    # -------------------- CREATE --------------------
    def create_invoice(self, invoice_in: InvoiceCreate) -> InvoiceRead:
        """
        Yeni fatura oluşturur; kalemleri, stok hareketlerini ve cari hareketini
        TEK transaction içinde yazar. Başarısızlıkta hepsi rollback olur.
        """
        try:
            # 1️⃣ Fatura verisi (items hariç)
            invoice_data = invoice_in.model_dump(exclude={"items"})
            if not invoice_data.get("invoice_no"):
                invoice_data["invoice_no"] = self._generate_invoice_no()

            # 2️⃣ Faturayı ekle, id almak için flush
            db_invoice = models.Invoice(**invoice_data)
            self.db.add(db_invoice)
            self.db.flush()  # id üretildi, commit yok

            # 3️⃣ Kalemleri ekle + stok hareketi + stok güncelleme
            direction = (
                MovementType.CIKIS if invoice_in.invoice_type == InvoiceType.SATIS else MovementType.GIRIS
            )

            for item_in in invoice_in.items:
                # 🧾 InvoiceItem
                db_item = models.InvoiceItem(
                    invoice_id=db_invoice.id,
                    product_id=item_in.product_id,
                    quantity=item_in.quantity,
                    unit_price=item_in.unit_price,
                    vat_rate=item_in.vat_rate,
                )
                self.db.add(db_item)

                # 🔄 Ürün stok güncellemesi
                product = self.db.query(models.Product).filter(models.Product.id == item_in.product_id).first()
                if product:
                    if invoice_in.invoice_type == InvoiceType.SATIS:
                        product.stock_amount -= item_in.quantity
                    else:
                        product.stock_amount += item_in.quantity
                    stock_after_value = product.stock_amount
                else:
                    stock_after_value = None

                # 📦 Stok hareketi
                db_sm = models.StockMovement(
                    product_id=item_in.product_id,
                    quantity=item_in.quantity,
                    unit_price=item_in.unit_price,
                    movement_type=direction,
                    currency=invoice_in.currency,
                    reference_type="FATURA",
                    reference_id=db_invoice.id,
                    description=f"Fatura #{db_invoice.id} ({invoice_in.invoice_type.value})",
                    stock_after=stock_after_value,  # 🔥 yeni eklenen alan
                )
                self.db.add(db_sm)

            # 4️⃣ Cari hareketi (borç/alacak)
            total_amount = sum(item.quantity * item.unit_price for item in invoice_in.items)
            ct_direction = (
                TransactionDirection.BORC
                if invoice_in.invoice_type == InvoiceType.SATIS
                else TransactionDirection.ALACAK
            )

            db_ct = models.CustomerTransaction(
                customer_id=invoice_in.customer_id,
                amount=total_amount,
                direction=ct_direction,
                reference_type="FATURA",
                reference_id=db_invoice.id,
                description=f"Fatura #{db_invoice.id}",
            )
            self.db.add(db_ct)

            # 5️⃣ Tek commit — atomik işlem
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

            # 🧹 Stok hareketleri
            stock_moves = (
                self.db.query(models.StockMovement)
                .filter(
                    models.StockMovement.reference_type == "FATURA",
                    models.StockMovement.reference_id == invoice_id,
                )
                .all()
            )
            for sm in stock_moves:
                self.db.delete(sm)

            # 🧹 Cari hareketleri
            cust_tx = (
                self.db.query(models.CustomerTransaction)
                .filter(
                    models.CustomerTransaction.reference_type == "FATURA",
                    models.CustomerTransaction.reference_id == invoice_id,
                )
                .all()
            )
            for ct in cust_tx:
                self.db.delete(ct)

            # 🧹 Ödemeler
            payments = (
                self.db.query(payment.model)
                .filter(payment.model.invoice_id == invoice_id)
                .all()
            )
            for p in payments:
                self.db.delete(p)

            # 🧹 Fatura kalemleri
            for item in db_invoice.items:
                self.db.delete(item)

            # 🧹 Fatura
            self.db.delete(db_invoice)
            self.db.commit()
            return True

        except SQLAlchemyError as e:
            self.db.rollback()
            raise RuntimeError(f"Fatura silinirken hata: {str(e)}") from e

    # -------------------- READ --------------------
    def get_all_invoices(self, skip: int = 0, limit: int = 100):
        """Tüm faturaları döndürür."""
        return invoice.get_multi(db=self.db, skip=skip, limit=limit)

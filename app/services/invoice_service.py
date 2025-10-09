from app.services.service_base import ServiceBase
from app.crud.invoice import crud_invoice
from app.models.customer_transaction import TransactionDirection, TransactionReference
from app.models.stock_movement import MovementType
from app.services.customer_service import CustomerService
from app.schemas.stock_movement import StockMovementCreate
from app.schemas.invoice import InvoiceCreate
from app.crud.product import crud_product
from app.crud.stock_movement import crud_stock_movement


class InvoiceService(ServiceBase):
    """
    Fatura işlemleri servis katmanı.
    Fatura oluşturma, stok düşümü, cari işlemler gibi süreçleri yönetir.
    """

    def create_invoice(self, obj_in: InvoiceCreate):
        # 1️⃣ Fatura iskeletini oluştur
        invoice = crud_invoice.create_skeleton(self.db, obj_in)

        total = 0
        tax_total = 0

        # 2️⃣ Kalemleri ekle ve stokları düş
        for item in obj_in.items:
            crud_invoice.add_item(self.db, invoice_id=invoice.id, item=item)

            product = crud_product.get(self.db, item.product_id)
            if not product:
                raise ValueError(f"Ürün bulunamadı (ID: {item.product_id})")

            # Stok azalt
            if product.stock_amount is not None:
                product.stock_amount -= item.quantity
                if product.stock_amount < 0:
                    raise ValueError(f"Stok yetersiz: {product.name}")
                self.db.commit()
                self.db.refresh(product)

            # Stok hareketi kaydet
            stock_movement = StockMovementCreate(
                product_id=item.product_id,
                movement_type=MovementType.CIKIS if obj_in.invoice_type == "SATIS" else MovementType.GIRIS,
                quantity=item.quantity,
                unit_price=item.unit_price,
                currency=obj_in.currency,
                note=f"Satış faturası #{invoice.id}" if obj_in.invoice_type == "SATIS" else f"Alış faturası #{invoice.id}",
                invoice_id=invoice.id,
                stock_after=product.stock_amount
            )
            crud_stock_movement.create(self.db, stock_movement)

            # Toplam hesapla
            total += item.unit_price * item.quantity
            tax_total += (item.unit_price * item.quantity) * (item.vat_rate / 100)

        # 3️⃣ Fatura toplamlarını güncelle
        crud_invoice.finalize_totals(self.db, invoice_id=invoice.id, total=total, tax=tax_total)

        # 4️⃣ Cari hareket kaydı oluştur
        customer_service = CustomerService(self.db)
        customer_service.record_transaction(
            customer_id=invoice.customer_id,
            amount=total + tax_total,
            direction=TransactionDirection.BORC if obj_in.invoice_type == "SATIS" else TransactionDirection.ALACAK,
            description=f"Satış faturası #{invoice.id}" if obj_in.invoice_type == "SATIS" else f"Alış faturası #{invoice.id}",
            reference_type=TransactionReference.FATURA,
            reference_id=invoice.id
        )

        return invoice

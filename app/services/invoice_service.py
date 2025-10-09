# app/services/invoice_service.py
from sqlalchemy.orm import Session
from app.services.service_base import ServiceBase
from app.services.stock_service import StockService
from app.services.customer_service import CustomerService
from app.crud.invoice import crud_invoice
from app.crud.product import crud_product
from app.schemas.invoice import InvoiceCreate, InvoiceItemCreate, InvoiceType
from app.schemas.stock_movement import MovementType

class InvoiceService(ServiceBase):
    """
    Fatura işlemleri servis katmanı.
    Fatura oluşturma, stok ve cari güncellemelerini yönetir.
    """

    def __init__(self, db: Session):
        super().__init__(db)
        self.stock_service = StockService(db)
        self.customer_service = CustomerService(db)

    def create_invoice(self, data: InvoiceCreate):
        try:
            # 1. Faturayı oluştur
            invoice = crud_invoice.create_skeleton(self.db, data)

            total = 0.0
            tax = 0.0

            # 2. Fatura kalemlerini işle
            for item in data.items or []:
                product = crud_product.get(self.db, item.product_id)
                if not product:
                    raise ValueError(f"Ürün bulunamadı (id={item.product_id})")

                # Kalemi ekle
                crud_invoice.add_item(self.db, invoice_id=invoice.id, item=item)

                # Tutarları hesapla
                line_total = item.quantity * item.unit_price
                line_tax = line_total * (item.vat_rate / 100.0)
                total += line_total
                tax += line_tax

                # Stok hareketi oluştur
                if data.invoice_type == InvoiceType.SATIS:
                    self.stock_service.adjust_stock(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                        currency=data.currency,
                        movement_type=MovementType.CIKIS,
                        note=f"Satış faturası #{invoice.id}",
                        invoice_id=invoice.id,
                    )
                elif data.invoice_type == InvoiceType.ALIS:
                    self.stock_service.adjust_stock(
                        product_id=item.product_id,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                        currency=data.currency,
                        movement_type=MovementType.GIRIS,
                        note=f"Alış faturası #{invoice.id}",
                        invoice_id=invoice.id,
                    )

            # 3. Fatura toplamlarını finalize et
            crud_invoice.finalize_totals(
                self.db,
                invoice_id=invoice.id,
                total=total,
                tax=tax,
            )

            # 4. Cari bakiyesini güncelle
            if data.customer_id:
                if data.invoice_type == InvoiceType.SATIS:
                    self.customer_service.add_debt(data.customer_id, total + tax)
                elif data.invoice_type == InvoiceType.ALIS:
                    self.customer_service.add_credit(data.customer_id, total + tax)

            self.db.refresh(invoice)
            return invoice

        except Exception as e:
            self.db.rollback()
            raise e

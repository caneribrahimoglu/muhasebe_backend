from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud.base import CRUDBase
from app.models.invoice import Invoice, InvoiceType
from app.models.invoice_item import InvoiceItem
from app.models.product import Product
from app.models.stock_movement import MovementType
from app.crud.stock_movement import crud_stock_movement
from app.schemas.invoice import InvoiceCreate, InvoiceUpdate
from app.schemas.stock_movement import StockMovementCreate  # ✅ eklendi


class CRUDInvoice(CRUDBase[Invoice, InvoiceCreate, InvoiceUpdate]):
    def create(self, db: Session, obj_in: InvoiceCreate):
        items_data = obj_in.items
        obj_data = obj_in.model_dump(exclude={"items"})
        invoice = self.model(**obj_data)

        total = 0
        tax = 0
        invoice_type = obj_in.invoice_type
        db.add(invoice)
        db.flush()  # invoice.id’yi almak için

        for item in items_data:
            # Kalem tutarını hesapla
            line_total = item.quantity * item.unit_price
            line_tax = line_total * (item.vat_rate / 100)
            total += line_total
            tax += line_tax

            db_item = InvoiceItem(**item.model_dump(), total=line_total + line_tax)
            invoice.items.append(db_item)

            # Ürünü bul
            product = db.query(Product).get(item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Ürün (ID={item.product_id}) bulunamadı.")

            # Hareket yönünü belirle
            movement_type = None

            if invoice_type == InvoiceType.SATIS:
                if product.stock_amount < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"{product.name} ürününde yeterli stok yok. "
                               f"Mevcut: {product.stock_amount}, Gerekli: {item.quantity}"
                    )
                product.stock_amount -= item.quantity
                movement_type = MovementType.CIKIS

            elif invoice_type == InvoiceType.ALIS:
                product.stock_amount += item.quantity
                movement_type = MovementType.GIRIS

            elif invoice_type == InvoiceType.IADE:
                if obj_in.invoice_type == InvoiceType.SATIS:
                    product.stock_amount += item.quantity
                    movement_type = MovementType.GIRIS
                else:
                    if product.stock_amount < item.quantity:
                        raise HTTPException(
                            status_code=400,
                            detail=f"{product.name} için iade yapılamıyor, yeterli stok yok."
                        )
                    product.stock_amount -= item.quantity
                    movement_type = MovementType.CIKIS

            else:
                raise HTTPException(status_code=400, detail=f"Geçersiz fatura tipi: {invoice_type}")

            # Stok hareketi oluştur
            movement_data = {
                "product_id": product.id,
                "invoice_id": invoice.id,
                "movement_type": movement_type,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "currency": invoice.currency,
                "stock_after": product.stock_amount,
                "note": f"Fatura: {invoice.invoice_no} ({invoice_type.value})"
            }

            # ✅ dict yerine Pydantic model veriyoruz
            crud_stock_movement.create(db=db, obj_in=StockMovementCreate(**movement_data))

        # Fatura toplamlarını yaz
        invoice.total_amount = total
        invoice.tax_amount = tax
        invoice.grand_total = total + tax
        invoice.balance = invoice.grand_total

        db.commit()
        db.refresh(invoice)
        return invoice


crud_invoice = CRUDInvoice(Invoice)

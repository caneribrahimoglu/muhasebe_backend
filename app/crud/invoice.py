from sqlalchemy.orm import Session
from app.models.invoice import Invoice as InvoiceModel
from app.models.invoice_item import InvoiceItem as InvoiceItemModel
from app.schemas.invoice import InvoiceCreate, InvoiceItemCreate, InvoiceUpdate
from app.crud.base import CRUDBase

class CRUDInvoice(CRUDBase[InvoiceModel, InvoiceCreate, InvoiceUpdate]):
    def create_skeleton(self, db: Session, obj_in: InvoiceCreate) -> InvoiceModel:
        """Kalemler hariç fatura iskeletini oluşturur."""
        data = obj_in.model_dump(exclude={'items'})
        invoice = InvoiceModel(**data)
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice

    def add_item(self, db: Session, *, invoice_id: int, item: InvoiceItemCreate) -> InvoiceItemModel:
        """Faturaya yeni kalem ekler."""
        db_item = InvoiceItemModel(invoice_id=invoice_id, **item.model_dump())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def finalize_totals(self, db: Session, *, invoice_id: int, total: float, tax: float) -> InvoiceModel:
        """Toplam tutarları ve vergiyi fatura üzerine yazar."""
        invoice = db.query(InvoiceModel).filter(InvoiceModel.id == invoice_id).first()
        if not invoice:
            raise ValueError("Fatura bulunamadı.")
        invoice.total_amount = total
        invoice.tax_amount = tax
        invoice.grand_total = total + tax
        db.commit()
        db.refresh(invoice)
        return invoice


invoice = CRUDInvoice(InvoiceModel)

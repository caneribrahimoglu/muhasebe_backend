from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.invoice import crud_invoice
from app.crud.product import crud_product
from app.crud.stock_movement import crud_stock_movement
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceType
from app.schemas.stock_movement import StockMovementCreate


router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceRead)
def create_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    # Yeni fatura kaydı
    db_invoice = crud_invoice.create(db, obj_in=invoice_in)
    db.commit()
    db.refresh(db_invoice)

    # Her satır için stok hareketi oluştur
    for item in invoice_in.items:
        product = crud_product.get(db, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Ürün ID {item.product_id} bulunamadı")
        if invoice_in.invoice_type == InvoiceType.SATIS and product.stock_amount - item.quantity < 0:
            raise HTTPException(status_code=400, detail=f"Yetersiz stok: {product.name}")
        # Stok güncelle
        if invoice_in.invoice_type == InvoiceType.SATIS:
            product.stock_amount -= item.quantity
        elif invoice_in.invoice_type == InvoiceType.ALIS:
            product.stock_amount += item.quantity
        db.add(product)

        # Hareket kaydı
        movement_data = {
            "product_id": item.product_id,
            "movement_type": "CIKIS" if invoice_in.invoice_type == InvoiceType.SATIS else "GIRIS",
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "currency": invoice_in.currency,
            "note": invoice_in.invoice_no,
            "invoice_id": db_invoice.id,
            "stock_after": product.stock_amount,
        }
        crud_stock_movement.create(db, obj_in=StockMovementCreate(**movement_data))

    db.commit()
    db.refresh(db_invoice)
    return db_invoice


@router.get("/", response_model=list[InvoiceRead])
def get_all_invoices(db: Session = Depends(get_db)):
    return crud_invoice.get_multi(db=db)


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_obj = crud_invoice.get(db=db, obj_id=invoice_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Fatura bulunamadı")
    return db_obj


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    db_obj = crud_invoice.remove(db=db, obj_id=invoice_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Fatura zaten silinmiş veya mevcut değil")
    return {"ok": True}

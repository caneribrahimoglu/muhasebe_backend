from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.invoice import crud_invoice
from app.crud.product import crud_product
from app.crud.stock_movement import crud_stock_movement
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceType
from app.schemas.stock_movement import StockMovementCreate
from app.services.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceRead)
def create_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    service = InvoiceService(db)
    return service.create_invoice(invoice_in)


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

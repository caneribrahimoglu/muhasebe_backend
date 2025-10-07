from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceRead, InvoiceUpdate
from app.crud.invoice import crud_invoice

router = APIRouter(prefix="/invoices", tags=["Invoices"])


@router.post("/", response_model=InvoiceRead)
def create_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    return crud_invoice.create(db=db, obj_in=invoice_in)


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

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.invoice import InvoiceCreate, InvoiceRead
from app.services.invoice_service import InvoiceService


router = APIRouter(prefix="/invoices", tags=["Faturalar"])


@router.post("/", response_model=InvoiceRead)
def create_invoice(invoice_in: InvoiceCreate, db: Session = Depends(get_db)):
    """
    Yeni bir fatura oluşturur.
    İş mantığı service katmanında yürür:
      - Fatura kaydı oluşturulur.
      - Stok hareketleri otomatik eklenir.
      - Cari bakiyesi güncellenir.
      - (Varsa) Kasa/Banka hareketi oluşturulur.
    """
    service = InvoiceService(db)
    return service.create_invoice(invoice_in)


@router.get("/", response_model=List[InvoiceRead])
def list_invoices(db: Session = Depends(get_db)):
    """
    Tüm faturaları listeler.
    """
    service = InvoiceService(db)
    return service.get_all_invoices()


@router.get("/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Tek bir faturayı getirir.
    """
    service = InvoiceService(db)
    invoice = service.get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Fatura bulunamadı.")
    return invoice


@router.delete("/{invoice_id}")
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """
    Faturayı siler ve ilişkili hareketleri geri alır:
      - Stoklar iade edilir.
      - Cari bakiyesi düzeltilir.
      - (Varsa) Kasa/Banka hareketi iptal edilir.
    """
    service = InvoiceService(db)
    result = service.delete_invoice(invoice_id)
    if not result:
        raise HTTPException(status_code=404, detail="Fatura zaten silinmiş veya mevcut değil.")
    return {"message": "Fatura başarıyla silindi ve tüm bağlı işlemler geri alındı."}

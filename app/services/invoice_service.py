from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.crud import invoice, stock_movement, customer_transaction
from app.schemas.invoice import InvoiceCreate
from app.models.stock_movement import MovementType
from app.models.customer_transaction import TransactionDirection
from app.models.invoice import InvoiceType
from app.services import cash_service, bank_service
from app.schemas.cash_transaction import CashTransactionCreate
from app.schemas.bank_transaction import BankTransactionCreate


class InvoiceService:
    """
    Fatura ile ilişkili tüm iş mantığını yöneten sınıf.
    Zincir:
      Fatura -> Stok -> Cari -> (Kasa/Banka)
    """

    def __init__(self, db: Session):
        self.db = db

    # 1️⃣ Fatura oluşturma
    def create_invoice(self, invoice_in: InvoiceCreate):
        db_invoice = invoice.create(db=self.db, obj_in=invoice_in)

        # Stok hareketleri
        for item in invoice_in.items:
            stock_data = {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "direction": MovementType.CIKIS if invoice_in.invoice_type == InvoiceType.SATIS else MovementType.GIRIS,
                "reference_type": "FATURA",
                "reference_id": db_invoice.id,
                "description": f"Fatura #{db_invoice.id} - {invoice_in.invoice_type.value}",
            }
            stock_movement.create(db=self.db, obj_in=stock_data)

        # Cari hareket
        customer_data = {
            "customer_id": invoice_in.customer_id,
            "amount": invoice_in.total_amount,
            "direction": TransactionDirection.BORC if invoice_in.invoice_type == InvoiceType.SATIS else TransactionDirection.ALACAK,
            "reference_type": "FATURA",
            "reference_id": db_invoice.id,
            "description": f"Fatura #{db_invoice.id}",
        }
        customer_transaction.create(db=self.db, obj_in=customer_data)

        # Kasa/Banka işlemi (opsiyonel)
        if invoice_in.payment_method == "CASH" and invoice_in.cash_account_id:
            txn = CashTransactionCreate(
                cash_account_id=invoice_in.cash_account_id,
                direction="GIRIS" if invoice_in.invoice_type == InvoiceType.SATIS else "CIKIS",
                amount=invoice_in.total_amount,
                description=f"Fatura #{db_invoice.id} ödemesi",
            )
            cash_service.create_cash_transaction(db=self.db, transaction_in=txn)

        elif invoice_in.payment_method == "BANK" and invoice_in.bank_account_id:
            txn = BankTransactionCreate(
                bank_account_id=invoice_in.bank_account_id,
                direction="GIRIS" if invoice_in.invoice_type == InvoiceType.SATIS else "CIKIS",
                amount=invoice_in.total_amount,
                description=f"Fatura #{db_invoice.id} ödemesi",
            )
            bank_service.create_bank_transaction(db=self.db, transaction_in=txn)

        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice

    # 2️⃣ Tüm faturaları getir
    def get_all_invoices(self):
        return invoice.get_multi(db=self.db)

    # 3️⃣ Tek fatura getir
    def get_invoice_by_id(self, invoice_id: int):
        db_invoice = invoice.get(db=self.db, obj_id=invoice_id)
        if not db_invoice:
            raise HTTPException(status_code=404, detail="Fatura bulunamadı.")
        return db_invoice

    # 4️⃣ Fatura silme (zincirli geri alma)
    def delete_invoice(self, invoice_id: int):
        db_invoice = invoice.get(db=self.db, obj_id=invoice_id)
        if not db_invoice:
            raise HTTPException(status_code=404, detail="Fatura bulunamadı.")

        # İlgili stok hareketlerini geri al
        related_stocks = stock_movement.get_by_reference(self.db, "FATURA", invoice_id)
        for s in related_stocks:
            reverse_direction = MovementType.GIRIS if s.direction == MovementType.CIKIS else MovementType.CIKIS
            stock_movement.create(
                db=self.db,
                obj_in={
                    "product_id": s.product_id,
                    "quantity": s.quantity,
                    "direction": reverse_direction,
                    "reference_type": "FATURA_IPTAL",
                    "reference_id": invoice_id,
                    "description": f"Fatura #{invoice_id} iptali",
                },
            )

        # Cari bakiyeyi geri al
        related_txn = customer_transaction.get_by_reference(self.db, "FATURA", invoice_id)
        for t in related_txn:
            reverse_dir = TransactionDirection.ALACAK if t.direction == TransactionDirection.BORC else TransactionDirection.BORC
            customer_transaction.create(
                db=self.db,
                obj_in={
                    "customer_id": t.customer_id,
                    "amount": t.amount,
                    "direction": reverse_dir,
                    "reference_type": "FATURA_IPTAL",
                    "reference_id": invoice_id,
                    "description": f"Fatura #{invoice_id} iptali",
                },
            )

        # Faturayı sil
        invoice.remove(db=self.db, obj_id=invoice_id)
        self.db.commit()
        return True

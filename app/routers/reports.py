from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.database import get_db
from app.models.customer import Customer
from app.models.invoice import Invoice, InvoiceType
from app.models.payment import Payment, PaymentType

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/customer-balance")
def get_customer_balance(db: Session = Depends(get_db)):
    """
    Her müşterinin toplam borç, alacak ve net bakiyesini döndürür.
    """
    invoice_subq = (
        db.query(
            Invoice.customer_id.label("customer_id"),
            func.sum(
                case(
                    (Invoice.invoice_type == InvoiceType.SATIS, Invoice.grand_total),
                    (Invoice.invoice_type == InvoiceType.IADE, -Invoice.grand_total),
                    else_=0,
                )
            ).label("invoice_total")
        )
        .group_by(Invoice.customer_id)
        .subquery()
    )

    payment_subq = (
        db.query(
            Payment.customer_id.label("customer_id"),
            func.sum(
                case(
                    (Payment.payment_type == PaymentType.TAHSILAT, Payment.amount),
                    (Payment.payment_type == PaymentType.ODEME, -Payment.amount),
                    else_=0,
                )
            ).label("payment_total")
        )
        .group_by(Payment.customer_id)
        .subquery()
    )

    query = (
        db.query(
            Customer.id,
            Customer.title,
            func.coalesce(invoice_subq.c.invoice_total, 0).label("total_invoices"),
            func.coalesce(payment_subq.c.payment_total, 0).label("total_payments"),
            (
                func.coalesce(invoice_subq.c.invoice_total, 0)
                - func.coalesce(payment_subq.c.payment_total, 0)
            ).label("balance"),
        )
        .outerjoin(invoice_subq, Customer.id == invoice_subq.c.customer_id)
        .outerjoin(payment_subq, Customer.id == payment_subq.c.customer_id)
        .order_by(Customer.title)
    )

    results = query.all()

    report = []
    for r in results:
        report.append({
            "customer_id": r.id,
            "customer_name": r.title,
            "total_invoices": round(r.total_invoices, 2),
            "total_payments": round(r.total_payments, 2),
            "balance": round(r.balance, 2),
            "status": "Borçlu" if r.balance > 0 else ("Alacaklı" if r.balance < 0 else "Kapalı")
        })

    return report

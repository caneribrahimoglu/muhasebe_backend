# app/models/__init__.py

# -------------------- Cari (Müşteri) --------------------
from app.models.customer import Customer
from app.models.customer_address import CustomerAddress
from app.models.customer_bank import CustomerBank

# -------------------- Ürünler --------------------
from app.models.product import Product
from app.models.product_compatibility import ProductCompatibility

# -------------------- Fatura --------------------
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem


# -------------------- Stok ve Hareketler --------------------
from app.models.stock_movement import StockMovement
from app.models.customer_transaction import CustomerTransaction
from app.models.cash_transaction import CashTransaction
from app.models.bank_transaction import BankTransaction

# -------------------- Ödemeler --------------------
from app.models.payment import Payment

# -------------------- Export Listesi --------------------
__all__ = [
    # Cari
    "Customer",
    "CustomerAddress",
    "CustomerBank",

    # Ürün
    "Product",
    "ProductCompatibility",

    # Fatura
    "Invoice",
    "InvoiceItem",

    # Hareketler
    "StockMovement",
    "CustomerTransaction",
    "CashTransaction",
    "BankTransaction",

    # Ödeme
    "Payment",
]

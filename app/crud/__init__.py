# --- Customer CRUD'ları ---
from .customer import customer
from .customer_address import customer_address
from .customer_bank import customer_bank
from .customer_transaction import customer_transaction

# --- Product CRUD'ları ---
from .product import product
from .product_compatibility import product_compatibility

# --- Invoice ve Kalem CRUD'ları ---
from .invoice import invoice
# Eğer invoice_item.py varsa:
# from .invoice_item import invoice_item

# --- Stock CRUD ---
from .stock_movement import stock_movement

# --- Payment ve İlgili CRUD'lar ---
from .payment import payment
from .cash_account import cash_account
from .cash_transaction import cash_transaction
from .bank_account import bank_account
from .bank_transaction import bank_transaction

# --- Eski veya ek CRUD'lar ---
# from .old_customers import old_customers  # Gerekirse

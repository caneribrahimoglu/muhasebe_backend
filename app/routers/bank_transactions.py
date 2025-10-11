from app.routers.base_service import generate_service_router
from app.services import bank_service
from app.schemas.bank_transaction import BankTransaction, BankTransactionCreate

# Banka hareketleri için service tabanlı router
router = generate_service_router(
    name="bank_transactions",
    service_create_func=bank_service.create_bank_transaction,
    service_get_func=bank_service.get_bank_transactions,
    response_schema=BankTransaction,
    create_schema=BankTransactionCreate,
    prefix="/bank_transactions",
    tags=["Banka Hareketleri"]
)

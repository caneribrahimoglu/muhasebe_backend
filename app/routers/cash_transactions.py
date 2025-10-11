from app.routers.base_service import generate_service_router
from app.services import cash_service
from app.schemas.cash_transaction import CashTransaction, CashTransactionCreate

# Kasa hareketleri için service tabanlı router
router = generate_service_router(
    name="cash_transactions",
    service_create_func=cash_service.create_cash_transaction,
    service_get_func=cash_service.get_cash_transactions,
    response_schema=CashTransaction,
    create_schema=CashTransactionCreate,
    prefix="/cash_transactions",
    tags=["Kasa Hareketleri"]
)

from app.routers.base import generate_router
from app.crud import cash_account
from app.schemas.cash_account import CashAccount, CashAccountCreate, CashAccountUpdate

# Kasa hesapları için klasik CRUD router
# İş mantığı yok (sadece CRUD), o yüzden base router kullanıyoruz.
router = generate_router(
    name="cash_accounts",
    crud=cash_account,
    schema=CashAccount,
    create_schema=CashAccountCreate,
    update_schema=CashAccountUpdate,
    prefix="/cash_accounts",
    tags=["Kasa Hesapları"]
)

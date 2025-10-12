from app.routers.base import generate_router
from app.crud.bank_account import bank_account
from app.schemas.bank_account import BankAccount, BankAccountCreate, BankAccountUpdate

# Banka hesapları da sadece CRUD içerir.
router = generate_router(
    name="bank_accounts",
    crud=bank_account,
    schema=BankAccount,
    create_schema=BankAccountCreate,
    update_schema=BankAccountUpdate,
    prefix="/bank_accounts",
    tags=["Banka Hesapları"]
)

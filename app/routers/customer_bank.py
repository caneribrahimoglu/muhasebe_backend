from app.routers.base import generate_router
from app import schemas
from app.crud.customer_bank import customer_bank

router = generate_router(
    name="CustomerBank",
    crud=customer_bank,
    schema=schemas.CustomerBank,
    create_schema=schemas.CustomerBankCreate,
    update_schema=schemas.CustomerBankUpdate,
    prefix="/customer-banks",
    tags=["Customer Banks"]
)

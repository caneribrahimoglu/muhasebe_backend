from app.routers.base import generate_router
from app import crud, schemas

router = generate_router(
    name="CustomerBank",
    crud=crud.customer_bank,
    schema=schemas.CustomerBank,
    create_schema=schemas.CustomerBankCreate,
    update_schema=schemas.CustomerBankUpdate,
    prefix="/customer-banks",
    tags=["Customer Banks"]
)

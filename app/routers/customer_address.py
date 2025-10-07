from app.routers.base import generate_router
from app import crud, schemas

router = generate_router(
    name="CustomerAddress",
    crud=crud.customer_address,
    schema=schemas.CustomerAddress,
    create_schema=schemas.CustomerAddressCreate,
    update_schema=schemas.CustomerAddressUpdate,
    prefix="/customer-addresses",
    tags=["Customer Addresses"]
)

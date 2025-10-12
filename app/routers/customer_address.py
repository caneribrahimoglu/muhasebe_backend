from app.routers.base import generate_router
from app import schemas
from app.crud.customer_address import  customer_address

router = generate_router(
    name="CustomerAddress",
    crud=customer_address,
    schema=schemas.CustomerAddress,
    create_schema=schemas.CustomerAddressCreate,
    update_schema=schemas.CustomerAddressUpdate,
    prefix="/customer-addresses",
    tags=["Customer Addresses"]
)

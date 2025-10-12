from app.routers.base import generate_router
from app import schemas
from app.crud.customer import customer

router = generate_router(
    name="Customer",
    crud=customer,
    schema=schemas.Customer,
    create_schema=schemas.CustomerCreate,
    update_schema=schemas.CustomerUpdate,
    prefix="/customers",
    tags=["Customers"]
)

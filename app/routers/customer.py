from app.routers.base import generate_router
from app import crud, schemas

router = generate_router(
    name="Customer",
    crud=crud.crud_customer,
    schema=schemas.Customer,
    create_schema=schemas.CustomerCreate,
    update_schema=schemas.CustomerUpdate,
    prefix="/customers",
    tags=["Customers"]
)

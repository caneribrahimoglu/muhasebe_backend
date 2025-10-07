from app.crud.base import CRUDBase
from app.models.product_compatibility import ProductCompatibility
from app.schemas.product_compatibility import (
    ProductCompatibilityCreate,
    ProductCompatibilityUpdate,
)


class CRUDProductCompatibility(
    CRUDBase[ProductCompatibility, ProductCompatibilityCreate, ProductCompatibilityUpdate]
):
    pass


crud_product_compatibility = CRUDProductCompatibility(ProductCompatibility)

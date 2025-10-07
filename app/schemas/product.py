from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from app.schemas.product_compatibility import ProductCompatibilityRead, ProductCompatibilityCreate, ProductCompatibilityUpdate


class ProductType(str, Enum):
    TICARI_MAL = "TICARI_MAL"
    HIZMET = "HIZMET"
    SARF_MALZEMESI = "SARF_MALZEMESI"
    DIGER = "DIGER"


class ProductBase(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    barcode: Optional[str] = None
    vat_rate: Optional[float] = 0
    purchase_price: Optional[float] = 0
    sales_price: Optional[float] = 0
    stock_amount: Optional[float] = 0
    critical_stock: Optional[float] = 0
    currency: Optional[str] = "TRY"
    is_active: Optional[bool] = True
    product_type: Optional[ProductType] = ProductType.TICARI_MAL


class ProductCreate(ProductBase):
    compatibilities: Optional[List[ProductCompatibilityCreate]] = []


class ProductUpdate(ProductBase):
    compatibilities: Optional[List[ProductCompatibilityUpdate]] = []


class ProductRead(ProductBase):
    id: int
    compatibilities: List[ProductCompatibilityRead] = []

    model_config = {"from_attributes": True}

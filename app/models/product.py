from sqlalchemy import Column, Integer, String, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel
import enum



class ProductType(enum.Enum):
    TICARI_MAL = "TICARI_MAL"
    HIZMET = "HIZMET"
    SARF_MALZEMESI = "SARF_MALZEMESI"
    DIGER = "DIGER"


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    brand = Column(String(100))
    unit = Column(String(50))
    barcode = Column(String(100))
    vat_rate = Column(Float, default=0)
    purchase_price = Column(Float, default=0)
    sales_price = Column(Float, default=0)
    stock_amount = Column(Float, default=0)
    critical_stock = Column(Float, default=0)
    currency = Column(String(10), default="TRY")
    is_active = Column(Boolean, default=True)
    product_type = Column(Enum(ProductType), default=ProductType.TICARI_MAL)

    # İlişki
    compatibilities = relationship(
        "ProductCompatibility",
        back_populates="product",
        cascade="all, delete-orphan"
    )

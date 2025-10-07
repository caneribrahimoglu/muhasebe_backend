from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class ProductCompatibility(BaseModel):
    __tablename__ = "product_compatibilities"

    __table_args__ = (
        UniqueConstraint("product_id", "brand_name", "model_codes", name="uq_product_brand_model"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    # Bu alanlar birebir senin kullandığın sistemin mantığına göre:
    brand_name = Column(String(100), index=True)
    model_codes = Column(String(500))  # bir satırda birden fazla model olabilir
    search_text = Column(String(600), index=True    )  # arama kolaylığı için markalar + modeller birleştirilebilir

    product = relationship("Product", back_populates="compatibilities")

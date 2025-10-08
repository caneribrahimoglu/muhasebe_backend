from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class ProductCompatibility(BaseModel):
    __tablename__ = "product_compatibilities"

    __table_args__ = (
        UniqueConstraint("product_id", "brand", "model_code", name="uq_product_brand_model"),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    brand = Column(String(100), index=True)
    model_code = Column(String(500))  # tek model
    search_text = Column(String(600), index=True)

    product = relationship("Product", back_populates="compatibilities")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base_model import BaseModel


class ProductCompatibility(BaseModel):
    __tablename__ = "product_compatibilities"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))

    # Bu alanlar birebir senin kullandığın sistemin mantığına göre:
    brand_name = Column(String(100), index=True)
    model_codes = Column(String(500))  # bir satırda birden fazla model olabilir
    search_text = Column(String(600))  # arama kolaylığı için markalar + modeller birleştirilebilir

    product = relationship("Product", back_populates="compatibilities")

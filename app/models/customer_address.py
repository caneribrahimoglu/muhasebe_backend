from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CustomerAddress(Base):
    __tablename__ = "customer_addresses"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))

    address_name = Column(String(100))
    country = Column(String(50))
    address_type = Column(String(50))  # "Fatura" / "Teslimat"
    city = Column(String(100))
    district = Column(String(100))
    neighborhood = Column(String(100))
    town = Column(String(100))
    postal_code = Column(String(20))
    address = Column(String(500))
    phone1 = Column(String(20))
    phone2 = Column(String(20))
    mobile1 = Column(String(20))
    mobile2 = Column(String(20))
    email1 = Column(String(150))
    email2 = Column(String(150))

    customer = relationship("Customer", back_populates="addresses")

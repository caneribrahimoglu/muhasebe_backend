from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CustomerBank(Base):
    __tablename__ = "customer_banks"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))

    iban = Column(String(50))
    bank_name = Column(String(100))
    branch_name = Column(String(100))
    branch_code = Column(String(20))
    account_no = Column(String(50))

    customer = relationship("Customer", back_populates="banks")

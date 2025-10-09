from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from enum import Enum
from app.database import Base

class TransactionDirection(str, Enum):
    BORC = "BORC"
    ALACAK = "ALACAK"

class TransactionReference(str, Enum):
    FATURA = "FATURA"
    ODEME = "ODEME"
    IADE = "IADE"


class CustomerTransaction(Base):
    __tablename__ = "customer_transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id", ondelete="CASCADE"))
    date = Column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    direction = Column(SqlEnum(TransactionDirection), nullable=False)
    reference_type = Column(SqlEnum(TransactionReference), nullable=False)
    reference_id = Column(Integer, nullable=True)
    balance_after = Column(Float, nullable=True)

    customer = relationship("Customer", back_populates="transactions")

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class BankDirection(str, enum.Enum):
    """
    Banka hareket yönü:
    GİRİŞ -> hesaba para girişi
    ÇIKIŞ -> hesaptan para çıkışı
    """
    GIRIS = "GIRIS"
    CIKIS = "CIKIS"

class BankTransaction(Base):
    """
    Banka hesabı hareket tablosu.
    """
    __tablename__ = "bank_transactions"

    id = Column(Integer, primary_key=True, index=True)
    bank_account_id = Column(Integer, ForeignKey("bank_accounts.id"))
    direction = Column(Enum(BankDirection), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    # Bağlantı: hareketin ait olduğu banka hesabı
    bank_account = relationship("BankAccount", backref="transactions")

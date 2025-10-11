from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

class CashDirection(str, enum.Enum):
    """
    Para akış yönü:
    GİRİŞ -> kasaya para girişi
    ÇIKIŞ -> kasadan çıkan para
    """
    GIRIS = "GIRIS"
    CIKIS = "CIKIS"

class CashTransaction(Base):
    """
    Kasa hareket tablosu.
    Kasa içerisindeki nakit giriş/çıkışlarını kaydeder.
    """
    __tablename__ = "cash_transactions"

    id = Column(Integer, primary_key=True, index=True)
    cash_account_id = Column(Integer, ForeignKey("cash_accounts.id"))
    direction = Column(Enum(CashDirection), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    # İlişki: bu hareket hangi kasaya ait
    cash_account = relationship("CashAccount", backref="transactions")

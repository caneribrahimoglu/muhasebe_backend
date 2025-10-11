from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class CashAccount(Base):
    """
    Şirketin kasalarını temsil eder.
    Örnek: 'Merkez Kasa', 'Şube 1 Kasa' gibi.
    """
    __tablename__ = "cash_accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)   # Kasaya verilen isim
    balance = Column(Float, default=0.0)                 # Kasadaki toplam bakiye
    is_active = Column(Boolean, default=True)            # Pasif edilmiş kasa olabilir

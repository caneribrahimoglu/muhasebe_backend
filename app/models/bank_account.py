from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class BankAccount(Base):
    """
    Şirketin banka hesaplarını temsil eder.
    Örnek: Ziraat Bankası TL Hesabı, İş Bankası Dolar Hesabı.
    """
    __tablename__ = "bank_accounts"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, nullable=False)           # Banka adı
    account_name = Column(String, nullable=False)        # Hesap açıklaması
    iban = Column(String, unique=True)                   # IBAN numarası (benzersiz)
    currency = Column(String, default="TRY")             # Hesabın para birimi
    balance = Column(Float, default=0.0)                 # Mevcut bakiye
    is_active = Column(Boolean, default=True)

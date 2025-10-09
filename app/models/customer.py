from sqlalchemy import Column, Integer, String, Boolean, Enum, Date, Float
from sqlalchemy.orm import relationship
#from app.database import Base
from app.models.base_model import BaseModel
import enum


class CustomerType(enum.Enum):
    ALICI = "ALICI"
    SATICI = "SATICI"


class InstitutionType(enum.Enum):
    SAHIS = "SAHIS"
    KURUM = "KURUM"


class Currency(enum.Enum):
    TRY = "TRY"
    USD = "USD"
    EUR = "EUR"


class Customer(BaseModel):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True)
    type = Column(Enum(CustomerType), nullable=False)
    institution_type = Column(Enum(InstitutionType), nullable=False)

    category = Column(String(100))
    title = Column(String(200))
    name = Column(String(150))
    tax_office = Column(String(100))
    tax_number = Column(String(20))
    tc_no = Column(String(20))
    mersis_no = Column(String(30))
    kep_address = Column(String(150))

    group1 = Column(String(100))
    group2 = Column(String(100))
    group3 = Column(String(100))
    group4 = Column(String(100))
    birth_date = Column(Date)

    # Finansal bilgiler
    currency = Column(Enum(Currency), default=Currency.TRY)
    deposit_amount = Column(Float, default=0)
    open_account_limit = Column(Float, default=0)
    credit_limit = Column(Float, default=0)
    account_cut_day = Column(Integer, default=0)
    term_day = Column(Integer, default=0)
    grace_day = Column(Integer, default=0)
    default_purchase_discount = Column(Float, default=0)
    default_sales_discount = Column(Float, default=0)

    # Kontrol alanları
    send_statement = Column(Boolean, default=False)
    limit_control = Column(Boolean, default=False)
    is_credit_customer = Column(Boolean, default=False)
    use_pos_device = Column(Boolean, default=False)

    # İlişkiler
    addresses = relationship("CustomerAddress", back_populates="customer", cascade="all, delete-orphan")
    banks = relationship("CustomerBank", back_populates="customer", cascade="all, delete-orphan")
    transactions = relationship("CustomerTransaction", back_populates="customer", cascade="all, delete-orphan")


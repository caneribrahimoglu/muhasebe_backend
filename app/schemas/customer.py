from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from app.schemas.customer_address import CustomerAddressRead
from app.schemas.customer_bank import CustomerBankRead


class CustomerType(str, Enum):
    ALICI = "ALICI"
    SATICI = "SATICI"


class InstitutionType(str, Enum):
    SAHIS = "SAHIS"
    KURUM = "KURUM"


class Currency(str, Enum):
    TRY = "TRY"
    USD = "USD"
    EUR = "EUR"


class CustomerBase(BaseModel):
    code: Optional[str] = None
    type: Optional[CustomerType] = CustomerType.ALICI
    institution_type: Optional[InstitutionType] = InstitutionType.SAHIS
    category: Optional[str] = None
    title: Optional[str] = None
    name: Optional[str] = None
    tax_office: Optional[str] = None
    tax_number: Optional[str] = None
    tc_no: Optional[str] = None
    mersis_no: Optional[str] = None
    kep_address: Optional[str] = None

    group1: Optional[str] = None
    group2: Optional[str] = None
    group3: Optional[str] = None
    group4: Optional[str] = None
    birth_date: Optional[date] = None

    currency: Optional[Currency] = Currency.TRY
    deposit_amount: Optional[float] = 0
    open_account_limit: Optional[float] = 0
    credit_limit: Optional[float] = 0
    account_cut_day: Optional[int] = 0
    term_day: Optional[int] = 0
    grace_day: Optional[int] = 0
    default_purchase_discount: Optional[float] = 0
    default_sales_discount: Optional[float] = 0

    send_statement: Optional[bool] = False
    limit_control: Optional[bool] = False
    is_credit_customer: Optional[bool] = False
    use_pos_device: Optional[bool] = False


class CustomerCreate(CustomerBase):
    addresses: Optional[List["CustomerAddressCreate"]] = []
    banks: Optional[List["CustomerBankCreate"]] = []


class CustomerUpdate(CustomerBase):
    addresses: Optional[List["CustomerAddressUpdate"]] = []
    banks: Optional[List["CustomerBankUpdate"]] = []


class CustomerRead(CustomerBase):
    id: int
    addresses: List[CustomerAddressRead] = []
    banks: List[CustomerBankRead] = []

    #Zaman damgaları (ekledik)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


from app.schemas.customer_address import CustomerAddressCreate, CustomerAddressUpdate
from app.schemas.customer_bank import CustomerBankCreate, CustomerBankUpdate
Customer = CustomerRead


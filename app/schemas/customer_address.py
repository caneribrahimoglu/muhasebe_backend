from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerAddressBase(BaseModel):
    address_name: Optional[str] = None
    country: Optional[str] = "TÜRKİYE"
    address_type: Optional[str] = None  # "Fatura" veya "Teslimat"
    city: Optional[str] = None
    district: Optional[str] = None
    neighborhood: Optional[str] = None
    town: Optional[str] = None
    postal_code: Optional[str] = None
    address: Optional[str] = None
    phone1: Optional[str] = None
    phone2: Optional[str] = None
    mobile1: Optional[str] = None
    mobile2: Optional[str] = None
    email1: Optional[EmailStr] = None
    email2: Optional[EmailStr] = None


class CustomerAddressCreate(CustomerAddressBase):
    pass


class CustomerAddressUpdate(CustomerAddressBase):
    id: Optional[int] = None   # 🔥 Güncelleme için ekledik


class CustomerAddressRead(CustomerAddressBase):
    id: int

    model_config = {"from_attributes": True}

CustomerAddress = CustomerAddressRead

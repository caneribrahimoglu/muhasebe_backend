from pydantic import BaseModel, EmailStr, ConfigDict

class CustomerBase(BaseModel):
    name: str
    email: EmailStr

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    # Kısmi güncelleme için alanlar opsiyonel
    name: str | None = None
    email: EmailStr | None = None


class Customer(CustomerBase):
    id : int
    # SQLAlchemy objesini Pydantic modele dönüştürmek için (Pydantic v2)
    model_config = ConfigDict(from_attributes=True)
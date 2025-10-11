from pydantic import BaseModel
from typing import Optional

class CashAccountBase(BaseModel):
    name: str
    balance: float = 0.0
    is_active: bool = True

class CashAccountCreate(CashAccountBase):
    """
    Yeni kasa oluştururken kullanılacak schema.
    """
    pass

class CashAccountUpdate(BaseModel):
    """
    Kasa güncellemesi (örneğin isim değişikliği, pasifleştirme)
    """
    name: Optional[str] = None
    is_active: Optional[bool] = None

class CashAccount(CashAccountBase):
    id: int

    class Config:
        from_attributes = True  # ORM objelerini JSON’a çevirirken kullanılır

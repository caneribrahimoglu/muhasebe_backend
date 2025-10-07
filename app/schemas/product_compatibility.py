from pydantic import BaseModel

class ProductCompatibilityBase(BaseModel):
    brand: str
    model_code: str
    search_text: str | None = None


class ProductCompatibilityCreate(ProductCompatibilityBase):
    pass


class ProductCompatibilityUpdate(ProductCompatibilityBase):
    pass


class ProductCompatibilityRead(ProductCompatibilityBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True

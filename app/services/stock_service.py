# app/services/stock_service.py
from app.services.service_base import ServiceBase
from app.crud.product import crud_product
from app.crud.stock_movement import crud_stock_movement
from app.schemas.stock_movement import StockMovementCreate, MovementType

class StockService(ServiceBase):
    """
    Stok yönetimi servis katmanı.
    Ürün stoklarını günceller ve stok hareketlerini kaydeder.
    """

    def adjust_stock(
        self,
        *,
        product_id: int,
        quantity: float,
        unit_price: float,
        currency: str,
        movement_type: MovementType,
        note: str | None = None,
        invoice_id: int | None = None
    ):
        product = crud_product.get(self.db, product_id)
        if not product:
            raise ValueError("Ürün bulunamadı.")

        new_amount = (
            (product.stock_amount or 0)
            + quantity if movement_type == MovementType.GIRIS else
            (product.stock_amount or 0) - quantity
        )

        if new_amount < 0:
            raise ValueError(f"Stok eksiye düşemez: Ürün ID {product_id}")

        # Stok hareketi oluştur
        movement_data = StockMovementCreate(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            unit_price=unit_price,
            currency=currency,
            note=note,
            invoice_id=invoice_id,
            stock_after=new_amount
        )
        crud_stock_movement.create(self.db, movement_data)

        # Ürün stok miktarını güncelle
        product.stock_amount = new_amount
        self.db.commit()
        self.db.refresh(product)

        return product

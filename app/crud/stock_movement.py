from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import StockMovementCreate, StockMovementUpdate


class CRUDStockMovement(
    CRUDBase[StockMovement, StockMovementCreate, StockMovementUpdate]
):
    """
    Stok hareketleri için CRUD işlemleri.
    Temel CRUDBase metodlarını (create, get, update, remove) devralır.
    Ayrıca belirli bir referansa göre hareketleri listeleyebilir.
    """

    def get_by_reference(self, db: Session, reference_type: str, reference_id: int):
        """
        Belirli bir referans (örneğin Fatura, İade, Sipariş) ile ilişkili stok hareketlerini getirir.
        """
        result = (
            db.query(self.model)
            .filter(
                self.model.reference_type == reference_type,
                self.model.reference_id == reference_id
            )
            .all()
        )
        # IDE'yi tatmin etmek için tip cast (isteğe bağlı)
        # from typing import cast
        # return cast(list[StockMovement], cast(object, result))
        return result


# ✅ CRUD instance
stock_movement = CRUDStockMovement(StockMovement)

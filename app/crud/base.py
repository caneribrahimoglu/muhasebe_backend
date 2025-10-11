from typing import TypeVar, Generic, List, Any, Type
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import Base
from datetime import datetime, UTC

# ---------- Generic type tanımları ----------
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Tüm modeller için temel CRUD işlemlerini yöneten generic sınıf.
    Tüm CRUD sınıfları buradan miras alır.
    """
    model: Type[ModelType]  # <-- IDE için kritik type hint

    def __init__(self, model: Type[ModelType]) -> None:
        """Model sınıfını alır ve CRUDBase'e bağlar."""
        self.model = model

    # ---------- READ ----------
    def get(self, db: Session, obj_id: int) -> ModelType | None:
        """ID ile tek kayıt getirir."""
        return db.query(self.model).filter(self.model.id == obj_id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Tüm kayıtları sayfa bazlı getirir."""
        return db.query(self.model).offset(skip).limit(limit).all()

    # ---------- CREATE ----------
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Yeni kayıt oluşturur."""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ---------- UPDATE (PUT) ----------
    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType) -> ModelType:
        """Tam güncelleme (PUT)."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        # updated_at varsa otomatik güncelle
        if hasattr(db_obj, "updated_at"):
            setattr(db_obj, "updated_at", datetime.now(UTC))

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ---------- PARTIAL UPDATE (PATCH) ----------
    def update_partial(
        self,
        db: Session,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        """Parçalı güncelleme (PATCH)."""
        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_unset=True)

        if hasattr(db_obj, "updated_at"):
            update_data["updated_at"] = datetime.now(UTC)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ---------- DELETE ----------
    def remove(self, db: Session, obj_id: int) -> ModelType | None:
        """Kayıt siler."""
        obj = db.get(self.model, obj_id)  # SQLAlchemy 2.0 önerilen yöntemi
        if obj:
            db.delete(obj)
            db.commit()
        return obj

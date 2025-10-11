from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.product import Product
from app.models.product_compatibility import ProductCompatibility
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    def create(self, db: Session, obj_in: ProductCreate):
        """Ürünü ve ona bağlı uyumluluk listesini (compatibilities) birlikte oluşturur."""
        compatibilities_data = obj_in.compatibilities or []
        obj_data = obj_in.model_dump(exclude={"compatibilities"})
        db_obj = Product(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        for comp in compatibilities_data:
            db.add(ProductCompatibility(
                product_id=db_obj.id,
                brand=comp.brand,
                model_code=comp.model_code,
                search_text=f"{comp.brand} {comp.model_code}"
            ))

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, db_obj: Product, obj_in: ProductUpdate):
        """Ürün güncellemesi — eğer compatibilities varsa önce eskilerini siler, sonra yenilerini ekler."""
        data = obj_in.model_dump(exclude_unset=True)
        comps = data.pop("compatibilities", None)

        if comps is not None:
            db.query(ProductCompatibility).filter_by(product_id=db_obj.id).delete()
            for comp in comps:
                db.add(ProductCompatibility(
                    product_id=db_obj.id,
                    brand=comp.get("brand"),
                    model_code=comp.get("model_code"),
                    search_text=f"{comp.get('brand')} {comp.get('model_code')}"
                ))

        for field, value in data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_partial(self, db: Session, db_obj: Product, obj_in: ProductUpdate):
        """Uyumluluk dahil kısmi güncelleme."""
        data = obj_in.model_dump(exclude_unset=True)
        comps = data.pop("compatibilities", None)

        if comps is not None:
            db.query(ProductCompatibility).filter_by(product_id=db_obj.id).delete()
            for comp in comps or []:
                db.add(ProductCompatibility(
                    product_id=db_obj.id,
                    brand=comp.get("brand"),
                    model_code=comp.get("model_code"),
                    search_text=f"{comp.get('brand')} {comp.get('model_code')}"
                ))

        for field, value in data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj


product = CRUDProduct(Product)

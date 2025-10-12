from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.crud.product import product as crud  # ✅ buradaki 'crud' artık doğrudan CRUDProduct nesnesi
from app.models.product_compatibility import ProductCompatibility
from app.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])


# 🧩 Ürün oluşturma
@router.post("/", response_model=ProductRead)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    return crud.create(db, product_in)  # ✅ düzeltildi


# 📋 Tüm ürünleri listele
@router.get("/", response_model=list[ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    return crud.get_multi(db)  # ✅ düzeltildi


# 🔍 Tek ürün getir
@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get(db, product_id)  # ✅ düzeltildi
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return db_obj


# ✏️ Ürün güncelle (PUT)
@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    db_obj = crud.get(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return crud.update(db, db_obj, product_in)  # ✅ düzeltildi


# ❌ Ürün sil
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    crud.remove(db, obj_id=product_id)  # ✅ düzeltildi
    return {"ok": True}


# 🔎 Uyumluluk listesi içinde arama
@router.get("/search/", response_model=list[ProductRead])
def search_products(
    query: str = Query(..., description="Model veya marka adı ile arama yap"),
    db: Session = Depends(get_db)
):
    results = (
        db.query(crud.model)  # ✅ düzeltildi
        .join(ProductCompatibility)
        .filter(ProductCompatibility.search_text.ilike(f"%{query}%"))
        .all()
    )
    return results


# 🩹 Parçalı güncelleme (PATCH)
@router.patch("/{product_id}", response_model=ProductRead)
def partial_update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    db_obj = crud.get(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return crud.update_partial(db, db_obj, product_in)  # ✅ düzeltildi

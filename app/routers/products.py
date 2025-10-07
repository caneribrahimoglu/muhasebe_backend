from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.crud.product import crud_product
from app.models.product_compatibility import ProductCompatibility
from app.database import get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductRead)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create(db, product_in)


@router.get("/", response_model=list[ProductRead])
def get_all_products(db: Session = Depends(get_db)):
    return crud_product.get_multi(db)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_obj = crud_product.get(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return db_obj


@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    db_obj = crud_product.get(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    return crud_product.update(db, db_obj, product_in)


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_obj = crud_product.get(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")
    crud_product.remove(db, obj_id=product_id)
    return {"ok": True}


# 🔍 Arama fonksiyonu (uyumluluk listesi içinde model kodu ile)
@router.get("/search/", response_model=list[ProductRead])
def search_products(query: str = Query(..., description="Model veya marka adı ile arama yap"), db: Session = Depends(get_db)):
    results = (
        db.query(crud_product.model)
        .join(ProductCompatibility)
        .filter(ProductCompatibility.search_text.ilike(f"%{query}%"))
        .all()
    )
    return results

@router.patch("/{product_id}", response_model=ProductRead)
def partial_update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    db_obj = crud_product.get(db, product_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı")

    # Sadece gönderilen alanları güncelle
    updated_obj = crud_product.update(db, db_obj, product_in)
    return updated_obj


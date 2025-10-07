from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product_compatibility import (
    ProductCompatibilityCreate,
    ProductCompatibilityRead,
    ProductCompatibilityUpdate,
)
from app.crud.product_compatibility import crud_product_compatibility

router = APIRouter(prefix="/product-compatibility", tags=["Product Compatibility"])


@router.post("/", response_model=ProductCompatibilityRead)
def create_compatibility(item_in: ProductCompatibilityCreate, db: Session = Depends(get_db)):
    return crud_product_compatibility.create(db=db, obj_in=item_in)


@router.get("/", response_model=list[ProductCompatibilityRead])
def get_all_compatibilities(db: Session = Depends(get_db)):
    return crud_product_compatibility.get_multi(db=db)


@router.get("/{comp_id}", response_model=ProductCompatibilityRead)
def get_compatibility(comp_id: int, db: Session = Depends(get_db)):
    db_obj = crud_product_compatibility.get(db=db, obj_id=comp_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Uyumluluk kaydı bulunamadı")
    return db_obj


@router.patch("/{comp_id}", response_model=ProductCompatibilityRead)
def patch_compatibility(comp_id: int, item_in: ProductCompatibilityUpdate, db: Session = Depends(get_db)):
    db_obj = crud_product_compatibility.get(db=db, obj_id=comp_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Uyumluluk kaydı bulunamadı")
    return crud_product_compatibility.update_partial(db=db, db_obj=db_obj, obj_in=item_in)


@router.delete("/{comp_id}")
def delete_compatibility(comp_id: int, db: Session = Depends(get_db)):
    db_obj = crud_product_compatibility.remove(db=db, obj_id=comp_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Uyumluluk kaydı bulunamadı veya silinmiş")
    return {"ok": True}

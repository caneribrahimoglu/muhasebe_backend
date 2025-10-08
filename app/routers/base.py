from typing import Type, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.database import get_db

def generate_router(
    name: str,
    crud,
    schema: Type,
    create_schema: Type,
    update_schema: Type,
    prefix: str,
    tags: List[str]
) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)

    # CREATE
    @router.post(
        "/",
        response_model=schema,
        summary=f"Yeni {name.capitalize()} oluştur",
        operation_id=f"create_{name}"
    )
    def create_item(item_in: create_schema = Body(...), db: Session = Depends(get_db)):
        return crud.create(db=db, obj_in=item_in)

    # READ ALL
    @router.get(
        "/",
        response_model=List[schema],
        summary=f"Tüm {name.capitalize()} kayıtlarını getir",
        operation_id=f"get_all_{name}s"
    )
    def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return crud.get_multi(db=db, skip=skip, limit=limit)

    # READ SINGLE
    @router.get(
        "/{item_id}",
        response_model=schema,
        summary=f"{name.capitalize()} detayını getir",
        operation_id=f"get_{name}_by_id"
    )
    def read_item(item_id: int, db: Session = Depends(get_db)):
        db_item = crud.get(db=db, obj_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{name.capitalize()} bulunamadı")
        return db_item

    # FULL UPDATE (PUT)
    @router.put(
        "/{item_id}",
        response_model=schema,
        summary=f"{name.capitalize()} kaydını tamamen güncelle",
        operation_id=f"update_{name}_full"
    )
    def update_item(
        item_id: int,
        item_in: update_schema = Body(...),
        db: Session = Depends(get_db)
    ):
        db_item = crud.get(db=db, obj_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{name.capitalize()} bulunamadı")
        return crud.update(db=db, db_obj=db_item, obj_in=item_in)

    # PARTIAL UPDATE (PATCH)
    @router.patch(
        "/{item_id}",
        response_model=schema,
        summary=f"{name.capitalize()} kaydını kısmen güncelle",
        operation_id=f"patch_{name}_partial"
    )
    def patch_item(
        item_id: int,
        item_in: update_schema = Body(...),
        db: Session = Depends(get_db)
    ):
        db_item = crud.get(db=db, obj_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{name.capitalize()} bulunamadı")
        # Kısmi güncelleme için dict’te sadece gönderilen alanları dikkate al
        update_data = item_in.model_dump(exclude_unset=True)
        return crud.update(db=db, db_obj=db_item, obj_in=update_data)

    # DELETE
    @router.delete(
        "/{item_id}",
        summary=f"{name.capitalize()} kaydını sil",
        operation_id=f"delete_{name}"
    )
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        db_item = crud.get(db=db, obj_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{name.capitalize()} bulunamadı")
        crud.remove(db=db, obj_id=item_id)
        return {"message": f"{name.capitalize()} başarıyla silindi."}

    return router

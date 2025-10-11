from typing import Type, List, Callable, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db


def generate_service_router(
    *,
    name: str,
    service_create_func: Callable,
    service_get_func: Callable,
    response_schema: Type,
    create_schema: Type,
    prefix: str,
    tags: List[str],
    service_get_by_id_func: Optional[Callable] = None,
    service_update_func: Optional[Callable] = None,
    service_delete_func: Optional[Callable] = None
) -> APIRouter:
    """
    Service katmanını kullanan dinamik router oluşturucu.
    CRUD router'ın aksine, burada tüm işlemler doğrudan service fonksiyonlarına delege edilir.
    Böylece iş mantıkları (örneğin bakiye güncellemesi, doğrulama, zincirleme işlemler)
    otomatik olarak devreye girer.
    """

    router = APIRouter(prefix=prefix, tags=tags)

    # CREATE
    @router.post("/", response_model=response_schema)
    def create_item(item_in: create_schema, db: Session = Depends(get_db)):
        return service_create_func(db=db, transaction_in=item_in)

    # LIST
    @router.get("/", response_model=List[response_schema])
    def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return service_get_func(db=db, skip=skip, limit=limit)

    # GET BY ID (isteğe bağlı)
    if service_get_by_id_func:
        @router.get("/{item_id}", response_model=response_schema)
        def get_item(item_id: int, db: Session = Depends(get_db)):
            obj = service_get_by_id_func(db=db, obj_id=item_id)
            if not obj:
                raise HTTPException(status_code=404, detail=f"{name} bulunamadı.")
            return obj

    # UPDATE (isteğe bağlı)
    if service_update_func:
        @router.patch("/{item_id}", response_model=response_schema)
        def update_item(item_id: int, item_in: create_schema, db: Session = Depends(get_db)):
            return service_update_func(db=db, obj_id=item_id, obj_in=item_in)

    # DELETE (isteğe bağlı)
    if service_delete_func:
        @router.delete("/{item_id}")
        def delete_item(item_id: int, db: Session = Depends(get_db)):
            service_delete_func(db=db, obj_id=item_id)
            return {"message": f"{name} başarıyla silindi."}

    return router

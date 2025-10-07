from typing import Type, List, Any
from fastapi import APIRouter, Depends, HTTPException, status
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
    """
    Generic CRUD router generator.
    CRUDBase ile tanımlanan işlemleri otomatik olarak FastAPI endpoint'lerine dönüştürür.
    """
    router = APIRouter(prefix=prefix, tags=tags)

    # ---------- CREATE ----------
    @router.post("/", response_model=schema, status_code=status.HTTP_201_CREATED)
    def create_item(item_in: Any, db: Session = Depends(get_db)):
        """
        Yeni kayıt oluşturur.
        """
        db_obj = crud.create(db=db, obj_in=item_in)
        return db_obj

    # ---------- READ (GET ALL) ----------
    @router.get("/", response_model=List[schema])
    def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        """
        Tüm kayıtları getirir (sayfalama destekli).
        """
        return crud.get_multi(db=db, skip=skip, limit=limit)

    # ---------- READ (GET ONE) ----------
    @router.get("/{item_id}", response_model=schema)
    def read_item(item_id: int, db: Session = Depends(get_db)):
        """
        ID’ye göre tek kayıt getirir.
        """
        db_obj = crud.get(db=db, obj_id=item_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        return db_obj

    # ---------- UPDATE (PUT) ----------
    @router.put("/{item_id}", response_model=schema)
    def update_item(item_id: int, item_in: Any, db: Session = Depends(get_db)):
        """
        Tam güncelleme (PUT).
        """
        db_obj = crud.get(db=db, obj_id=item_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        return crud.update(db=db, db_obj=db_obj, obj_in=item_in)

    # ---------- PARTIAL UPDATE (PATCH) ----------
    @router.patch("/{item_id}", response_model=schema)
    def partial_update_item(item_id: int, item_in: Any, db: Session = Depends(get_db)):
        """
        Parçalı güncelleme (PATCH).
        Sadece gönderilen alanları günceller.
        """
        db_obj = crud.get(db=db, obj_id=item_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        return crud.update_partial(db=db, db_obj=db_obj, obj_in=item_in)

    # ---------- DELETE ----------
    @router.delete("/{item_id}", response_model=schema)
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        """
        ID’ye göre kayıt siler.
        """
        db_obj = crud.remove(db=db, obj_id=item_id)
        if not db_obj:
            raise HTTPException(status_code=404, detail=f"{name} not found or already deleted")
        return db_obj

    return router

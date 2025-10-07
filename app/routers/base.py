from typing import Type, List
from fastapi import APIRouter, Depends, HTTPException
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

    @router.post("/", response_model=schema)
    def create_item(item_in: create_schema, db: Session = Depends(get_db)):
        return crud.create(db=db, obj_in=item_in)

    @router.get("/", response_model=List[schema])
    def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return crud.get_multi(db=db, skip=skip, limit=limit)

    @router.get("/{item_id}", response_model=schema)
    def read_item(item_id: int, db: Session = Depends(get_db)):
        db_item = crud.get(db=db, obj_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        return db_item

    @router.put("/{item_id}", response_model=schema)
    def update_item(item_id: int, item_in: update_schema, db: Session = Depends(get_db)):
        db_item = crud.get(db=db, obj_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        return crud.update(db=db, db_obj=db_item, obj_in=item_in)

    @router.delete("/{item_id}")
    def delete_item(item_id: int, db: Session = Depends(get_db)):
        db_item = crud.get(db=db, obj_id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail=f"{name} not found")
        crud.remove(db=db, obj_id=item_id)
        return {"ok": True}

    return router

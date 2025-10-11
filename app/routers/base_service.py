from typing import Type, List, Callable
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
    tags: List[str]
) -> APIRouter:
    """
    Service katmanını kullanan dinamik router oluşturucu.
    CRUD router'ın aksine, burada create() fonksiyonu doğrudan service katmanından çağrılır.
    Böylece iş mantıkları (örneğin bakiye güncellemesi) otomatik devreye girer.
    """

    router = APIRouter(prefix=prefix, tags=tags)

    @router.post("/", response_model=response_schema)
    def create_item(item_in: create_schema, db: Session = Depends(get_db)):
        """
        Service katmanındaki create fonksiyonunu çağırır.
        İş mantığı burada değil, service içinde yürür.
        """
        return service_create_func(db=db, transaction_in=item_in)

    @router.get("/", response_model=List[response_schema])
    def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        """
        Service katmanındaki get fonksiyonunu çağırır.
        """
        return service_get_func(db=db, skip=skip, limit=limit)

    return router

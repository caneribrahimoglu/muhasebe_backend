from app.crud.base import CRUDBase
from app import models, schemas

customer_address = CRUDBase(models.CustomerAddress)

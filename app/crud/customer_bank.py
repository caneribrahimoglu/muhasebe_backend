from app.crud.base import CRUDBase
from app import models, schemas

customer_bank = CRUDBase(models.CustomerBank)

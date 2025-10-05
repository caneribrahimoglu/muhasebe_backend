from fastapi import FastAPI
from app.routers import customers
from app.database import engine
from app.models import customer as models

app = FastAPI(title="Muhasebe Backend")

models.Base.metadata.create_all(bind=engine)

app.include_router(customers.router)

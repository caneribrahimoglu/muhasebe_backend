from fastapi import FastAPI
from routers import customer
from database import engine
import models
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(customer.router)
from fastapi import FastAPI
from pydantic import BaseModel
from routers import customer
from database import engine, Base
import models
app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(customer.router)
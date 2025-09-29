from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Customer(BaseModel):
    id: int
    name: str
    surname: str
    email: str

customers = []

@app.get("/")
def root():
    return {"message": "Merhaba Muhasebe!"}



@app.post("/customer/")
def customer_add(customer: Customer):
    customers.append(customer)
    return {"message":"Müşteri eklendi", "customer": customer}

@app.get("/customer/")
def customer_list():
    return  customers






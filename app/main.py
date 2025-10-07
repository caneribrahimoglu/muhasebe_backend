from fastapi import FastAPI
from app.routers import customer, customer_address, customer_bank, products, product_compatibility
from app.database import Base, engine

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

# FastAPI uygulaması
app = FastAPI(
    title="Muhasebe Backend",
    version="1.0.0",
    description="Caner İbrahimoglu tarafından geliştirilen yapay zekâ destekli muhasebe backend API'si."
)

# Router'ları ekle
app.include_router(customer.router)
app.include_router(customer_address.router)
app.include_router(customer_bank.router)
app.include_router(products.router)
app.include_router(product_compatibility.router)


# Basit test endpoint’i
@app.get("/")
def root():
    return {"message": "Muhasebe Backend API aktif 🚀"}

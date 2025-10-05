from sqlalchemy import Column, Integer, String
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

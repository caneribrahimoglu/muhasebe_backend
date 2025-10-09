# app/services/customer_service.py
from app.services.service_base import ServiceBase
from app.crud.customer import crud_customer

class CustomerService(ServiceBase):
    """
    Cari hesap servis katmanı.
    Cari borç ve alacak işlemleri burada yönetilir.
    """

    def add_debt(self, customer_id: int, amount: float):
        customer = crud_customer.get(self.db, customer_id)
        if not customer:
            raise ValueError("Cari bulunamadı.")
        # Henüz net bir borç alanı yok, örnek olarak deposit_amount kullanalım:
        if hasattr(customer, "deposit_amount"):
            customer.deposit_amount -= amount
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def add_credit(self, customer_id: int, amount: float):
        customer = crud_customer.get(self.db, customer_id)
        if not customer:
            raise ValueError("Cari bulunamadı.")
        if hasattr(customer, "deposit_amount"):
            customer.deposit_amount += amount
        self.db.commit()
        self.db.refresh(customer)
        return customer

from app.models.customer import Customer
from app.services.service_base import ServiceBase
from app.crud.customer import crud_customer
from app.models.customer_transaction import TransactionDirection, TransactionReference
from app.crud.customer_transaction import crud_customer_transaction
from app.schemas.customer_transaction import CustomerTransactionCreate

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

    def record_transaction(self, customer_id: int, amount: float, direction: TransactionDirection, description: str,
                           reference_type: TransactionReference, reference_id: int | None = None):
        print(f"🧾 record_transaction() çağrıldı: {description} — {amount}₺ yön={direction.value}")

        # Mevcut bakiyeyi çek
        customer = self.db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError("Cari bulunamadı.")

        # Yeni bakiye
        new_balance = (customer.deposit_amount or 0)
        if direction == TransactionDirection.BORC:
            new_balance -= amount
        else:
            new_balance += amount

        # Kayıt oluştur
        tx = CustomerTransactionCreate(
            customer_id=customer_id,
            amount=amount,
            direction=direction,
            description=description,
            reference_type=reference_type,
            reference_id=reference_id,
            balance_after=new_balance
        )

        crud_customer_transaction.create(self.db, tx)
        print("✅ Cari hareket kaydı oluşturuldu.")

        # Müşteri bakiyesini güncelle
        customer.deposit_amount = new_balance
        self.db.commit()
        self.db.refresh(customer)
        return customer

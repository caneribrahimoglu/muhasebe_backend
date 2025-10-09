from app.services.service_base import ServiceBase
from app.models.customer_transaction import TransactionDirection, TransactionReference
from app.services.customer_service import CustomerService
from app.schemas.payment import PaymentCreate
from app.crud.payment import crud_payment


class PaymentService(ServiceBase):
    """
    Tahsilat ve ödeme işlemlerini yönetir.
    Örnek: Müşteriden tahsilat yapmak, tedarikçiye ödeme yapmak.
    """

    def create_payment(self, obj_in: PaymentCreate):
        # 🔒 Cari zorunlu kontrol
        if not obj_in.customer_id:
            raise ValueError("Cari seçilmeden tahsilat/ödeme oluşturulamaz.")

        # 1️⃣ Ödeme kaydını oluştur
        payment = crud_payment.create(self.db, obj_in)
        self.db.refresh(payment)  # ID'nin garanti gelmesi için

        print(f"💰 PaymentService: {obj_in.payment_type} işlemi için cari hareket başlatılıyor...")

        # 2️⃣ Cari hareketini oluştur
        customer_service = CustomerService(self.db)

        # Tahsilat = ALACAK, Ödeme = BORC
        direction = (
            TransactionDirection.ALACAK
            if obj_in.payment_type == "TAHSILAT"
            else TransactionDirection.BORC
        )

        description = (
            f"{obj_in.method.value.title()} ile tahsilat #{payment.id}"
            if obj_in.payment_type == "TAHSILAT"
            else f"{obj_in.method.value.title()} ile ödeme #{payment.id}"
        )

        customer_service.record_transaction(
            customer_id=obj_in.customer_id,
            amount=obj_in.amount,
            direction=direction,
            description=description,
            reference_type=TransactionReference.ODEME,
            reference_id=payment.id
        )

        return payment

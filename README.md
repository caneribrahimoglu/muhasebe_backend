# 💼 Muhasebe Backend

**Muhasebe Backend**, FastAPI, SQLAlchemy ve Pydantic kullanılarak geliştirilen, modüler, ölçeklenebilir ve ilişkisel bir **muhasebe yönetim sistemi API** projesidir.  
Proje; müşteri, adres ve banka bilgilerini ilişkisel olarak yöneten bir altyapı üzerine kurulmuştur.

---

## 🚀 Özellikler

- ⚙️ **Generic CRUD altyapısı**
  - `app/crud/base.py` üzerinden her model için ortak CRUD işlemleri.
- 🧩 **İlişkisel müşteri yönetimi**
  - Müşteriler (`Customer`) ile bağlı adres (`CustomerAddress`) ve banka (`CustomerBank`) kayıtları tek endpoint üzerinden yönetilir.
- 🔁 **Kısmi güncelleme desteği**
  - `PUT /customers/{id}` çağrısı:
    - `id` varsa → günceller  
    - `id` yoksa → yeni kayıt oluşturur  
    - JSON’da olmayan `id` → ilgili kayıtları siler
- 🧱 **Soyutlanmış router sistemi**
  - `app/routers/base.py` üzerinden tüm CRUD endpoint’leri dinamik olarak üretilir.
- 🧰 **Pydantic + SQLAlchemy uyumu**
  - `model_config = {"from_attributes": True}` ile hızlı dönüşüm.
- 🗃️ **SQLite veritabanı (PostgreSQL uyumlu yapı)**

---

## 🗂️ Proje Yapısı

```
app/
├── crud/
│   ├── __init__.py
│   ├── base.py                # Generic CRUDBase sınıfı
│   ├── customer.py            # Customer CRUD (ilişkisel yapıyla)
│   ├── customer_address.py    # Adres CRUD
│   └── customer_bank.py       # Banka CRUD
│
├── models/
│   ├── __init__.py
│   ├── customer.py            # Customer SQLAlchemy modeli
│   ├── customer_address.py    # CustomerAddress SQLAlchemy modeli
│   └── customer_bank.py       # CustomerBank SQLAlchemy modeli
│
├── routers/
│   ├── __init__.py
│   ├── base.py                # Dinamik CRUD router oluşturucu
│   ├── customer.py            # Customer endpoint’leri
│   ├── customer_address.py
│   └── customer_bank.py
│
├── schemas/
│   ├── __init__.py
│   ├── customer.py            # Pydantic modeller (CustomerBase, Create, Update, Read)
│   ├── customer_address.py    # Adres modelleri
│   └── customer_bank.py       # Banka modelleri
│
├── database.py                # SQLAlchemy bağlantısı ve session ayarları
├── main.py                    # FastAPI giriş noktası
└── __init__.py
```

---

## ⚡ Kurulum

### 1️⃣ Sanal ortam oluştur
```bash
python -m venv .venv
```

### 2️⃣ Ortamı etkinleştir
Windows:
```bash
.venv\Scripts\activate
```
Linux/Mac:
```bash
source .venv/bin/activate
```

### 3️⃣ Gerekli bağımlılıkları yükle
```bash
pip install -r requirements.txt
```

### 4️⃣ Sunucuyu başlat
```bash
uvicorn app.main:app --reload
```

### 5️⃣ Swagger arayüzü
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Örnek JSON (Customer Create)

```json
{
  "code": "MUST-001",
  "type": "ALICI",
  "institution_type": "KURUM",
  "title": "OpenAI Teknoloji A.Ş.",
  "name": "OpenAI",
  "tax_number": "1234567890",
  "addresses": [
    {
      "address_name": "Merkez Ofis",
      "city": "İstanbul",
      "district": "Levent",
      "address": "Büyükdere Cad. No:100"
    }
  ],
  "banks": [
    {
      "bank_name": "Ziraat Bankası",
      "iban": "TR000000000000000000001111"
    }
  ]
}
```

---

## 🔄 Örnek JSON (Customer Update / Partial Update)

```json
{
  "addresses": [
    {
      "id": 1,
      "address_name": "Merkez Ofis (Güncellendi)",
      "city": "İstanbul",
      "district": "Maslak",
      "address": "Maslak Mah. No:5"
    },
    {
      "address_name": "Yeni Şube",
      "city": "Ankara",
      "district": "Çankaya",
      "address": "Atatürk Bulvarı No:25"
    }
  ],
  "banks": [
    {
      "id": 1,
      "bank_name": "VakıfBank",
      "iban": "TR000000000000000000002222"
    }
  ]
}
```

---

## 🧭 Geliştirici Notları

- Kodlama standardı: **PEP8**
- ORM: **SQLAlchemy**
- Validation: **Pydantic**
- Framework: **FastAPI**
- Test arayüzü: **Swagger UI** (`/docs`)

---

## 📈 Gelecek Planı

- [ ] Ürün (Product) modülü
- [ ] Stok & depo yönetimi
- [ ] Fatura & satış işlemleri
- [ ] Kullanıcı yetkilendirme (Auth)
- [ ] AI destekli fatura/fiş okuma (LLM entegrasyonu)

---

## 👨‍💻 Geliştirici

**Caner İbrahimoglu**  
📦 [GitHub: caneribrahimoglu](https://github.com/caneribrahimoglu)

---

## 🧠 Lisans

MIT License © 2025  
Bu proje özgürce kullanılabilir, geliştirilebilir ve dağıtılabilir.

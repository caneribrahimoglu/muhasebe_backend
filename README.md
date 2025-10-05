# 📘 Muhasebe Backend (FastAPI)

Bu proje, **modüler**, **ölçeklenebilir** ve **bakımı kolay** bir FastAPI tabanlı backend uygulamasıdır.  
Hedef: ERP/Muhasebe sistemine temel oluşturacak, müşteri, ürün, fatura vb. modülleri API olarak yönetmek.

---

## 🚀 Özellikler

- ✅ **FastAPI** tabanlı modern backend yapısı  
- ✅ **SQLAlchemy ORM** ile veritabanı yönetimi  
- ✅ **Pydantic v2** ile tip güvenliği ve veri doğrulama  
- ✅ **Soyut CRUD mimarisi (Generic CRUD Base)**  
- ✅ Katmanlı dosya yapısı:
  - `models` → Veritabanı tabloları  
  - `schemas` → Veri şemaları (request/response modelleri)  
  - `crud` → CRUD işlemleri (soyutlama + spesifik işlemler)  
  - `routers` → API endpoint’leri  
  - `database.py` → Veritabanı bağlantısı  
  - `main.py` → Uygulama başlatma noktası

---

## 🧩 Dosya Yapısı

```bash
muhasebe_backend/
│
├── app/
│   ├── crud/
│   │   ├── base.py              # Generic CRUD soyutlaması
│   │   └── _old_customers.py         # Customer’a özel CRUD işlemleri
│   │
│   ├── models/
│   │   └── customer.py          # SQLAlchemy model (Customer)
│   │
│   ├── schemas/
│   │   └── customer.py          # Pydantic şemaları (CustomerCreate, Update, vb.)
│   │
│   ├── routers/
│   │   └── _old_customers.py         # Customer endpoint’leri (GET, POST, PUT, DELETE)
│   │
│   ├── database.py              # DB engine, session ve Base tanımı
│   └── main.py                  # Uygulama girişi (FastAPI instance)
│
├── muhasebe.db                  # SQLite veritabanı (lokal)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Kurulum

### 1️⃣ Sanal ortam oluştur ve aktif et

```bash
python -m venv .venv
source .venv/bin/activate   # (Linux/Mac)
.venv\Scripts\activate      # (Windows)
```

### 2️⃣ Gerekli paketleri yükle

```bash
pip install -r requirements.txt
```

### 3️⃣ Sunucuyu başlat

```bash
uvicorn app.main:app --reload
```

### 4️⃣ Swagger arayüzü üzerinden test et

🔗 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧠 Örnek Endpoint’ler

### 🔹 Tüm müşterileri getir
`GET /customers/`

### 🔹 Tek müşteriyi getir
`GET /customers/{customer_id}`

### 🔹 Yeni müşteri oluştur
`POST /customers/`

```json
{
  "name": "Caner İbrahim",
  "email": "caner@example.com"
}
```

### 🔹 Müşteri bilgilerini güncelle
`PUT /customers/{customer_id}`

```json
{
  "name": "Caner İ. Güncellendi"
}
```

### 🔹 Müşteri sil
`DELETE /customers/{customer_id}`

---

## 🧱 Yapısal Mantık

- `base.py` içerisindeki **CRUDBase** sınıfı,  
  diğer tüm modeller için tekrar kullanılabilir CRUD işlevleri sağlar.  
- Yeni bir tablo ekleneceğinde yalnızca:
  1. `models/` altına yeni model eklenir  
  2. `schemas/` altına karşılık gelen şemalar yazılır  
  3. `crud/` altında `new_model_crud = CRUDBase(Model, SchemaCreate, SchemaUpdate)` yapılır  
  4. `routers/` altına yeni router eklenir  
  5. `main.py` içine `app.include_router(...)` eklenir  

Hepsi bu kadar.

---

## 🗺️ Yol Haritası

| Adım | Özellik | Açıklama |
|------|----------|-----------|
| ✅ 1 | Müşteri CRUD | Temel CRUD tamamlandı |
| 🔜 2 | Ürün (Product) CRUD | Aynı mimariyle yeni modül |
| 🔜 3 | PostgreSQL geçişi | SQLite → PostgreSQL |
| 🔜 4 | Kullanıcı Auth sistemi | JWT tabanlı giriş/çıkış |
| 🔜 5 | Fatura Modülü | Müşteri ve ürünlerle ilişkili yapı |
| 🔜 6 | Frontend (React) entegrasyonu | Yönetim paneli |

---

## 👨‍💻 Geliştirici Notları

- Kod yapısı **modülerdir**: her modül bağımsız olarak genişletilebilir.  
- CRUD soyutlaması sayesinde, yeni tablo eklemek **5 dakikalık iştir.**  
- Proje; FastAPI + SQLAlchemy + Pydantic v2 mimarisinin **temiz, endüstri standardı** örneğidir.

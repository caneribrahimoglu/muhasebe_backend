# 📊 Muhasebe Backend

Bu proje, modern muhasebe uygulamaları için geliştirilmiş **FastAPI tabanlı bir backend servisidir**.  
Amaç, ölçeklenebilir, hızlı ve güvenilir bir altyapı üzerinde müşteri, fatura ve diğer muhasebe operasyonlarını yönetmektir.  

---

## 🚀 Teknolojiler
- **[FastAPI](https://fastapi.tiangolo.com/)** → API geliştirme
- **[SQLAlchemy](https://www.sqlalchemy.org/)** → ORM ve veritabanı yönetimi
- **[Pydantic](https://docs.pydantic.dev/)** → Veri doğrulama ve şemalar
- **[SQLite](https://www.sqlite.org/)** → Varsayılan veritabanı (geliştirme ortamı)
- **[Uvicorn](https://www.uvicorn.org/)** → ASGI server

---

## ⚙️ Kurulum

### 1. Depoyu Klonla
```bash
git clone https://github.com/caneribrahimoglu/muhasebe_backend.git
cd muhasebe_backend
```

### 2. Sanal Ortam Oluştur ve Aktifleştir
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Gereksinimleri Kur
```bash
pip install -r requirements.txt
```

---

## ▶️ Çalıştırma

Uygulamayı başlatmak için:
```bash
uvicorn main:app --reload
```

Çalışır hale geldiğinde:
- Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📂 Proje Yapısı
```
muhasebe_backend/
│
├── routers/          # API endpoint dosyaları
│   └── customer.py   # Örnek müşteri endpointleri
│
├── models.py         # SQLAlchemy modelleri
├── schemas.py        # Pydantic şemaları
├── crud.py           # CRUD fonksiyonları
├── database.py       # Veritabanı bağlantısı
├── main.py           # Uygulamanın giriş noktası
├── requirements.txt  # Gerekli kütüphaneler
└── README.md         # Proje dokümantasyonu
```

---

## ✅ Mevcut Özellikler
- Müşteri ekleme (POST /customer)
- Müşteri listeleme (GET /customer)
- Otomatik şema validasyonu
- SQLite ile hızlı prototipleme

---

## 🛠️ Yol Haritası
- [ ] Müşteri güncelleme ve silme endpointleri  
- [ ] Fatura ve ödeme modülü  
- [ ] PostgreSQL entegrasyonu (production için)  
- [ ] JWT Authentication  

---

## 👨‍💻 Katkı
Pull request’ler kabul edilir. Büyük değişiklikler için önce bir konu açarak tartışınız.  

---

## 📌 Yazar
**Hüseyin Caner İBRAHİMOĞLU**  
📎 [GitHub Profilim](https://github.com/caneribrahimoglu)

# 🧾 Muhasebe Backend (FastAPI ERP Çekirdeği)

Bu proje; **FastAPI**, **SQLAlchemy** ve **Pydantic 2.0** altyapısı ile geliştirilmiş  
bir **mini muhasebe ve stok yönetim sistemi**dir.  
Fatura, stok, cari hesap ve tahsilat modüllerini entegre biçimde yönetir.

---

## 🚀 Özellikler

### 👥 Cari Yönetimi (`/customers`)
- Müşteri ve tedarikçi kayıtlarını **tek tablo** üzerinden yönetir.
- `CustomerType`: `ALICI` / `SATICI`
- `InstitutionType`: `KURUM` / `SAHIS`
- Finansal bilgiler: döviz, iskonto, kredi limiti, vade, cari kodu vb.

### 📦 Ürün Yönetimi (`/products`)
- Ürün, kategori, stok ve fiyat bilgileri.
- `ProductCompatibility` ile model uyumluluk listeleri.
- Ürün arama: `/products/search/?query=...`

### 🧾 Fatura Yönetimi (`/invoices`)
- Satış, alış ve iade faturaları.
- Fatura satırlarında ürün, miktar, fiyat, KDV oranı.
- **Otomatik toplam / vergi hesaplama.**
- **Eksi stok kontrolü:** stok yetersizse hata döner.
- **Stok entegrasyonu:** satışta stok düşer, alışta artar.
- Fatura kesildiğinde cari borç eklenir (`balance`).

### 💰 Tahsilat / Ödeme Yönetimi (`/payments`)
- Faturalara bağlı tahsilat (TAHSILAT) veya ödeme (ODEME) kaydı.
- `PaymentMethod`: `NAKIT`, `HAVALE`, `KREDI_KARTI`, `CEK`
- Tahsilat sonrası fatura bakiyesi otomatik azalır.

### 🔄 Stok Hareketleri (`/stock-movements`)
- Her fatura satırı için otomatik hareket kaydı.
- `MovementType`: `GIRIS` / `CIKIS`
- Hangi faturadan, kimden ve ne kadar değişim olduğunu tutar.

### 📊 Raporlama (`/reports`)
- `/reports/stock-summary` → ürün bazında giriş/çıkış ve mevcut stok özeti.
- `/reports/customer-balance` → müşteri bazında toplam borç, alacak, bakiye ve durum.

---

## ⚙️ Sistem Davranışı

| İşlem | Otomatik Etki |
|-------|----------------|
| Satış faturası oluşturuldu | Stok azalır, cari borç eklenir |
| Alış faturası oluşturuldu | Stok artar, cari alacak eklenir |
| İade faturası oluşturuldu | Ters yönlü stok ve bakiye işlemi yapılır |
| Tahsilat kaydedildi | Fatura bakiyesi düşer |
| Ödeme kaydedildi | Satıcılara olan borç düşer |
| Rapor çağrıldı | Canlı veriyle güncel özet döner |

---

## 🧩 Veri Modeli (özet)

```
Customer
│
├── Invoice
│     ├── InvoiceItem
│     │       └── Product
│     │
│     └── Payment
│
└── StockMovement (otomatik log)
        └── Product
```

---

## 🧱 Teknolojiler

| Bileşen | Açıklama |
|----------|-----------|
| **FastAPI** | REST API çatısı |
| **SQLAlchemy** | ORM & veritabanı yönetimi |
| **Pydantic v2** | Veri şemaları ve doğrulama |
| **SQLite** | Veritabanı (geliştirme ortamı) |
| **Uvicorn** | ASGI server |

---

## ⚙️ Kurulum

### 1️⃣ Ortamı oluştur
```bash
python -m venv venv
venv\Scripts\activate  # (Windows)
source venv/bin/activate  # (Linux / Mac)
```

### 2️⃣ Gereksinimleri yükle
```bash
pip install -r requirements.txt
```

### 3️⃣ Sunucuyu çalıştır
```bash
uvicorn app.main:app --reload
```

### 4️⃣ API Arayüzü
Tarayıcıda aç:
👉 http://127.0.0.1:8000/docs

---

## 📊 Mevcut Modüller

| Modül | Dosya |
|--------|--------|
| Müşteri Yönetimi | `app/models/customer.py` |
| Ürün Yönetimi | `app/models/product.py` |
| Uyumluluk | `app/models/product_compatibility.py` |
| Fatura | `app/models/invoice.py`, `app/models/invoice_item.py` |
| Tahsilat/Ödeme | `app/models/payment.py` |
| Stok Hareketleri | `app/models/stock_movement.py` |
| Raporlama | `app/routers/reports.py` |

---

## ✅ Şu Anda Sistem Şunları Yapabiliyor

| İşlev | Durum |
|--------|--------|
| Cari hesap ekleme / listeleme | ✅ |
| Ürün ekleme / güncelleme / arama | ✅ |
| Fatura oluşturma (alış, satış, iade) | ✅ |
| Otomatik stok güncelleme | ✅ |
| Eksi stok koruması | ✅ |
| Stok hareket logu | ✅ |
| Tahsilat ve ödeme yönetimi | ✅ |
| Cari bakiye hesaplama | ✅ |
| Stok özet raporu | ✅ |
| Swagger arayüzü (test ortamı) | ✅ |

---

## 💡 Gelecek Planı

- 🏦 Kasa / Banka modülü  
- 🧾 Fatura yazdırma (PDF)  
- 📅 Vade & hatırlatma sistemi  
- 🏬 Çoklu depo yönetimi  
- 📈 Kâr–Zarar raporları  
- 📤 Excel / PDF dışa aktarma  
- 🤖 AI destekli sorgu (LLM)  
- 🌐 Trendyol / N11 API entegrasyonu  

---

## 👨‍💻 Geliştirici Notu

Bu sistem, üretim için değil **öğrenme ve geliştirme** amaçlı bir temel iskelet projesidir.  
Kod yapısı modülerdir; `CRUDBase` sınıfı sayesinde yeni modeller kolayca eklenebilir.

> 🚀 “Fatura kes, stok düşsün, cari borçlansın, tahsilat yap bakiyeyi düşür,  
ve tüm hareketleri raporla.”  
Hepsi entegre şekilde çalışır.

---

## 🧩 Lisans
MIT License  
© 2025 Muhasebe Backend

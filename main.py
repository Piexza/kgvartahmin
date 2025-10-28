# ⚽ KG Tahmin Modeli

SportMonks API kullanarak futbol maçları için **Karşılıklı Gol (KG / BTTS - Both Teams To Score)** tahmin modeli.

Makine öğrenimi ile geçmiş maç verilerini analiz ederek gelecek maçların KG olma olasılığını hesaplar.

## 🎯 Özellikler

- ✅ SportMonks API entegrasyonu
- ✅ Geçmiş maç verilerinden öğrenme
- ✅ Takım istatistikleri analizi (ev/deplasman performansı)
- ✅ Makine öğrenimi modeli (Random Forest)
- ✅ Gelecek maçlar için KG olasılığı tahmini
- ✅ Kullanımı kolay komut satırı arayüzü

## 📋 Gereksinimler

- Python 3.8+
- SportMonks API üyeliği ve API anahtarı

## 🚀 Kurulum

1. **Repository'yi klonlayın:**
```bash
git clone https://github.com/Piexza/kgvartahmin.git
cd kgvartahmin
```

2. **Gerekli paketleri yükleyin:**
```bash
pip install -r requirements.txt
```

3. **API anahtarınızı ayarlayın:**

`.env` dosyası oluşturun:
```bash
cp .env.example .env
```

`.env` dosyasını düzenleyerek SportMonks API anahtarınızı ekleyin:
```
SPORTMONKS_API_KEY=your_api_key_here
```

## 💻 Kullanım

Programı başlatın:
```bash
python main.py
```

### Menü Seçenekleri:

1. **Modeli Eğit**: Geçmiş maç verileriyle modeli eğitin
2. **Gelecek Maçlar için Tahmin Yap**: Gelecek maçların KG olasılığını hesaplayın
3. **Modeli Kaydet**: Eğitilmiş modeli kaydedin
4. **Modeli Yükle**: Kaydedilmiş modeli yükleyin
5. **Çıkış**: Programdan çıkın

## 📊 Örnek Kullanım

### 1. Model Eğitimi
```
Lig ID: 271 (Süper Lig - Türkiye)
Sezon ID: 23032 (2024-2025 sezonu)
```

### 2. Tahmin Yapma
Model eğitildikten sonra gelecek maçlar için tahmin yapabilirsiniz:

```
⚽ Galatasaray vs Fenerbahçe
   📅 Tarih: 2025-10-29 19:00:00
   📊 KG Olasılığı: %78.5
   🟢 Yüksek Güven
```

## 🏗️ Proje Yapısı

```
kgvartahmin/
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py        # SportMonks API veri çekme
│   ├── feature_engineering.py # Özellik mühendisliği
│   ├── model.py                # Makine öğrenimi modeli
│   └── predictor.py            # Tahmin motoru
├── models/                     # Eğitilmiş modeller
├── .env.example                # API key şablonu
├── .gitignore
├── config.py                   # Ayarlar
├── main.py                     # Ana program
├── requirements.txt            # Bağımlılıklar
└── README.md
```

## 🧠 Model Detayları

Model, aşağıdaki özellikleri kullanarak tahmin yapar:

- **Ev Sahibi İstatistikleri:**
  - Son maçlarda KG yüzdesi
  - Ortalama attığı gol
  - Ortalama yediği gol
  - Kalesini gole kapatma sayısı

- **Deplasman İstatistikleri:**
  - Son maçlarda KG yüzdesi
  - Ortalama attığı gol
  - Ortalama yediği gol
  - Gol atamadığı maç sayısı

- **Kombine Özellikler:**
  - Takımların birleşik KG ortalaması
  - Beklenen toplam gol sayısı
  - Savunma gücü farkı
  - Hücum gücü farkı

## 📈 Model Performansı

Model, geçmiş veriler üzerinde eğitilir ve test edilir. Tipik başarı oranı: **%65-75**

## ⚙️ Yapılandırma

`config.py` dosyasından ayarları değiştirebilirsiniz:

```python
RECENT_MATCHES_COUNT = 10  # Analiz edilecek son maç sayısı
MIN_MATCHES_FOR_PREDICTION = 5  # Tahmin için minimum maç
```

## 🔐 Güvenlik

- API anahtarınızı asla paylaşmayın
- `.env` dosyası Git'e yüklenmez (.gitignore ile korunur)

## 📝 Lisans

Bu proje kişisel kullanım içindir.

## 🤝 Katkıda Bulunma

Pull request'ler kabul edilir. Büyük değişiklikler için lütfen önce bir issue açın.

## 📧 İletişim

Sorularınız için GitHub Issues kullanabilirsiniz.

---

**Not:** Bu proje eğitim amaçlıdır. Bahis yaparken dikkatli olun ve sorumlu davranın.

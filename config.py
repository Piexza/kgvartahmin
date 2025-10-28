import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# SportMonks API ayarları
SPORTMONKS_API_KEY = os.getenv('SPORTMONKS_API_KEY')
SPORTMONKS_BASE_URL = 'https://api.sportmonks.com/v3/football'

# Model ayarları
MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': 10,
    'random_state': 42
}

# Tahmin ayarları
MIN_MATCHES_FOR_PREDICTION = 5  # Tahmin için minimum maç sayısı
RECENT_MATCHES_COUNT = 10  # Analiz edilecek son maç sayısı

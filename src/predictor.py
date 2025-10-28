from src.data_fetcher import SportMonksDataFetcher
from src.feature_engineering import FeatureEngineer
from src.model import BTTSModel
import pandas as pd

class BTTSPredictor:
    """Gelecek maçlar için KG tahmini yapan sınıf"""
    
    def __init__(self):
        self.data_fetcher = SportMonksDataFetcher()
        self.feature_engineer = FeatureEngineer()
        self.model = BTTSModel()
    
    def train_model(self, league_id, season_id):
        """Modeli belirli bir lig ve sezon verisiyle eğitir"""
        print(f"📥 Lig {league_id}, Sezon {season_id} verileri çekiliyor...")
        
        # Maç verilerini çek
        matches_df = self.data_fetcher.get_league_matches(league_id, season_id)
        
        if matches_df.empty:
            print("❌ Maç verisi bulunamadı!")
            return
        
        print(f"✅ {len(matches_df)} maç verisi çekildi")
        
        # Eğitim verisi hazırla
        print("🔄 Eğitim verisi hazırlanıyor...")
        training_data = self.feature_engineer.prepare_training_data(matches_df)
        
        if training_data.empty:
            print("❌ Eğitim verisi oluşturulamadı!")
            return
        
        print(f"✅ {len(training_data)} eğitim örneği hazırlandı")
        
        # Modeli eğit
        self.model.train(training_data)
    
    def predict_match(self, home_team_id, away_team_id, historical_matches_df):
        """Belirli bir maç için KG tahmini yapar"""
        
        # Takım istatistiklerini hesapla
        home_stats = self.feature_engineer.calculate_team_stats(
            historical_matches_df, home_team_id, is_home=True
        )
        away_stats = self.feature_engineer.calculate_team_stats(
            historical_matches_df, away_team_id, is_home=False
        )
        
        # Maç özelliklerini oluştur
        features = self.feature_engineer.create_match_features(home_stats, away_stats)
        
        # KG olasılığını tahmin et
        probability = self.model.predict_probability(features)
        
        return probability[0] if probability is not None else None
    
    def predict_upcoming_matches(self, league_id=None, historical_season_id=None):
        """Gelecek maçlar için KG tahminleri yapar"""
        
        # Gelecek maçları çek
        print("📥 Gelecek maçlar çekiliyor...")
        upcoming_df = self.data_fetcher.get_upcoming_matches(league_id)
        
        if upcoming_df.empty:
            print("❌ Gelecek maç bulunamadı!")
            return pd.DataFrame()
        
        print(f"✅ {len(upcoming_df)} gelecek maç bulundu")
        
        # Geçmiş maç verilerini çek (tahmin için)
        if historical_season_id:
            historical_df = self.data_fetcher.get_league_matches(league_id, historical_season_id)
        else:
            historical_df = pd.DataFrame()
        
        # Her maç için tahmin yap
        predictions = []
        
        for idx, match in upcoming_df.iterrows():
            print(f"\n⚽ {match['home_team_name']} vs {match['away_team_name']}")
            
            # Takımların son maçlarını çek
            home_form = self.data_fetcher.get_team_form(match['home_team_id'])
            away_form = self.data_fetcher.get_team_form(match['away_team_id'])
            
            # Tüm geçmiş verileri birleştir
            all_historical = pd.concat([historical_df, home_form, away_form]).drop_duplicates()
            
            if all_historical.empty:
                print("  ⚠️ Yeterli veri yok, tahmin yapılamıyor")
                continue
            
            # Tahmin yap
            probability = self.predict_match(
                match['home_team_id'],
                match['away_team_id'],
                all_historical
            )
            
            if probability is not None:
                print(f"  📊 KG Olasılığı: %{probability:.1f}")
                
                predictions.append({
                    'date': match['date'],
                    'home_team': match['home_team_name'],
                    'away_team': match['away_team_name'],
                    'btts_probability': probability
                })
        
        return pd.DataFrame(predictions)
    
    def save_model(self, filepath='models/btts_model.pkl'):
        """Eğitilmiş modeli kaydeder"""
        self.model.save_model(filepath)
    
    def load_model(self, filepath='models/btts_model.pkl'):
        """Kaydedilmiş modeli yükler"""
        self.model.load_model(filepath)

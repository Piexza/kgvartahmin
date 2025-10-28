from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import pandas as pd
from config import MODEL_PARAMS

class BTTSModel:
    """KG (Karşılıklı Gol) tahmini için makine öğrenimi modeli"""
    
    def __init__(self):
        self.model = RandomForestClassifier(**MODEL_PARAMS)
        self.feature_columns = None
        self.is_trained = False
    
    def train(self, training_data):
        """Modeli eğitir"""
        if training_data.empty:
            print("❌ Eğitim verisi boş!")
            return
        
        # Hedef değişken ve özellikleri ayır
        X = training_data.drop('btts_actual', axis=1)
        y = training_data['btts_actual']
        
        # Özellik sütunlarını kaydet
        self.feature_columns = X.columns.tolist()
        
        # Eğitim ve test setlerine ayır
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"📊 Eğitim seti: {len(X_train)} maç")
        print(f"📊 Test seti: {len(X_test)} maç")
        
        # Modeli eğit
        print("🔄 Model eğitiliyor...")
        self.model.fit(X_train, y_train)
        
        # Test seti üzerinde tahmin yap
        y_pred = self.model.predict(X_test)
        
        # Başarı oranını hesapla
        accuracy = accuracy_score(y_test, y_pred)
        print(f"✅ Model başarı oranı: {accuracy*100:.2f}%")
        
        # Detaylı rapor
        print("\n📈 Detaylı Rapor:")
        print(classification_report(y_test, y_pred, target_names=['KG Yok', 'KG Var']))
        
        # Özellik önem sıralaması
        self._print_feature_importance()
        
        self.is_trained = True
    
    def _print_feature_importance(self):
        """Özelliklerin önem sıralamasını gösterir"""
        if self.feature_columns is None:
            return
        
        importance_df = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n🎯 En Önemli Özellikler:")
        for idx, row in importance_df.head(5).iterrows():
            print(f"  {row['feature']}: {row['importance']*100:.2f}%")
    
    def predict_probability(self, features):
        """KG olasılığını tahmin eder"""
        if not self.is_trained:
            print("❌ Model henüz eğitilmedi!")
            return None
        
        # Özellikleri DataFrame'e çevir
        if isinstance(features, dict):
            features_df = pd.DataFrame([features])
        else:
            features_df = features
        
        # Eksik sütunları ekle (varsayılan değerlerle)
        for col in self.feature_columns:
            if col not in features_df.columns:
                features_df[col] = 0
        
        # Sütun sıralamasını düzelt
        features_df = features_df[self.feature_columns]
        
        # Olasılık tahmini yap
        probabilities = self.model.predict_proba(features_df)
        
        # KG olasılığını döndür (sınıf 1)
        return probabilities[:, 1] * 100
    
    def save_model(self, filepath='models/btts_model.pkl'):
        """Modeli kaydeder"""
        if not self.is_trained:
            print("❌ Model henüz eğitilmedi!")
            return
        
        model_data = {
            'model': self.model,
            'feature_columns': self.feature_columns
        }
        
        joblib.dump(model_data, filepath)
        print(f"💾 Model kaydedildi: {filepath}")
    
    def load_model(self, filepath='models/btts_model.pkl'):
        """Kaydedilmiş modeli yükler"""
        try:
            model_data = joblib.load(filepath)
            self.model = model_data['model']
            self.feature_columns = model_data['feature_columns']
            self.is_trained = True
            print(f"✅ Model yüklendi: {filepath}")
        except FileNotFoundError:
            print(f"❌ Model dosyası bulunamadı: {filepath}")

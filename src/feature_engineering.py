import pandas as pd
import numpy as np
from config import RECENT_MATCHES_COUNT

class FeatureEngineer:
    """Maç verileri için özellik mühendisliği yapan sınıf"""
    
    def __init__(self):
        pass
    
    def calculate_team_stats(self, matches_df, team_id, is_home=True):
        """Takım istatistiklerini hesaplar"""
        if matches_df.empty:
            return self._get_default_stats()
        
        # Takımın maçlarını filtrele
        if is_home:
            team_matches = matches_df[matches_df['home_team_id'] == team_id]
            goals_scored = team_matches['home_score']
            goals_conceded = team_matches['away_score']
        else:
            team_matches = matches_df[matches_df['away_team_id'] == team_id]
            goals_scored = team_matches['away_score']
            goals_conceded = team_matches['home_score']
        
        if len(team_matches) == 0:
            return self._get_default_stats()
        
        # Son N maça odaklan
        recent_matches = team_matches.tail(RECENT_MATCHES_COUNT)
        
        stats = {
            'matches_played': len(recent_matches),
            'btts_count': recent_matches['btts'].sum(),
            'btts_percentage': (recent_matches['btts'].sum() / len(recent_matches)) * 100,
            'avg_goals_scored': goals_scored.tail(RECENT_MATCHES_COUNT).mean(),
            'avg_goals_conceded': goals_conceded.tail(RECENT_MATCHES_COUNT).mean(),
            'avg_total_goals': recent_matches['total_goals'].mean(),
            'clean_sheets': (goals_conceded.tail(RECENT_MATCHES_COUNT) == 0).sum(),
            'failed_to_score': (goals_scored.tail(RECENT_MATCHES_COUNT) == 0).sum()
        }
        
        return stats
    
    def _get_default_stats(self):
        """Veri yoksa varsayılan istatistikler döner"""
        return {
            'matches_played': 0,
            'btts_count': 0,
            'btts_percentage': 50.0,
            'avg_goals_scored': 1.0,
            'avg_goals_conceded': 1.0,
            'avg_total_goals': 2.0,
            'clean_sheets': 0,
            'failed_to_score': 0
        }
    
    def create_match_features(self, home_stats, away_stats):
        """Maç özellikleri oluşturur"""
        features = {
            # Ev sahibi özellikleri
            'home_btts_pct': home_stats['btts_percentage'],
            'home_avg_scored': home_stats['avg_goals_scored'],
            'home_avg_conceded': home_stats['avg_goals_conceded'],
            'home_clean_sheets': home_stats['clean_sheets'],
            'home_failed_to_score': home_stats['failed_to_score'],
            
            # Deplasman özellikleri
            'away_btts_pct': away_stats['btts_percentage'],
            'away_avg_scored': away_stats['avg_goals_scored'],
            'away_avg_conceded': away_stats['avg_goals_conceded'],
            'away_clean_sheets': away_stats['clean_sheets'],
            'away_failed_to_score': away_stats['failed_to_score'],
            
            # Kombine özellikler
            'combined_btts_pct': (home_stats['btts_percentage'] + away_stats['btts_percentage']) / 2,
            'expected_total_goals': home_stats['avg_goals_scored'] + away_stats['avg_goals_scored'],
            'defensive_strength_diff': abs(home_stats['avg_goals_conceded'] - away_stats['avg_goals_conceded']),
            'offensive_strength_diff': abs(home_stats['avg_goals_scored'] - away_stats['avg_goals_scored'])
        }
        
        return features
    
    def prepare_training_data(self, matches_df):
        """Eğitim verisi hazırlar"""
        training_data = []
        
        for idx, match in matches_df.iterrows():
            # Bu maçtan önceki maçları al
            previous_matches = matches_df[matches_df['date'] < match['date']]
            
            # Ev sahibi ve deplasman takımı istatistikleri
            home_stats = self.calculate_team_stats(previous_matches, match['home_team_id'], is_home=True)
            away_stats = self.calculate_team_stats(previous_matches, match['away_team_id'], is_home=False)
            
            # Yeterli veri var mı kontrol et
            if home_stats['matches_played'] < 3 or away_stats['matches_played'] < 3:
                continue
            
            # Özellikleri oluştur
            features = self.create_match_features(home_stats, away_stats)
            features['btts_actual'] = match['btts']
            
            training_data.append(features)
        
        return pd.DataFrame(training_data)

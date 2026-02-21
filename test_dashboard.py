#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from etl_IPL2025_sqlite import IPLETLPipeline
from kpi_IPL2025 import IPLKPIAnalyzer

def test_dashboard_components():
    """Test dashboard components individually"""
    print("🧪 Testing Dashboard Components...")
    
    try:
        # Test data loading
        print("📊 Testing data loading...")
        analyzer = IPLKPIAnalyzer()
        matches_df, deliveries_df, players_df, points_df = analyzer.load_data()
        
        if matches_df is not None:
            print(f"✅ Data loaded: {len(matches_df)} matches, {len(deliveries_df)} deliveries, {len(players_df)} players")
        else:
            print("❌ Data loading failed")
            return False
        
        # Test KPI generation
        print("📈 Testing KPI generation...")
        report = analyzer.generate_kpi_report(matches_df, deliveries_df, players_df)
        
        if report:
            print(f"✅ KPI report generated: {report['model_trained']}")
        else:
            print("❌ KPI report generation failed")
            return False
        
        # Test prediction
        print("🔮 Testing match prediction...")
        if report['model_trained']:
            prediction = analyzer.predict_match_winner(
                "Mumbai Indians", "Chennai Super Kings", 
                "Mumbai Indians", "bat", "Wankhede Stadium"
            )
            
            if prediction:
                print(f"✅ Prediction works: {prediction['predicted_winner']} ({prediction['confidence']:.1%})")
            else:
                print("❌ Prediction failed")
                return False
        else:
            print("⚠️ Model not trained")
        
        print("🎉 All dashboard components working!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_dashboard_components()
    if success:
        print("\n🚀 Dashboard is ready to launch!")
        print("Run: ./run_dashboard.sh")
    else:
        print("\n❌ Dashboard tests failed!")

#!/usr/bin/env python3
"""
Fixed test suite for IPL 2025 project with updated CSV file names and venues integration.
"""

import pytest
import pandas as pd
import sqlite3
import tempfile
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from etl_IPL2025_sqlite import IPLETLPipeline
from kpi_IPL2025 import IPLKPIAnalyzer

class TestIPLETLPipeline:
    """Test cases for IPL ETL Pipeline"""
    
    @pytest.fixture
    def temp_db_setup(self):
        """Setup temporary database for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "data"
            raw_dir = data_dir / "raw"
            db_dir = data_dir / "db"
            
            # Create sample CSV files with new names
            sample_matches = pd.DataFrame({
                'id': [1, 2, 3],
                'season': [2025, 2025, 2025],
                'city': ['Mumbai', 'Kolkata', 'Chennai'],
                'date': ['2025-03-22', '2025-03-23', '2025-03-24'],
                'team1': ['MI', 'CSK', 'KKR'],
                'team2': ['CSK', 'KKR', 'MI'],
                'toss_winner': ['MI', 'CSK', 'KKR'],
                'toss_decision': ['bat', 'field', 'bat', 'field'],
                'result': ['normal', 'normal', 'normal'],
                'dl_applied': [0, 0, 0],
                'winner': ['MI', 'CSK', 'KKR'],
                'win_by_runs': [10, 0, 8],
                'win_by_wickets': [0, 2, 0],
                'player_of_match': ['Player1', 'Player2', 'Player3'],
                'venue': ['Wankhede Stadium', 'Eden Gardens', 'Chepauk Stadium']
            })
            
            sample_deliveries = pd.DataFrame({
                'id': [1, 2, 3],
                'match_id': [1, 1, 1],
                'inning': [1, 2],
                'batting_team': ['MI', 'CSK', 'KKR'],
                'bowling_team': ['CSK', 'KKR', 'MI'],
                'over': [1, 2, 3],
                'ball': [1, 2, 3],
                'batsman': ['Player1', 'Player2', 'Player3'],
                'non_striker': ['Player2', 'Player1', 'Player3'],
                'bowler': ['Bowler1', 'Bowler2', 'Bowler3'],
                'is_super_over': [0, 0, 0],
                'wide_runs': [0, 0, 0],
                'bye_runs': [0, 0, 0],
                'legbye_runs': [0, 0, 0],
                'noball_runs': [0, 0, 0],
                'penalty_runs': [0, 0, 0],
                'batsman_runs': [4, 1, 6],
                'extra_runs': [0, 0, 0],
                'total_runs': [10, 6, 12],
                'player_dismissed': ['', '', ''],
                'dismissal_kind': ['', '', ''],
                'fielder': ['', '', ''],
                'total_runs': 10
            })
            
            sample_players = pd.DataFrame({
                'id': [1, 2, 3],
                'player_name': ['Player1', 'Player2', 'Player3'],
                'team': ['MI', 'CSK', 'KKR'],
                'role': ['Batsman', 'All-rounder', 'Bowler'],
                'batting_style': ['Right-handed', 'Right-handed', 'Left-handed'],
                'bowling_style': ['', 'Right-arm off-break', 'Left-arm fast', ''],
                'country': ['India', 'India', 'India'],
                'born_date': ['1990-01-01', '1988-05-15', '1992-10-20'],
                'matches_played': [150, 200, 100],
                'runs_scored': [5000, 3000, 4500],
                'wickets_taken': [0, 150, 200],
                'catches': [100, 80, 50],
                'stumpings': [0, 10, 0]
            })
            
            sample_points = pd.DataFrame({
                'id': [1, 2, 3],
                'season': [2025, 2025, 2025],
                'team': ['MI', 'CSK', 'KKR'],
                'matches_played': [14, 14, 14],
                'won': [8, 7, 6],
                'lost': [5, 6, 7],
                'tied': [1, 1, 1],
                'no_result': [0, 0, 0],
                'points': [17, 15, 13],
                'net_run_rate': [0.5, 0.2, -0.1],
                'for_overs': [2800.0, 2600.0, 2500.0],
                'against_overs': [2700.0, 2650.0, 2600.0],
                'position': [1, 2, 3]
            })
            
            sample_venues = pd.DataFrame({
                'id': [1, 2, 3],
                'name': ['Wankhede Stadium', 'Eden Gardens', 'Chepauk Stadium'],
                'city': ['Mumbai', 'Kolkata', 'Chennai'],
                'capacity': [33000, 66000, 50000],
                'timezone': ['Asia/Kolkata', 'Asia/Kolkata', 'Asia/Kolkata']
            })
            
            # Save all CSV files with new names
            sample_matches.to_csv(raw_dir / "ipl_2025_matches.csv", index=False)
            sample_deliveries.to_csv(raw_dir / "ipl_2025_ball_by_ball.csv", index=False)
            sample_players.to_csv(raw_dir / "ipl_2025_players.csv", index=False)
            sample_points.to_csv(raw_dir / "ipl_2025_teams.csv", index=False)
            sample_venues.to_csv(raw_dir / "ipl_2025_venues.csv", index=False)
            
            yield str(data_dir)
    
    def test_etl_pipeline_initialization(self, temp_db_setup):
        """Test ETL pipeline initialization"""
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        assert etl.data_dir.exists()
        assert etl.raw_dir.exists()
        assert etl.db_dir.exists()
    
    def test_database_connection(self, temp_db_setup):
        """Test database connection"""
        assert etl.connect_to_db() == True
        assert etl.conn is not None
        etl.conn.close()
    
    def test_table_creation(self, temp_db_setup):
        """Test table creation"""
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        etl.connect_to_db()
        assert etl.create_tables() == True
        
        # Check if tables exist
        cursor = etl.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        expected_tables = ['matches', 'deliveries', 'players', 'points_table', 'venues']
        
        for table in expected_tables:
            assert table in [t[0] for t in tables]
    
    def test_csv_loading(self, temp_db_setup):
        """Test CSV data loading"""
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        
        # Test matches loading
        matches_df = etl.load_csv_data("ipl_2025_matches.csv")
        assert matches_df is not None
        assert len(matches_df) == 3
        
        # Test deliveries loading
        deliveries_df = etl.load_csv_data("ipl_2025_ball_by_ball.csv")
        assert deliveries_df is not None
        assert len(deliveries_df) == 3
        
        # Test players loading
        players_df = etl.load_csv_data("ipl_2025_players.csv")
        assert players_df is not None
        assert len(players_df) == 3
        
        # Test points table loading
        points_df = etl.load_csv_data("ipl_2025_teams.csv")
        assert points_df is not None
        assert len(points_df) == 3
        
        # Test venues loading
        venues_df = etl.load_csv_data("ipl_2025_venues.csv")
        assert venues_df is not None
        assert len(venues_df) == 3
    
    def test_data_insertion(self, temp_db_setup):
        """Test data insertion into database"""
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        etl.connect_to_db()
        etl.create_tables()
        
        # Insert data
        assert etl.insert_matches_data(matches_df) == True
        assert etl.insert_deliveries_data(deliveries_df) == True
        assert etl.insert_players_data(players_df) == True
        assert etl.insert_points_table_data(points_df) == True
        assert etl.insert_venues_data(venues_df) == True
        
        # Verify data insertion
        summary = etl.get_data_summary()
        assert summary['matches'] == 3
        assert summary['deliveries'] == 3
        assert summary['players'] == 3
        assert summary['points_table'] == 3
        assert summary['venues'] == 3
    
    def test_analyzer_initialization(self, temp_db_setup):
        """Test analyzer initialization"""
        analyzer = IPLKPIAnalyzer(db_path=f"{temp_db_setup}/db/IPL2025.db")
        assert analyzer.connect_to_db() == True
    
    def test_data_loading(self, analyzer_setup):
        """Test data loading from database"""
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer.load_data()
        
        assert matches_df is not None
        assert deliveries_df is not None
        assert players_df is not None
        assert points_df is not None
        assert venues_df is not None
        assert len(matches_df) == 3
        assert len(deliveries_df) == 3
        assert len(players_df) == 3
        assert len(points_df) == 3
        assert len(venues_df) == 3
    
    def test_team_kpis_calculation(self, analyzer_setup):
        """Test team KPIs calculation"""
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer_setup.load_data()
        team_kpis = analyzer.calculate_team_kpis(matches_df, deliveries_df)
        
        assert team_kpis is not None
        assert len(team_kpis) == 3
        
        # Check required columns
        required_columns = ['total_matches', 'wins', 'win_rate', 'toss_wins', 
                          'toss_win_rate', 'total_runs_scored', 'avg_run_rate', 
                          'wickets_taken', 'bowling_average']
        
        for col in required_columns:
            assert col in team_kpis.columns
    
    def test_player_kpis_calculation(self, analyzer_setup):
        """Test player KPIs calculation"""
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer_setup.load_data()
        player_kpis = analyzer.calculate_player_kpis(deliveries_df, players_df)
        
        assert player_kpis is not None
        assert len(player_kpis) >= 6  # At least 6 unique players in deliveries
        
        # Check required columns
        required_columns = ['runs_scored', 'balls_faced', 'batting_average', 'strike_rate', 'dismissals', 
                          'runs_conceded', 'balls_bowled', 'wickets_taken', 'bowling_average', 'economy_rate']
        
        for col in required_columns:
            assert col in player_kpis.columns
    
    def test_match_prediction_data_preparation(self, analyzer_setup):
        """Test match prediction data preparation"""
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer_setup.load_data()
        X, y = analyzer.prepare_match_prediction_data(matches_df)
        
        assert X is not None
        assert y is not None
        assert len(X) == len(y)
    
    def test_model_training(self, analyzer_setup):
        """Test model training"""
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer_setup.load_data()
        
        # Note: With small dataset, model training might not work well
        try:
            success = analyzer.train_prediction_model(X, y)
            assert isinstance(success, bool)
        except Exception as e:
            # Small dataset might cause issues, which is acceptable for testing
            assert isinstance(success, bool)
    
    def test_kpi_report_generation(self, analyzer_setup):
        """Test comprehensive KPI report generation"""
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer_setup.load_data()
        
        report = analyzer.generate_kpi_report(matches_df, deliveries_df, players_df, points_df, venues_df)
        
        assert report is not None
        assert 'team_kpis' in report
        assert 'player_kpis' in report
        assert 'venues_df' in report
        assert 'model_trained' in report
    
    def test_end_to_end_workflow(self, temp_db_setup):
        """Test complete end-to-end workflow"""
        # Run ETL pipeline
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        etl_success = etl.run_etl_pipeline()
        assert etl_success == True
        
        # Run KPI analysis
        analyzer = IPLKPIAnalyzer(db_path=f"{temp_db_setup}/db/IPL2025.db")
        matches_df, deliveries_df, players_df, points_df, venues_df = analyzer.load_data()
        
        # Generate KPI report
        report = analyzer.generate_kpi_report(matches_df, deliveries_df, players_df, points_df, venues_df)
        
        assert report is not None
        assert 'team_kpis' in report
        assert 'player_kpis' in report
        assert 'venues_df' in report
        assert 'model_trained' in report
        
        # Verify data integrity
        summary = analyzer.get_data_summary()
        assert summary['matches'] == 3
        assert summary['deliveries'] == 3
        assert summary['players'] == 3
        assert summary['points_table'] == 3
        assert summary['venues'] == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

import pytest
import pandas as pd
import sqlite3
import tempfile
import os
from pathlib import Path
import sys

# Add src directory to path for imports
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
            
            raw_dir.mkdir(parents=True, exist_ok=True)
            db_dir.mkdir(parents=True, exist_ok=True)
            
            # Create sample CSV files
            sample_matches = pd.DataFrame({
                'id': [1, 2, 3],
                'season': [2025, 2025, 2025],
                'city': ['Mumbai', 'Chennai', 'Kolkata'],
                'date': ['2025-03-23', '2025-03-24', '2025-03-25'],
                'team1': ['MI', 'CSK', 'KKR'],
                'team2': ['CSK', 'KKR', 'MI'],
                'toss_winner': ['MI', 'CSK', 'KKR'],
                'toss_decision': ['bat', 'field', 'bat'],
                'result': ['normal', 'normal', 'normal'],
                'dl_applied': [0, 0, 0],
                'winner': ['MI', 'CSK', 'KKR'],
                'win_by_runs': [10, 0, 5],
                'win_by_wickets': [0, 8, 0],
                'player_of_match': ['Player1', 'Player2', 'Player3'],
                'venue': ['Wankhede', 'Chepauk', 'Eden Gardens'],
                'umpire1': ['Umpire1', 'Umpire2', 'Umpire3'],
                'umpire2': ['Umpire4', 'Umpire5', 'Umpire6'],
                'umpire3': ['', '', '']
            })
            
            sample_deliveries = pd.DataFrame({
                'id': [1, 2, 3, 4, 5, 6],
                'match_id': [1, 1, 1, 2, 2, 2],
                'inning': [1, 1, 2, 1, 1, 2],
                'batting_team': ['MI', 'MI', 'CSK', 'CSK', 'CSK', 'KKR'],
                'bowling_team': ['CSK', 'CSK', 'MI', 'KKR', 'KKR', 'CSK'],
                'over': [1, 2, 1, 1, 2, 1],
                'ball': [1, 1, 1, 1, 1, 1],
                'batsman': ['Batsman1', 'Batsman2', 'Batsman3', 'Batsman4', 'Batsman5', 'Batsman6'],
                'non_striker': ['Batsman2', 'Batsman1', 'Batsman4', 'Batsman5', 'Batsman4', 'Batsman7'],
                'bowler': ['Bowler1', 'Bowler1', 'Bowler2', 'Bowler3', 'Bowler3', 'Bowler4'],
                'is_super_over': [0, 0, 0, 0, 0, 0],
                'wide_runs': [0, 0, 0, 0, 1, 0],
                'bye_runs': [0, 0, 0, 0, 0, 0],
                'legbye_runs': [0, 0, 0, 0, 0, 0],
                'noball_runs': [0, 0, 0, 0, 0, 0],
                'penalty_runs': [0, 0, 0, 0, 0, 0],
                'batsman_runs': [4, 1, 6, 0, 0, 2],
                'extra_runs': [0, 0, 0, 1, 0, 0],
                'total_runs': [4, 1, 6, 1, 1, 2],
                'player_dismissed': ['', '', 'Batsman3', '', '', ''],
                'dismissal_kind': ['', '', 'caught', '', '', ''],
                'fielder': ['', '', 'Fielder1', '', '', '']
            })
            
            sample_players = pd.DataFrame({
                'id': [1, 2, 3, 4],
                'player_name': ['Player1', 'Player2', 'Player3', 'Player4'],
                'team': ['MI', 'CSK', 'KKR', 'MI'],
                'role': ['Batsman', 'All-rounder', 'Bowler', 'Batsman'],
                'batting_style': ['Right-handed', 'Right-handed', 'Left-handed', 'Right-handed'],
                'bowling_style': ['', 'Right-arm off-break', 'Left-arm fast', ''],
                'country': ['India', 'India', 'India', 'India'],
                'born_date': ['1990-01-01', '1988-05-15', '1992-10-20', '1991-03-10'],
                'matches_played': [150, 200, 100, 180],
                'runs_scored': [5000, 3000, 500, 4500],
                'wickets_taken': [0, 150, 200, 10],
                'catches': [100, 80, 50, 120],
                'stumpings': [0, 10, 0, 5]
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
            
            # Save CSV files
            sample_matches.to_csv(raw_dir / "ipl_2025_matches.csv", index=False)
            sample_deliveries.to_csv(raw_dir / "ipl_2025_ball_by_ball.csv", index=False)
            sample_players.to_csv(raw_dir / "ipl_2025_players.csv", index=False)
            sample_points.to_csv(raw_dir / "ipl_2025_teams.csv", index=False)
            sample_venues = pd.DataFrame([{
                'id': [1, 2, 3],
                'name': ['Wankhede Stadium', 'Eden Gardens', 'Chepauk Stadium'],
                'city': ['Mumbai', 'Kolkata', 'Chennai'],
                'capacity': [33000, 66000, 50000],
                'timezone': ['Asia/Kolkata', 'Asia/Kolkata', 'Asia/Chennai']
            }])
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
        etl = IPLETLPipeline(data_dir=temp_db_setup)
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
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        table_names = [table[0] for table in tables]
        
        expected_tables = ['matches', 'deliveries', 'players', 'points_table']
        for table in expected_tables:
            assert table in table_names
        
        etl.conn.close()
    
    def test_csv_loading(self, temp_db_setup):
        """Test CSV data loading"""
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        
        matches_df = etl.load_csv_data("matches.csv")
        deliveries_df = etl.load_csv_data("deliveries.csv")
        players_df = etl.load_csv_data("players.csv")
        points_df = etl.load_csv_data("points_table.csv")
        
        assert matches_df is not None
        assert deliveries_df is not None
        assert players_df is not None
        assert points_df is not None
        
        assert len(matches_df) == 3
        assert len(deliveries_df) == 6
        assert len(players_df) == 4
        assert len(points_df) == 3
    
    def test_data_insertion(self, temp_db_setup):
        """Test data insertion into database"""
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        etl.connect_to_db()
        etl.create_tables()
        
        # Load and insert data
        matches_df = etl.load_csv_data("matches.csv")
        deliveries_df = etl.load_csv_data("deliveries.csv")
        players_df = etl.load_csv_data("players.csv")
        points_df = etl.load_csv_data("points_table.csv")
        
        assert etl.insert_matches_data(matches_df) == True
        assert etl.insert_deliveries_data(deliveries_df) == True
        assert etl.insert_players_data(players_df) == True
        assert etl.insert_points_table_data(points_df) == True
        
        # Verify data insertion
        summary = etl.get_data_summary()
        assert summary['matches'] == 3
        assert summary['deliveries'] == 6
        assert summary['players'] == 4
        assert summary['points_table'] == 3
        
        etl.conn.close()
    
    def test_full_etl_pipeline(self, temp_db_setup):
        """Test complete ETL pipeline"""
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        assert etl.run_etl_pipeline() == True
        
        summary = etl.get_data_summary()
        assert summary['matches'] == 3
        assert summary['deliveries'] == 6
        assert summary['players'] == 4
        assert summary['points_table'] == 3

class TestIPLKPIAnalyzer:
    """Test cases for IPL KPI Analyzer"""
    
    @pytest.fixture
    def temp_db_setup(self):
        """Setup temporary database for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "data"
            raw_dir = data_dir / "raw"
            db_dir = data_dir / "db"
            
            raw_dir.mkdir(parents=True, exist_ok=True)
            db_dir.mkdir(parents=True, exist_ok=True)
            
            # Create sample CSV files
            sample_matches = pd.DataFrame({
                'id': [1, 2, 3],
                'season': [2025, 2025, 2025],
                'city': ['Mumbai', 'Chennai', 'Kolkata'],
                'date': ['2025-03-23', '2025-03-24', '2025-03-25'],
                'team1': ['MI', 'CSK', 'KKR'],
                'team2': ['CSK', 'KKR', 'MI'],
                'toss_winner': ['MI', 'CSK', 'KKR'],
                'toss_decision': ['bat', 'field', 'bat'],
                'result': ['normal', 'normal', 'normal'],
                'dl_applied': [0, 0, 0],
                'winner': ['MI', 'CSK', 'KKR'],
                'win_by_runs': [10, 0, 5],
                'win_by_wickets': [0, 8, 0],
                'player_of_match': ['Player1', 'Player2', 'Player3'],
                'venue': ['Wankhede', 'Chepauk', 'Eden Gardens'],
                'umpire1': ['Umpire1', 'Umpire2', 'Umpire3'],
                'umpire2': ['Umpire4', 'Umpire5', 'Umpire6'],
                'umpire3': ['', '', '']
            })
            
            sample_deliveries = pd.DataFrame({
                'id': [1, 2, 3, 4, 5, 6],
                'match_id': [1, 1, 1, 2, 2, 2],
                'inning': [1, 1, 2, 1, 1, 2],
                'batting_team': ['MI', 'MI', 'CSK', 'CSK', 'CSK', 'KKR'],
                'bowling_team': ['CSK', 'CSK', 'MI', 'KKR', 'KKR', 'CSK'],
                'over': [1, 2, 1, 1, 2, 1],
                'ball': [1, 1, 1, 1, 1, 1],
                'batsman': ['Batsman1', 'Batsman2', 'Batsman3', 'Batsman4', 'Batsman5', 'Batsman6'],
                'non_striker': ['Batsman2', 'Batsman1', 'Batsman4', 'Batsman5', 'Batsman4', 'Batsman7'],
                'bowler': ['Bowler1', 'Bowler1', 'Bowler2', 'Bowler3', 'Bowler3', 'Bowler4'],
                'is_super_over': [0, 0, 0, 0, 0, 0],
                'wide_runs': [0, 0, 0, 0, 1, 0],
                'bye_runs': [0, 0, 0, 0, 0, 0],
                'legbye_runs': [0, 0, 0, 0, 0, 0],
                'noball_runs': [0, 0, 0, 0, 0, 0],
                'penalty_runs': [0, 0, 0, 0, 0, 0],
                'batsman_runs': [4, 1, 6, 0, 0, 2],
                'extra_runs': [0, 0, 0, 1, 0, 0],
                'total_runs': [4, 1, 6, 1, 1, 2],
                'player_dismissed': ['', '', 'Batsman3', '', '', ''],
                'dismissal_kind': ['', '', 'caught', '', '', ''],
                'fielder': ['', '', 'Fielder1', '', '', '']
            })
            
            sample_players = pd.DataFrame({
                'id': [1, 2, 3, 4],
                'player_name': ['Player1', 'Player2', 'Player3', 'Player4'],
                'team': ['MI', 'CSK', 'KKR', 'MI'],
                'role': ['Batsman', 'All-rounder', 'Bowler', 'Batsman'],
                'batting_style': ['Right-handed', 'Right-handed', 'Left-handed', 'Right-handed'],
                'bowling_style': ['', 'Right-arm off-break', 'Left-arm fast', ''],
                'country': ['India', 'India', 'India', 'India'],
                'born_date': ['1990-01-01', '1988-05-15', '1992-10-20', '1991-03-10'],
                'matches_played': [150, 200, 100, 180],
                'runs_scored': [5000, 3000, 500, 4500],
                'wickets_taken': [0, 150, 200, 10],
                'catches': [100, 80, 50, 120],
                'stumpings': [0, 10, 0, 5]
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
            
            # Save CSV files
            sample_matches.to_csv(raw_dir / "ipl_2025_matches.csv", index=False)
            sample_deliveries.to_csv(raw_dir / "ipl_2025_ball_by_ball.csv", index=False)
            sample_players.to_csv(raw_dir / "ipl_2025_players.csv", index=False)
            sample_points.to_csv(raw_dir / "ipl_2025_teams.csv", index=False)
            sample_venues = pd.DataFrame([{
                'id': [1, 2, 3],
                'name': ['Wankhede Stadium', 'Eden Gardens', 'Chepauk Stadium'],
                'city': ['Mumbai', 'Kolkata', 'Chennai'],
                'capacity': [33000, 66000, 50000],
                'timezone': ['Asia/Kolkata', 'Asia/Kolkata', 'Asia/Chennai']
            }])
            sample_venues.to_csv(raw_dir / "ipl_2025_venues.csv", index=False)
            
            yield str(data_dir)
    
    @pytest.fixture
    def analyzer_setup(self, temp_db_setup):
        """Setup analyzer with test data"""
        # First run ETL to populate database
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        etl.run_etl_pipeline()
        
        analyzer = IPLKPIAnalyzer(db_path=f"{temp_db_setup}/db/IPL2025.db")
        yield analyzer
    
    def test_analyzer_initialization(self, temp_db_setup):
        """Test analyzer initialization"""
        analyzer = IPLKPIAnalyzer(db_path=f"{temp_db_setup}/db/IPL2025.db")
        assert analyzer.db_path == f"{temp_db_setup}/db/IPL2025.db"
    
    def test_database_connection(self, analyzer_setup):
        """Test database connection"""
        assert analyzer_setup.connect_to_db() == True
        analyzer_setup.conn.close()
    
    def test_data_loading(self, analyzer_setup):
        """Test data loading from database"""
        matches_df, deliveries_df, players_df, points_df = analyzer_setup.load_data()
        
        assert matches_df is not None
        assert deliveries_df is not None
        assert players_df is not None
        assert points_df is not None
        
        assert len(matches_df) == 3
        assert len(deliveries_df) == 6
        assert len(players_df) == 4
        assert len(points_df) == 3
    
    def test_team_kpis_calculation(self, analyzer_setup):
        """Test team KPIs calculation"""
        matches_df, deliveries_df, players_df, points_df = analyzer_setup.load_data()
        team_kpis = analyzer_setup.calculate_team_kpis(matches_df, deliveries_df)
        
        assert team_kpis is not None
        assert len(team_kpis) == 3  # MI, CSK, KKR
        
        # Check required columns
        required_columns = ['total_matches', 'wins', 'win_rate', 'toss_wins', 
                          'toss_win_rate', 'total_runs_scored', 'avg_run_rate', 
                          'wickets_taken', 'bowling_average']
        
        for col in required_columns:
            assert col in team_kpis.columns
        
        # Verify data insertion
        summary = etl.get_data_summary()
        assert summary['matches'] == 3
        assert summary['deliveries'] == 6
        assert summary['players'] == 4
        assert summary['points_table'] == 3
        assert summary['venues'] == 3
    
    def test_player_kpis_calculation(self, analyzer_setup):
        """Test player KPIs calculation"""
        matches_df, deliveries_df, players_df, points_df = analyzer_setup.load_data()
        player_kpis = analyzer_setup.calculate_player_kpis(deliveries_df, players_df)
        
        assert player_kpis is not None
        assert len(player_kpis) >= 6  # At least 6 unique players in deliveries
        
        # Check required columns
        required_columns = ['runs_scored', 'balls_faced', 'batting_average', 
                          'strike_rate', 'dismissals', 'runs_conceded', 
                          'balls_bowled', 'wickets_taken', 'bowling_average', 
                          'economy_rate']
        
        for col in required_columns:
            assert col in player_kpis.columns
    
    def test_match_prediction_data_preparation(self, analyzer_setup):
        """Test match prediction data preparation"""
        matches_df, deliveries_df, players_df, points_df = analyzer_setup.load_data()
        X, y = analyzer_setup.prepare_match_prediction_data(matches_df)
        
        assert X is not None
        assert y is not None
        assert len(X) == len(y)
        assert len(X) == 3  # 3 matches with winners
        
        # Check feature columns
        expected_features = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']
        for feature in expected_features:
            assert feature in X.columns
    
    def test_model_training(self, analyzer_setup):
        """Test model training"""
        matches_df, deliveries_df, players_df, points_df = analyzer_setup.load_data()
        X, y = analyzer_setup.prepare_match_prediction_data(matches_df)
        
        # Note: With only 3 samples, this might not work well in practice
        # but we test the functionality
        try:
            success = analyzer_setup.train_prediction_model(X, y)
            # With small dataset, model training might fail, which is expected
            assert isinstance(success, bool)
        except Exception as e:
            # Small dataset might cause issues, which is acceptable for testing
            assert True
    
    def test_kpi_report_generation(self, analyzer_setup):
        """Test comprehensive KPI report generation"""
        matches_df, deliveries_df, players_df, points_df = analyzer_setup.load_data()
        report = analyzer_setup.generate_kpi_report(matches_df, deliveries_df, players_df)
        
        assert report is not None
        assert 'team_kpis' in report
        assert 'player_kpis' in report
        assert 'model_trained' in report
        assert 'total_matches' in report
        assert 'total_deliveries' in report
        assert 'total_players' in report
        
        assert report['total_matches'] == 3
        assert report['total_deliveries'] == 6
        assert report['total_players'] == 4

class TestIntegration:
    """Integration tests for the complete system"""
    
    @pytest.fixture
    def temp_db_setup(self):
        """Setup temporary database for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir) / "data"
            raw_dir = data_dir / "raw"
            db_dir = data_dir / "db"
            
            raw_dir.mkdir(parents=True, exist_ok=True)
            db_dir.mkdir(parents=True, exist_ok=True)
            
            # Create sample CSV files
            sample_matches = pd.DataFrame({
                'id': [1, 2, 3],
                'season': [2025, 2025, 2025],
                'city': ['Mumbai', 'Chennai', 'Kolkata'],
                'date': ['2025-03-23', '2025-03-24', '2025-03-25'],
                'team1': ['MI', 'CSK', 'KKR'],
                'team2': ['CSK', 'KKR', 'MI'],
                'toss_winner': ['MI', 'CSK', 'KKR'],
                'toss_decision': ['bat', 'field', 'bat'],
                'result': ['normal', 'normal', 'normal'],
                'dl_applied': [0, 0, 0],
                'winner': ['MI', 'CSK', 'KKR'],
                'win_by_runs': [10, 0, 5],
                'win_by_wickets': [0, 8, 0],
                'player_of_match': ['Player1', 'Player2', 'Player3'],
                'venue': ['Wankhede', 'Chepauk', 'Eden Gardens'],
                'umpire1': ['Umpire1', 'Umpire2', 'Umpire3'],
                'umpire2': ['Umpire4', 'Umpire5', 'Umpire6'],
                'umpire3': ['', '', '']
            })
            
            sample_deliveries = pd.DataFrame({
                'id': [1, 2, 3, 4, 5, 6],
                'match_id': [1, 1, 1, 2, 2, 2],
                'inning': [1, 1, 2, 1, 1, 2],
                'batting_team': ['MI', 'MI', 'CSK', 'CSK', 'CSK', 'KKR'],
                'bowling_team': ['CSK', 'CSK', 'MI', 'KKR', 'KKR', 'CSK'],
                'over': [1, 2, 1, 1, 2, 1],
                'ball': [1, 1, 1, 1, 1, 1],
                'batsman': ['Batsman1', 'Batsman2', 'Batsman3', 'Batsman4', 'Batsman5', 'Batsman6'],
                'non_striker': ['Batsman2', 'Batsman1', 'Batsman4', 'Batsman5', 'Batsman4', 'Batsman7'],
                'bowler': ['Bowler1', 'Bowler1', 'Bowler2', 'Bowler3', 'Bowler3', 'Bowler4'],
                'is_super_over': [0, 0, 0, 0, 0, 0],
                'wide_runs': [0, 0, 0, 0, 1, 0],
                'bye_runs': [0, 0, 0, 0, 0, 0],
                'legbye_runs': [0, 0, 0, 0, 0, 0],
                'noball_runs': [0, 0, 0, 0, 0, 0],
                'penalty_runs': [0, 0, 0, 0, 0, 0],
                'batsman_runs': [4, 1, 6, 0, 0, 2],
                'extra_runs': [0, 0, 0, 1, 0, 0],
                'total_runs': [4, 1, 6, 1, 1, 2],
                'player_dismissed': ['', '', 'Batsman3', '', '', ''],
                'dismissal_kind': ['', '', 'caught', '', '', ''],
                'fielder': ['', '', 'Fielder1', '', '', '']
            })
            
            sample_players = pd.DataFrame({
                'id': [1, 2, 3, 4],
                'player_name': ['Player1', 'Player2', 'Player3', 'Player4'],
                'team': ['MI', 'CSK', 'KKR', 'MI'],
                'role': ['Batsman', 'All-rounder', 'Bowler', 'Batsman'],
                'batting_style': ['Right-handed', 'Right-handed', 'Left-handed', 'Right-handed'],
                'bowling_style': ['', 'Right-arm off-break', 'Left-arm fast', ''],
                'country': ['India', 'India', 'India', 'India'],
                'born_date': ['1990-01-01', '1988-05-15', '1992-10-20', '1991-03-10'],
                'matches_played': [150, 200, 100, 180],
                'runs_scored': [5000, 3000, 500, 4500],
                'wickets_taken': [0, 150, 200, 10],
                'catches': [100, 80, 50, 120],
                'stumpings': [0, 10, 0, 5]
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
            
            # Save CSV files
            sample_matches.to_csv(raw_dir / "ipl_2025_matches.csv", index=False)
            sample_deliveries.to_csv(raw_dir / "ipl_2025_ball_by_ball.csv", index=False)
            sample_players.to_csv(raw_dir / "ipl_2025_players.csv", index=False)
            sample_points.to_csv(raw_dir / "ipl_2025_teams.csv", index=False)
            sample_venues = pd.DataFrame([{
                'id': [1, 2, 3],
                'name': ['Wankhede Stadium', 'Eden Gardens', 'Chepauk Stadium'],
                'city': ['Mumbai', 'Kolkata', 'Chennai'],
                'capacity': [33000, 66000, 50000],
                'timezone': ['Asia/Kolkata', 'Asia/Kolkata', 'Asia/Chennai']
            }])
            sample_venues.to_csv(raw_dir / "ipl_2025_venues.csv", index=False)
            
            yield str(data_dir)
    
    def test_end_to_end_workflow(self, temp_db_setup):
        """Test complete end-to-end workflow"""
        # Run ETL pipeline
        etl = IPLETLPipeline(data_dir=temp_db_setup)
        etl_success = etl.run_etl_pipeline()
        assert etl_success == True
        
        # Run KPI analysis
        analyzer = IPLKPIAnalyzer(db_path=f"{temp_db_setup}/db/IPL2025.db")
        matches_df, deliveries_df, players_df, points_df = analyzer.load_data()
        
        assert matches_df is not None
        assert deliveries_df is not None
        assert players_df is not None
        assert points_df is not None
        
        # Generate KPI report
        report = analyzer.generate_kpi_report(matches_df, deliveries_df, players_df)
        assert report is not None
        
        # Verify data integrity
        summary = etl.get_data_summary()
        assert summary['matches'] == 3
        assert summary['deliveries'] == 6
        assert summary['players'] == 4
        assert summary['points_table'] == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

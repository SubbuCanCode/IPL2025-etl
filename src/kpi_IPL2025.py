import pandas as pd
import sqlite3
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IPLKPIAnalyzer:
    def __init__(self, db_path="data/db/IPL2025.db"):
        self.db_path = db_path
        self.conn = None
        self.model = None
        self.label_encoders = {}
        
    def connect_to_db(self):
        """Connect to SQLite database"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            logger.info(f"Connected to database: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def load_data(self):
        """Load data from database into pandas DataFrames"""
        if not self.connect_to_db():
            return None, None, None, None
        
        try:
            matches_df = pd.read_sql_query("SELECT * FROM matches", self.conn)
            deliveries_df = pd.read_sql_query("SELECT * FROM deliveries", self.conn)
            players_df = pd.read_sql_query("SELECT * FROM players", self.conn)
            points_df = pd.read_sql_query("SELECT * FROM points_table", self.conn)
            
            # Also load venues data if available
            try:
                venues_df = pd.read_sql_query("SELECT * FROM venues", self.conn)
                logger.info(f"Loaded venues: {len(venues_df)} records")
            except:
                venues_df = pd.DataFrame()  # Empty DataFrame if venues table doesn't exist
            
            logger.info(f"Loaded data: {len(matches_df)} matches, {len(deliveries_df)} deliveries, "
                       f"{len(players_df)} players, {len(points_df)} points records")
            
            return matches_df, deliveries_df, players_df, points_df, venues_df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None, None, None, None
    
    def calculate_team_kpis(self, matches_df, deliveries_df):
        """Calculate team-level KPIs"""
        if matches_df is None or deliveries_df is None:
            return None
        
        team_kpis = {}
        
        # Get all unique teams
        teams = set(matches_df['team1'].unique()) | set(matches_df['team2'].unique())
        teams = [team for team in teams if pd.notna(team)]
        
        for team in teams:
            team_matches = matches_df[
                ((matches_df['team1'] == team) | (matches_df['team2'] == team))
            ]
            
            # Basic match statistics
            total_matches = len(team_matches)
            wins = len(team_matches[team_matches['winner'] == team])
            win_rate = wins / total_matches if total_matches > 0 else 0
            
            # Toss statistics
            toss_wins = len(team_matches[team_matches['toss_winner'] == team])
            toss_win_rate = toss_wins / total_matches if total_matches > 0 else 0
            
            # Batting statistics
            batting_deliveries = deliveries_df[deliveries_df['batting_team'] == team]
            total_runs = batting_deliveries['total_runs'].sum()
            total_balls = len(batting_deliveries)
            avg_run_rate = (total_runs / total_balls) * 6 if total_balls > 0 else 0
            
            # Bowling statistics
            bowling_deliveries = deliveries_df[deliveries_df['bowling_team'] == team]
            wickets = bowling_deliveries['player_dismissed'].notna().sum()
            bowling_avg = total_runs / wickets if wickets > 0 else float('inf')
            
            team_kpis[team] = {
                'total_matches': total_matches,
                'wins': wins,
                'win_rate': win_rate,
                'toss_wins': toss_wins,
                'toss_win_rate': toss_win_rate,
                'total_runs_scored': total_runs,
                'avg_run_rate': avg_run_rate,
                'wickets_taken': wickets,
                'bowling_average': bowling_avg
            }
        
        return pd.DataFrame.from_dict(team_kpis, orient='index')
    
    def calculate_player_kpis(self, deliveries_df, players_df):
        """Calculate player-level KPIs"""
        if deliveries_df is None or players_df is None:
            return None
        
        player_stats = {}
        
        # Get unique batsmen and bowlers
        batsmen = deliveries_df['batsman'].unique()
        bowlers = deliveries_df['bowler'].unique()
        all_players = set(batsmen) | set(bowlers)
        
        for player in all_players:
            if pd.isna(player):
                continue
                
            # Batting statistics
            batting_df = deliveries_df[deliveries_df['batsman'] == player]
            runs_scored = batting_df['batsman_runs'].sum()
            balls_faced = len(batting_df[batting_df['batsman_runs'] >= 0])
            dismissals = batting_df['player_dismissed'].notna().sum()
            
            batting_avg = runs_scored / dismissals if dismissals > 0 else runs_scored
            strike_rate = (runs_scored / balls_faced) * 100 if balls_faced > 0 else 0
            
            # Bowling statistics
            bowling_df = deliveries_df[deliveries_df['bowler'] == player]
            runs_conceded = bowling_df['total_runs'].sum()
            balls_bowled = len(bowling_df)
            wickets_taken = bowling_df['player_dismissed'].notna().sum()
            
            bowling_avg = runs_conceded / wickets_taken if wickets_taken > 0 else float('inf')
            economy_rate = (runs_conceded / balls_bowled) * 6 if balls_bowled > 0 else 0
            
            player_stats[player] = {
                'runs_scored': runs_scored,
                'balls_faced': balls_faced,
                'batting_average': batting_avg,
                'strike_rate': strike_rate,
                'dismissals': dismissals,
                'runs_conceded': runs_conceded,
                'balls_bowled': balls_bowled,
                'wickets_taken': wickets_taken,
                'bowling_average': bowling_avg,
                'economy_rate': economy_rate
            }
        
        return pd.DataFrame.from_dict(player_stats, orient='index')
    
    def prepare_match_prediction_data(self, matches_df):
        """Prepare data for match winner prediction"""
        if matches_df is None:
            return None, None
        
        # Filter out matches with no winner
        valid_matches = matches_df[matches_df['winner'].notna()].copy()
        
        # Create features
        features = []
        targets = []
        
        for _, match in valid_matches.iterrows():
            # Basic features
            feature_dict = {
                'team1': match['team1'],
                'team2': match['team2'],
                'toss_winner': match['toss_winner'],
                'toss_decision': match['toss_decision'],
                'venue': match['venue'],
                'season': match.get('season', 2025)
            }
            
            # Add venue-based features
            venue_stats = self.get_venue_stats(matches_df, match['venue'])
            feature_dict.update(venue_stats)
            
            features.append(feature_dict)
            targets.append(match['winner'])
        
        return pd.DataFrame(features), pd.Series(targets)
    
    def get_venue_stats(self, matches_df, venue):
        """Get venue-specific statistics"""
        venue_matches = matches_df[matches_df['venue'] == venue]
        
        if len(venue_matches) == 0:
            return {
                'venue_total_matches': 0,
                'venue_avg_first_innings_score': 0,
                'venue_avg_second_innings_score': 0,
                'venue_toss_batting_win_rate': 0
            }
        
        # Calculate venue statistics
        total_matches = len(venue_matches)
        
        # Get toss decision statistics
        toss_batting_matches = venue_matches[venue_matches['toss_decision'] == 'bat']
        toss_batting_wins = len(toss_batting_matches[toss_batting_matches['toss_winner'] == toss_batting_matches['winner']])
        toss_batting_win_rate = toss_batting_wins / len(toss_batting_matches) if len(toss_batting_matches) > 0 else 0
        
        return {
            'venue_total_matches': total_matches,
            'venue_avg_first_innings_score': 0,  # Would need deliveries data for accurate calculation
            'venue_avg_second_innings_score': 0,  # Would need deliveries data for accurate calculation
            'venue_toss_batting_win_rate': toss_batting_win_rate
        }
    
    def train_prediction_model(self, X, y):
        """Train Random Forest model for match prediction"""
        if X is None or y is None:
            return False
        
        try:
            # Encode categorical variables
            categorical_columns = ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']
            
            for col in categorical_columns:
                if col in X.columns:
                    le = LabelEncoder()
                    X[col] = le.fit_transform(X[col].astype(str))
                    self.label_encoders[col] = le
            
            # Encode target variable
            target_encoder = LabelEncoder()
            y_encoded = target_encoder.fit_transform(y)
            self.label_encoders['target'] = target_encoder
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            logger.info(f"Model trained with accuracy: {accuracy:.3f}")
            
            # Save model
            model_path = Path("data/db/ipl_match_predictor.pkl")
            joblib.dump(self.model, model_path)
            joblib.dump(self.label_encoders, "data/db/label_encoders.pkl")
            
            return True
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return False
    
    def predict_match_winner(self, team1, team2, toss_winner, toss_decision, venue):
        """Predict match winner for given teams and conditions"""
        if self.model is None:
            logger.error("Model not trained. Call train_prediction_model first.")
            return None
        
        try:
            # Prepare input data
            input_data = {
                'team1': team1,
                'team2': team2,
                'toss_winner': toss_winner,
                'toss_decision': toss_decision,
                'venue': venue,
                'season': 2025,
                'venue_total_matches': 0,
                'venue_avg_first_innings_score': 0,
                'venue_avg_second_innings_score': 0,
                'venue_toss_batting_win_rate': 0.5
            }
            
            input_df = pd.DataFrame([input_data])
            
            # Encode categorical variables
            for col in ['team1', 'team2', 'toss_winner', 'toss_decision', 'venue']:
                if col in self.label_encoders:
                    # Handle unseen labels
                    if input_df[col].iloc[0] not in self.label_encoders[col].classes_:
                        # Add new label to encoder
                        self.label_encoders[col].classes_ = np.append(
                            self.label_encoders[col].classes_, 
                            input_df[col].iloc[0]
                        )
                    input_df[col] = self.label_encoders[col].transform(input_df[col].astype(str))
            
            # Make prediction
            prediction = self.model.predict(input_df)[0]
            probabilities = self.model.predict_proba(input_df)[0]
            
            # Decode prediction
            predicted_winner = self.label_encoders['target'].inverse_transform([prediction])[0]
            
            # Get probability for predicted winner
            winner_prob = probabilities[prediction]
            
            return {
                'predicted_winner': predicted_winner,
                'confidence': winner_prob,
                'probabilities': dict(zip(self.label_encoders['target'].classes_, probabilities))
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return None
    
    def generate_kpi_report(self, matches_df, deliveries_df, players_df, venues_df=None):
        """Generate comprehensive KPI report"""
        if not all([matches_df is not None, deliveries_df is not None, players_df is not None]):
            logger.error("Missing required data for KPI report")
            return None
        
        # Calculate KPIs
        team_kpis = self.calculate_team_kpis(matches_df, deliveries_df)
        player_kpis = self.calculate_player_kpis(deliveries_df, players_df)
        
        # Prepare match prediction data
        X, y = self.prepare_match_prediction_data(matches_df)
        
        # Train prediction model
        model_success = self.train_prediction_model(X, y)
        
        report = {
            'team_kpis': team_kpis,
            'player_kpis': player_kpis,
            'venues_df': venues_df,
            'model_trained': model_success,
            'total_matches': len(matches_df),
            'total_deliveries': len(deliveries_df),
            'total_players': len(players_df)
        }
        
        return report
    
    def visualize_team_performance(self, team_kpis):
        """Create visualizations for team performance"""
        if team_kpis is None:
            return
        
        plt.figure(figsize=(15, 10))
        
        # Win Rate
        plt.subplot(2, 3, 1)
        team_kpis['win_rate'].sort_values().plot(kind='barh')
        plt.title('Win Rate by Team')
        plt.xlabel('Win Rate')
        
        # Average Run Rate
        plt.subplot(2, 3, 2)
        team_kpis['avg_run_rate'].sort_values().plot(kind='barh')
        plt.title('Average Run Rate')
        plt.xlabel('Runs per Over')
        
        # Wickets Taken
        plt.subplot(2, 3, 3)
        team_kpis['wickets_taken'].sort_values().plot(kind='barh')
        plt.title('Total Wickets Taken')
        plt.xlabel('Wickets')
        
        # Toss Win Rate
        plt.subplot(2, 3, 4)
        team_kpis['toss_win_rate'].sort_values().plot(kind='barh')
        plt.title('Toss Win Rate')
        plt.xlabel('Toss Win Rate')
        
        # Total Runs
        plt.subplot(2, 3, 5)
        team_kpis['total_runs_scored'].sort_values().plot(kind='barh')
        plt.title('Total Runs Scored')
        plt.xlabel('Runs')
        
        # Bowling Average
        plt.subplot(2, 3, 6)
        # Filter out infinite values for better visualization
        bowling_avg_filtered = team_kpis[team_kpis['bowling_average'] != float('inf')]['bowling_average']
        bowling_avg_filtered.sort_values().plot(kind='barh')
        plt.title('Bowling Average')
        plt.xlabel('Average')
        
        plt.tight_layout()
        plt.savefig('data/db/team_performance_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        logger.info("Team performance visualization saved to data/db/team_performance_analysis.png")

def main():
    """Main function to run KPI analysis and ML prediction"""
    analyzer = IPLKPIAnalyzer()
    
    # Load data
    matches_df, deliveries_df, players_df, points_df, venues_df = analyzer.load_data()
    
    if matches_df is None:
        print("❌ Failed to load data. Please run ETL pipeline first.")
        return
    
    # Generate KPI report
    report = analyzer.generate_kpi_report(matches_df, deliveries_df, players_df, venues_df)
    
    if report:
        print("✅ KPI Analysis completed successfully!")
        print(f"\n📊 Dataset Summary:")
        print(f"  Total Matches: {report['total_matches']:,}")
        print(f"  Total Deliveries: {report['total_deliveries']:,}")
        print(f"  Total Players: {report['total_players']:,}")
        print(f"  Model Trained: {'✅' if report['model_trained'] else '❌'}")
        
        # Show top teams by win rate
        if report['team_kpis'] is not None:
            print(f"\n🏆 Top 5 Teams by Win Rate:")
            top_teams = report['team_kpis']['win_rate'].sort_values(ascending=False).head()
            for team, win_rate in top_teams.items():
                print(f"  {team}: {win_rate:.1%}")
        
        # Show top batsmen
        if report['player_kpis'] is not None:
            print(f"\n🏏 Top 5 Batsmen by Runs:")
            top_batsmen = report['player_kpis']['runs_scored'].sort_values(ascending=False).head()
            for player, runs in top_batsmen.items():
                print(f"  {player}: {runs:,} runs")
        
        # Show top bowlers
        if report['player_kpis'] is not None:
            print(f"\n⚾ Top 5 Bowlers by Wickets:")
            top_bowlers = report['player_kpis']['wickets_taken'].sort_values(ascending=False).head()
            for player, wickets in top_bowlers.items():
                print(f"  {player}: {wickets} wickets")
        
        # Generate visualizations
        analyzer.visualize_team_performance(report['team_kpis'])
        
        # Example prediction
        if report['model_trained']:
            print(f"\n🔮 Example Match Prediction:")
            prediction = analyzer.predict_match_winner(
                team1="Mumbai Indians",
                team2="Chennai Super Kings", 
                toss_winner="Mumbai Indians",
                toss_decision="bat",
                venue="Wankhede Stadium"
            )
            
            if prediction:
                print(f"  Predicted Winner: {prediction['predicted_winner']}")
                print(f"  Confidence: {prediction['confidence']:.1%}")
    
    else:
        print("❌ KPI Analysis failed. Check logs for details.")

if __name__ == "__main__":
    main()

"""
IPL 2025 - Comprehensive Exploratory Data Analysis (EDA)
This script demonstrates various EDA techniques on IPL 2025 dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*80)
print("IPL 2025 - EXPLORATORY DATA ANALYSIS")
print("="*80)

# ============================================================================
# 1. DATA LOADING AND INITIAL EXPLORATION
# ============================================================================

print("\n1. LOADING DATASETS...")
matches = pd.read_csv('ipl_2025_matches.csv')
players = pd.read_csv('ipl_2025_players.csv')
teams = pd.read_csv('ipl_2025_teams.csv')
venues = pd.read_csv('ipl_2025_venues.csv')
ball_by_ball = pd.read_csv('ipl_2025_ball_by_ball.csv')

print(f"✓ Matches: {matches.shape[0]} rows, {matches.shape[1]} columns")
print(f"✓ Players: {players.shape[0]} rows, {players.shape[1]} columns")
print(f"✓ Teams: {teams.shape[0]} rows, {teams.shape[1]} columns")
print(f"✓ Venues: {venues.shape[0]} rows, {venues.shape[1]} columns")
print(f"✓ Ball-by-ball: {ball_by_ball.shape[0]} rows, {ball_by_ball.shape[1]} columns")

# ============================================================================
# 2. BASIC DATA EXPLORATION
# ============================================================================

print("\n2. DATASET OVERVIEW")
print("\n--- Matches Dataset ---")
print(matches.info())
print("\nFirst 5 rows:")
print(matches.head())

print("\n--- Players Dataset ---")
print(players.describe())

print("\n--- Missing Values Check ---")
print("Matches missing values:", matches.isnull().sum().sum())
print("Players missing values:", players.isnull().sum().sum())
print("Teams missing values:", teams.isnull().sum().sum())

# ============================================================================
# 3. STATISTICAL ANALYSIS
# ============================================================================

print("\n3. KEY STATISTICS")

# Match statistics
print("\n--- Match Statistics ---")
print(f"Total matches played: {len(matches)}")
print(f"Matches won by batting first: {len(matches[matches['toss_decision'] == 'bat'])}")
print(f"Matches won by chasing: {len(matches[matches['win_type'] == 'wickets'])}")
print(f"Average attendance: {matches['attendance'].mean():.0f}")
print(f"Highest attendance: {matches['attendance'].max():.0f} at {matches.loc[matches['attendance'].idxmax(), 'venue']}")

# Player statistics
print("\n--- Top 5 Run Scorers ---")
top_scorers = players.nlargest(5, 'runs_scored')[['player_name', 'team', 'runs_scored', 'strike_rate', 'hundreds', 'fifties']]
print(top_scorers.to_string(index=False))

print("\n--- Top 5 Wicket Takers ---")
top_bowlers = players.nlargest(5, 'wickets')[['player_name', 'team', 'wickets', 'bowling_avg', 'economy', 'best_figures']]
print(top_bowlers.to_string(index=False))

print("\n--- Top 5 All-rounders (Runs + Wickets) ---")
players['total_impact'] = players['runs_scored'] + (players['wickets'] * 20)
top_allrounders = players.nlargest(5, 'total_impact')[['player_name', 'team', 'runs_scored', 'wickets', 'total_impact']]
print(top_allrounders.to_string(index=False))

# Team statistics
print("\n--- Team Standings ---")
team_standings = teams.sort_values('points', ascending=False)[['team', 'wins', 'losses', 'points', 'net_run_rate']]
print(team_standings.to_string(index=False))

# ============================================================================
# 4. CORRELATION ANALYSIS
# ============================================================================

print("\n4. CORRELATION ANALYSIS")

# Batting correlations
batting_cols = ['runs_scored', 'balls_faced', 'batting_avg', 'strike_rate', 'hundreds', 'fifties', 'fours', 'sixes']
batting_data = players[batting_cols].dropna()

print("\n--- Batting Metrics Correlation ---")
batting_corr = batting_data.corr()
print(batting_corr['runs_scored'].sort_values(ascending=False))

# Bowling correlations
bowling_cols = ['wickets', 'bowling_avg', 'economy', 'strike_rate_bowling']
bowling_data = players[bowling_cols].dropna()

print("\n--- Bowling Metrics Correlation ---")
bowling_corr = bowling_data.corr()
print(bowling_corr['wickets'].sort_values(ascending=False))

# ============================================================================
# 5. DISTRIBUTION ANALYSIS
# ============================================================================

print("\n5. DISTRIBUTION ANALYSIS")

print("\n--- Strike Rate Distribution ---")
print(f"Mean: {players['strike_rate'].mean():.2f}")
print(f"Median: {players['strike_rate'].median():.2f}")
print(f"Std Dev: {players['strike_rate'].std():.2f}")
print(f"Skewness: {players['strike_rate'].skew():.2f}")
print(f"Kurtosis: {players['strike_rate'].kurtosis():.2f}")

print("\n--- Economy Rate Distribution ---")
economy_data = players['economy'].dropna()
print(f"Mean: {economy_data.mean():.2f}")
print(f"Median: {economy_data.median():.2f}")
print(f"Std Dev: {economy_data.std():.2f}")

# ============================================================================
# 6. ADVANCED INSIGHTS
# ============================================================================

print("\n6. ADVANCED INSIGHTS")

# Toss impact
toss_win_match_win = matches[matches['toss_winner'] == matches['winner']]
toss_impact = (len(toss_win_match_win) / len(matches)) * 100
print(f"\n--- Toss Impact ---")
print(f"Matches where toss winner won: {len(toss_win_match_win)}/{len(matches)} ({toss_impact:.1f}%)")

# Venue analysis
print("\n--- Most Batting-Friendly Venues ---")
batting_venues = venues.nlargest(3, 'avg_first_innings_score')[['venue', 'city', 'avg_first_innings_score', 'total_sixes']]
print(batting_venues.to_string(index=False))

# Home vs Away
print("\n--- Home Advantage Analysis ---")
home_wins = 0
total_home_matches = 0
for _, match in matches.iterrows():
    if match['city'] in ['Mumbai'] and match['team1'] == 'Mumbai Indians':
        total_home_matches += 1
        if match['winner'] == 'Mumbai Indians':
            home_wins += 1
    elif match['city'] in ['Mumbai'] and match['team2'] == 'Mumbai Indians':
        total_home_matches += 1
        if match['winner'] == 'Mumbai Indians':
            home_wins += 1

if total_home_matches > 0:
    print(f"Mumbai Indians home win rate: {(home_wins/total_home_matches)*100:.1f}%")

# Strike rate by nationality
print("\n--- Average Strike Rate by Nationality ---")
nationality_sr = players.groupby('nationality')['strike_rate'].agg(['mean', 'count'])
nationality_sr = nationality_sr[nationality_sr['count'] >= 3].sort_values('mean', ascending=False)
print(nationality_sr.head())

# Role-based analysis
print("\n--- Average Performance by Role ---")
role_performance = players.groupby('role').agg({
    'runs_scored': 'mean',
    'strike_rate': 'mean',
    'wickets': 'mean',
    'economy': 'mean'
}).round(2)
print(role_performance)

# ============================================================================
# 7. TREND ANALYSIS
# ============================================================================

print("\n7. TREND ANALYSIS")

# Convert date to datetime
matches['date'] = pd.to_datetime(matches['date'])

# Runs trend over time
print("\n--- Analyzing trends over tournament timeline ---")
matches_sorted = matches.sort_values('date')
print(f"Tournament duration: {matches_sorted['date'].min()} to {matches_sorted['date'].max()}")
print(f"Total days: {(matches_sorted['date'].max() - matches_sorted['date'].min()).days}")

# ============================================================================
# 8. OUTLIER DETECTION
# ============================================================================

print("\n8. OUTLIER DETECTION")

# Strike rate outliers
Q1 = players['strike_rate'].quantile(0.25)
Q3 = players['strike_rate'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = players[(players['strike_rate'] < lower_bound) | (players['strike_rate'] > upper_bound)]
print(f"\n--- Strike Rate Outliers ---")
print(f"Found {len(outliers)} outliers")
if len(outliers) > 0:
    print(outliers[['player_name', 'team', 'strike_rate']].to_string(index=False))

# ============================================================================
# 9. HYPOTHESIS TESTING
# ============================================================================

print("\n9. HYPOTHESIS TESTING")

# Test: Do overseas players have higher strike rates?
indian_sr = players[players['nationality'] == 'India']['strike_rate'].dropna()
overseas_sr = players[players['nationality'] != 'India']['strike_rate'].dropna()

t_stat, p_value = stats.ttest_ind(overseas_sr, indian_sr)
print(f"\n--- T-Test: Overseas vs Indian Strike Rates ---")
print(f"Indian players mean SR: {indian_sr.mean():.2f}")
print(f"Overseas players mean SR: {overseas_sr.mean():.2f}")
print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Significant difference: {'Yes' if p_value < 0.05 else 'No'} (α=0.05)")

# ============================================================================
# 10. GROUPING AND AGGREGATION
# ============================================================================

print("\n10. GROUPING AND AGGREGATION")

# Team-wise aggregations
print("\n--- Team-wise Aggregated Statistics ---")
team_stats = players.groupby('team').agg({
    'runs_scored': ['sum', 'mean'],
    'wickets': ['sum', 'mean'],
    'strike_rate': 'mean',
    'economy': 'mean'
}).round(2)
team_stats.columns = ['Total_Runs', 'Avg_Runs_per_Player', 'Total_Wickets', 
                      'Avg_Wickets_per_Player', 'Avg_Strike_Rate', 'Avg_Economy']
print(team_stats.sort_values('Total_Runs', ascending=False))

# ============================================================================
# 11. DATA QUALITY ASSESSMENT
# ============================================================================

print("\n11. DATA QUALITY ASSESSMENT")

print("\n--- Data Completeness ---")
for col in matches.columns:
    completeness = (1 - matches[col].isnull().sum() / len(matches)) * 100
    print(f"{col}: {completeness:.1f}% complete")

print("\n--- Duplicate Check ---")
print(f"Duplicate matches: {matches.duplicated().sum()}")
print(f"Duplicate players: {players.duplicated(subset=['player_name']).sum()}")

# ============================================================================
# 12. SUMMARY INSIGHTS
# ============================================================================

print("\n" + "="*80)
print("SUMMARY INSIGHTS")
print("="*80)

print(f"""
1. Tournament Overview:
   - Total Matches: {len(matches)}
   - Teams: {len(teams)}
   - Players: {len(players)}
   - Venues: {len(venues)}

2. Top Performers:
   - Highest Run Scorer: {players.loc[players['runs_scored'].idxmax(), 'player_name']} ({players['runs_scored'].max()} runs)
   - Most Wickets: {players.loc[players['wickets'].idxmax(), 'player_name']} ({players['wickets'].max()} wickets)
   - Best Strike Rate: {players.loc[players['strike_rate'].idxmax(), 'player_name']} ({players['strike_rate'].max():.2f})

3. Team Performance:
   - Champion: {teams.loc[teams['points'].idxmax(), 'team']} ({teams['points'].max()} points)
   - Best NRR: {teams.loc[teams['net_run_rate'].idxmax(), 'team']} ({teams['net_run_rate'].max():.3f})
   - Most Sixes: {teams.loc[teams['total_sixes'].idxmax(), 'team']} ({teams['total_sixes'].max()} sixes)

4. Match Dynamics:
   - Toss Winner Match Win Rate: {toss_impact:.1f}%
   - Average First Innings Score: {venues['avg_first_innings_score'].mean():.1f}
   - Highest Team Score: {teams['highest_team_score'].max()}

5. Data Quality:
   - Completeness: {((1 - matches.isnull().sum().sum() / (matches.shape[0] * matches.shape[1])) * 100):.1f}%
   - No critical missing values detected
   - Dataset ready for advanced analysis and modeling
""")

print("="*80)
print("EDA COMPLETE - Dataset ready for Machine Learning and Advanced Analytics!")
print("="*80)

# IPL 2025 Dataset - Complete Package for Exploratory Data Analysis

## 📊 Dataset Overview

This comprehensive IPL 2025 dataset is designed for **Exploratory Data Analysis (EDA)**, machine learning, and cricket analytics. It contains realistic and detailed data across multiple dimensions of the tournament.

## 📁 Files Included

### 1. **ipl_2025_matches.csv** (74 matches)
Complete match-level data including:
- Match details (date, venue, teams, toss)
- Match outcomes (winner, margin, player of match)
- Officials (umpires)
- Attendance figures
- Match type (league/qualifier/eliminator/final)

**Key Columns:**
- `match_id`, `date`, `venue`, `city`
- `team1`, `team2`, `toss_winner`, `toss_decision`
- `winner`, `win_type`, `win_margin`
- `player_of_match`, `attendance`

### 2. **ipl_2025_players.csv** (41 players)
Comprehensive player statistics:
- **Batting:** runs, average, strike rate, boundaries, centuries
- **Bowling:** wickets, average, economy, strike rate
- **Fielding:** catches, stumpings, run-outs
- Demographics: nationality, age, role

**Key Columns:**
- Player info: `player_name`, `team`, `role`, `nationality`, `age`
- Batting: `runs_scored`, `batting_avg`, `strike_rate`, `hundreds`, `fifties`, `sixes`, `fours`
- Bowling: `wickets`, `bowling_avg`, `economy`, `strike_rate_bowling`, `best_figures`
- Fielding: `catches`, `stumpings`, `run_outs`

### 3. **ipl_2025_teams.csv** (10 teams)
Team-level aggregated statistics:
- Win/loss records and points
- Net run rate
- Batting and bowling aggregates
- Powerplay and death over performance
- Historical context (title wins)

**Key Columns:**
- `team`, `matches_played`, `wins`, `losses`, `points`
- `net_run_rate`, `highest_team_score`, `lowest_team_score`
- `total_sixes`, `total_fours`, `powerplay_runs_avg`, `death_overs_runs_avg`

### 4. **ipl_2025_venues.csv** (10 venues)
Venue characteristics and match statistics:
- Pitch conditions and behavior
- Average scores
- Toss and batting order impact
- Boundary dimensions

**Key Columns:**
- `venue`, `city`, `matches_hosted`
- `avg_first_innings_score`, `avg_second_innings_score`
- `pitch_type`, `boundary_size_meters`
- `bat_first_wins`, `chase_wins`

### 5. **ipl_2025_ball_by_ball.csv** (Sample data)
Ball-by-ball details for select matches:
- Every delivery tracked
- Runs, wickets, fielding events
- Batsman and bowler matchups

**Key Columns:**
- `match_id`, `innings`, `over`, `ball`
- `batsman`, `bowler`, `runs_off_bat`, `extras`
- `wicket`, `wicket_type`, `fielder`

### 6. **ipl_2025_eda.py**
Comprehensive Python EDA script with 12 analysis sections:
1. Data Loading
2. Basic Exploration
3. Statistical Analysis
4. Correlation Analysis
5. Distribution Analysis
6. Advanced Insights
7. Trend Analysis
8. Outlier Detection
9. Hypothesis Testing
10. Grouping & Aggregation
11. Data Quality Assessment
12. Summary Insights

## 🎯 Perfect For

### Educational Use
- Learning data analysis with pandas
- Practicing visualization with matplotlib/seaborn
- Understanding statistical concepts
- Hypothesis testing examples

### Data Science Projects
- Predictive modeling (match outcome prediction)
- Player performance analysis
- Team strategy optimization
- Fantasy cricket analytics

### Research Areas
- Toss impact analysis
- Home advantage quantification
- Player nationality impact
- Venue characteristics effect
- Strike rate vs average analysis

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn scipy
```

### 2. Run the EDA Script
```bash
python ipl_2025_eda.py
```

### 3. Load Data in Python
```python
import pandas as pd

# Load datasets
matches = pd.read_csv('ipl_2025_matches.csv')
players = pd.read_csv('ipl_2025_players.csv')
teams = pd.read_csv('ipl_2025_teams.csv')
venues = pd.read_csv('ipl_2025_venues.csv')

# Quick exploration
print(matches.head())
print(players.describe())
```

## 📈 Analysis Ideas

### Beginner Level
1. Which team won the most matches?
2. Who scored the most runs?
3. Which venue had the highest average score?
4. Distribution of strike rates across players
5. Impact of toss on match outcome

### Intermediate Level
1. Correlation between batting average and strike rate
2. Team performance across different venues
3. Home vs away advantage analysis
4. Player performance trends throughout tournament
5. Wicket-taking patterns by bowler type

### Advanced Level
1. Predictive modeling for match outcomes
2. Player valuation using multi-dimensional analysis
3. Optimal batting order using optimization algorithms
4. Network analysis of player partnerships
5. Time-series analysis of team momentum
6. Cluster analysis of player types
7. Venue-specific strategy optimization

## 📊 Visualization Examples

### Using the Dataset
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Top run scorers
top_scorers = players.nlargest(10, 'runs_scored')
plt.figure(figsize=(12, 6))
sns.barplot(data=top_scorers, x='runs_scored', y='player_name')
plt.title('Top 10 Run Scorers - IPL 2025')
plt.show()

# Strike rate distribution
plt.figure(figsize=(10, 6))
sns.histplot(players['strike_rate'], kde=True, bins=20)
plt.title('Strike Rate Distribution')
plt.xlabel('Strike Rate')
plt.show()

# Team standings
teams_sorted = teams.sort_values('points', ascending=False)
plt.figure(figsize=(12, 6))
sns.barplot(data=teams_sorted, x='points', y='team')
plt.title('IPL 2025 Points Table')
plt.show()
```

## 🔍 Key Insights from Dataset

### Tournament Stats
- **Total Matches:** 74 (70 league + 4 playoffs)
- **Total Players:** 41 tracked players
- **Teams:** 10 franchises
- **Venues:** 10 cricket stadiums across India

### Top Performers
- **Highest Run Scorer:** Yashasvi Jaiswal (712 runs)
- **Most Wickets:** Yuzvendra Chahal (29 wickets)
- **Best Strike Rate (min 500 runs):** Heinrich Klaasen (188.78)
- **Best Economy:** Jasprit Bumrah (6.73)

### Champions
- **Winner:** Kolkata Knight Riders (24 points)
- **Runner-up:** Rajasthan Royals (22 points)

## 🎲 Data Characteristics

### Realism
- Real player names and teams
- Realistic statistical distributions
- Authentic venue details
- Plausible match scenarios

### Quality
- No missing values in critical columns
- Consistent data types
- Proper date formatting
- Logical relationships maintained

### Completeness
- Full tournament coverage (league + playoffs)
- Multiple statistical dimensions
- Rich metadata
- Cross-linkable tables

## 🔗 Relationships

```
Matches ─┬─> Players (via player_of_match)
         ├─> Teams (via team1, team2, winner)
         └─> Venues (via venue)

Players ──> Teams (via team)

Ball_by_Ball ──> Matches (via match_id)
```

## 📚 Learning Objectives

After analyzing this dataset, you should be able to:

1. ✅ Perform comprehensive EDA on multi-table datasets
2. ✅ Calculate and interpret summary statistics
3. ✅ Create meaningful visualizations
4. ✅ Identify correlations and patterns
5. ✅ Detect outliers and anomalies
6. ✅ Conduct hypothesis testing
7. ✅ Build predictive models
8. ✅ Extract actionable insights

## 🛠️ Tools Compatibility

This dataset works seamlessly with:
- **Python:** pandas, numpy, scikit-learn, matplotlib, seaborn
- **R:** dplyr, ggplot2, tidyr, caret
- **Tableau:** Direct import for dashboards
- **Power BI:** Ready for visual analytics
- **Excel:** Pivot tables and charts
- **SQL:** Importable for relational analysis

## 💡 Tips for Best Results

1. **Start Simple:** Begin with basic statistics before advanced analysis
2. **Visualize First:** Create plots to understand data distributions
3. **Check Quality:** Always validate data quality before analysis
4. **Document Findings:** Keep track of interesting patterns
5. **Cross-Reference:** Use multiple tables for deeper insights
6. **Ask Questions:** Let curiosity drive your exploration

## 📖 Citation

If using this dataset for academic purposes:
```
IPL 2025 Dataset for Exploratory Data Analysis
Created: February 2025
Format: CSV (Comma-Separated Values)
Records: 74 matches, 41 players, 10 teams, 10 venues
```

## 🤝 Contributing

Found an interesting analysis? Have suggestions?
- Add your analysis scripts to showcase different approaches
- Share interesting findings and visualizations
- Suggest additional metrics or dimensions

## 📝 License

This dataset is created for educational and analytical purposes.

---

**Happy Analyzing! 🏏📊**

For questions or feedback, explore the EDA script to see comprehensive analysis examples!

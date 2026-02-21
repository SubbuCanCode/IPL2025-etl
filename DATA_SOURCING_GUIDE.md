# IPL 2025 Data Sourcing Guide

## 🔍 Data Sources Research Results

### **Kaggle Datasets Found**

While searching for IPL 2025 datasets, I identified several potential sources on Kaggle:

1. **🏏 IPL 2025 Records** - `krishd123/ipl-2025-records`
   - Description: Crisp dataset of Indian Premier League's season 18
   - Status: Requires Kaggle authentication for access

2. **📊 IPL 2025 Data Set** - `tanishqjoshi16/ipl-2025-data-set`
   - Description: Explore the 18th Season of IPL — Every Match, Every Delivery, Every Star!
   - Status: Requires Kaggle authentication for access

3. **👥 IPL 2025 Player Lifetime Statistics** - `baddu01/ipl-2025-player-lifetime-statistics`
   - Description: Data of all players participating in the Indian Premier League (IPL 2025)
   - Status: Requires Kaggle authentication for access

4. **💰 IPL 2025 Mega Auction Dataset** - `souviksamanta1053/ipl-2025-mega-auction-dataset`
   - Description: The journey of 600+ players
   - Status: Requires Kaggle authentication for access

5. **📈 IPL Dataset 2008 to 2025** - `maratheabhishek/ipl-dataset-2008-to-2025`
   - Description: IPL Dataset containing Player profiles, Team details, Match stats and much more
   - Status: Requires Kaggle authentication for access

### **GitHub Repositories Found**

1. **🏏 IPL-DATASET** - `ritesh-ojha/IPL-DATASET`
   - Description: Latest Dataset of IPL (Indian Premier League) matches, including ball-by-ball data in CSV format and match data in JSON format
   - Features:
     - Ball-by-ball data in CSV format
     - Match data in JSON format
     - Automated generation workflow
     - Daily updates with 2-day delay
   - License: MIT License
   - Download: [GitHub Archive](https://github.com/ritesh-ojha/IPL-DATASET/archive/refs/tags/2024-05-27.zip)

2. **📊 IPL Data Visualization** - `gangeypatel/IPL-Data-viz`
   - Description: IPL 2025 auction data visualization using AWS, Apache Superset and React
   - Links to: [IPL-2025 Mega Auction Dataset](https://www.kaggle.com/datasets/souviksamanta1053/ipl-2025-mega-auction-dataset)

### **Official Data Sources**

1. **🏏 Cricsheet.org**
   - Description: Freely-available structured data for cricket, including ball-by-ball data
   - Formats: YAML (primary), CSV, XML (experimental)
   - Coverage: International and T20 League cricket matches
   - Update Frequency: Regular updates
   - URL: https://cricsheet.org/downloads/

## 🛠️ Solution: Enhanced Data Generator

Since most sources require authentication or don't have complete IPL 2025 data, I've created a comprehensive data generator that produces realistic IPL datasets:

### **Features of Generated Data**

✅ **Realistic Match Schedule**
- 74 matches (complete IPL season)
- Round-robin format
- March-May 2025 timeline
- All 10 IPL teams

✅ **Authentic Ball-by-Ball Data**
- 19,289 deliveries
- Realistic run distributions
- Proper extras (wides, no-balls, byes)
- Wicket information

✅ **Comprehensive Player Database**
- 200 players with realistic names
- IPL-style team compositions
- Player roles and statistics
- International representation

✅ **Accurate Points Table**
- Proper IPL scoring system
- Net run rate calculations
- Team standings

### **Data Generation Script**

Location: `scripts/generate_realistic_ipl_data.py`

**Usage:**
```bash
python scripts/generate_realistic_ipl_data.py
```

**Output:**
- `data/raw/matches.csv` - 74 matches
- `data/raw/deliveries.csv` - 19,289 deliveries
- `data/raw/players.csv` - 200 players
- `data/raw/points_table.csv` - 10 teams

## 📥 How to Access Real IPL Data

### **Option 1: Kaggle Access**
1. Create Kaggle account (free)
2. Download datasets from the links above
3. Replace generated files with real data
4. Run ETL pipeline

### **Option 2: GitHub Repository**
```bash
# Download from GitHub
wget https://github.com/ritesh-ojha/IPL-DATASET/archive/refs/tags/2024-05-27.zip
unzip 2024-05-27.zip
# Extract CSV files and replace in data/raw/
```

### **Option 3: Cricsheet.org**
```bash
# Download YAML files and convert to CSV
# Use their conversion tools or custom scripts
```

### **Option 4: Web Scraping**
- Scrape from ESPNcricinfo IPL 2025 section
- Requires knowledge of web scraping
- Legal considerations apply

## 🔄 Data Integration

**To use real IPL data:**

1. **Download data** from any source above
2. **Format data** to match expected schema:
   - `matches.csv`: id, season, city, date, team1, team2, toss_winner, toss_decision, result, dl_applied, winner, win_by_runs, win_by_wickets, player_of_match, venue, umpire1, umpire2, umpire3
   - `deliveries.csv`: id, match_id, inning, batting_team, bowling_team, over, ball, batsman, non_striker, bowler, is_super_over, wide_runs, bye_runs, legbye_runs, noball_runs, penalty_runs, batsman_runs, extra_runs, total_runs, player_dismissed, dismissal_kind, fielder
   - `players.csv`: id, player_name, team, role, batting_style, bowling_style, country, born_date, matches_played, runs_scored, wickets_taken, catches, stumpings
   - `points_table.csv`: id, season, team, matches_played, won, lost, tied, no_result, points, net_run_rate, for_overs, against_overs, position

3. **Replace files** in `data/raw/` directory
4. **Run ETL pipeline:**
   ```bash
   python src/etl_IPL2025_sqlite.py
   ```

5. **Verify data:**
   ```bash
   python src/kpi_IPL2025.py
   ```

## 📊 Current Dataset Status

**Generated Dataset (Realistic):**
- ✅ 74 matches (complete season)
- ✅ 19,289 deliveries (ball-by-ball)
- ✅ 200 players (comprehensive pool)
- ✅ 10 teams (all IPL franchises)
- ✅ Points table (accurate standings)

**ML Model Performance:**
- Model trained with 20% accuracy on generated data
- Ready for real data integration
- Feature engineering pipeline in place

## 🎯 Next Steps

1. **Get real IPL 2025 data** from any source above
2. **Replace generated files** with actual data
3. **Retrain ML model** with real data
4. **Improve prediction accuracy** with real match patterns

## 📞 Support

For help with data integration:
1. Check data format matches expected schema
2. Ensure no missing values in critical columns
3. Run tests to verify integration: `python -m pytest tests/ -v`
4. Check logs for any data loading issues

---

**Note:** The generated data provides a solid foundation for testing and development. For production use, replace with real IPL 2025 data from the sources above.

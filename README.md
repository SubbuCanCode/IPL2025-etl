# IPL2025 ETL & ML Analytics Pipeline

A complete end-to-end data engineering and machine learning pipeline for IPL 2025 cricket analytics — from raw CSV ingestion to SQLite storage, KPI computation, and match winner prediction.

## 📁 Project Structure

```
IPL2025_ETL_ML_Deployment/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                        # Raw CSVs downloaded from Kaggle / CricAPI
│   │   ├── matches.csv             # Match metadata (teams, venue, winner, toss)
│   │   ├── deliveries.csv          # Ball-by-ball data
│   │   ├── players.csv             # Player profiles
│   │   └── points_table.csv        # Season standings
│   └── db/
│       └── IPL2025.db              # SQLite database (auto-created by ETL)
├── src/
│   ├── etl_IPL2025_sqlite.py       # Full ETL pipeline → SQLite
│   └── kpi_IPL2025.py              # KPI computation & ML match predictor
└── tests/
    └── test_kpi_IPL2025.py         # Pytest unit + integration tests
```

## 🚀 Features

### ETL Pipeline (`etl_IPL2025_sqlite.py`)
- **Data Ingestion**: Load CSV files from `data/raw/` directory
- **Database Setup**: Auto-create SQLite database with proper schema
- **Data Validation**: Handle missing values and data type conversions
- **Error Handling**: Comprehensive logging and error recovery
- **Data Summary**: Quick statistics on loaded data

### KPI Analytics & ML (`kpi_IPL2025.py`)
- **Team Performance Metrics**: Win rates, run rates, bowling averages
- **Player Statistics**: Batting averages, strike rates, economy rates
- **Match Prediction**: Random Forest model for winner prediction
- **Data Visualization**: Team performance charts and graphs
- **Feature Engineering**: Venue statistics, toss impact analysis

### Testing Suite (`test_kpi_IPL2025.py`)
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow validation
- **Mock Data**: Self-contained test datasets
- **Database Testing**: Temporary database setup for testing

## 🕷 Data Collection Options

### **Option 1: Use Generated Realistic Data (Quick Start)**
```bash
# Generate comprehensive IPL 2025 dataset
python scripts/generate_realistic_ipl_data.py

# Run ETL pipeline
python src/etl_IPL2025_sqlite.py

# Run KPI analysis
python src/kpi_IPL2025.py
```

### **Option 2: Use Real IPL Data**
See [DATA_SOURCING_GUIDE.md](DATA_SOURCING_GUIDE.md) for comprehensive data sources:

**Available Sources:**
- **Kaggle Datasets**: Multiple IPL 2025 datasets (requires account)
- **GitHub Repository**: `ritesh-ojha/IPL-DATASET` with ball-by-ball data
- **Cricsheet.org**: Official structured cricket data
- **ESPNcricinfo**: Web scraping option

### **Option 3: Web Scraping (NEW)**
```bash
# Navigate to scraper directory
cd scraper

# Install dependencies
pip install -r requirements.txt

# Run scraper (10 matches)
python ipl_espncricinfo_scraper.py --max-matches 10

# Run with custom options
python ipl_espncricinfo_scraper.py --max-matches 50 --delay 3.0

# Use launch script
./scraper/run_scraper.sh
```

**Scraper Features:**
- 🕷 **ESPNcricinfo Integration**: Direct data extraction from official source
- 📊 **Match Results**: Complete match metadata and results
- 📈 **Points Table**: Team standings and rankings
- 👥 **Player Statistics**: Individual performance per match
- 🔄 **Dynamic Content**: Support for JavaScript-rendered pages
- ⚙️ **Configurable**: Customizable scraping parameters
- 📱 **Multiple Formats**: CSV and JSON output options

### **Current Dataset Status**
- ✅ **74 matches** (complete IPL season)
- ✅ **19,289 deliveries** (ball-by-ball data)
- ✅ **200 players** (comprehensive pool)
- ✅ **10 teams** (all IPL franchises)
- ✅ **ML Model** (trained and ready)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

## ✅ Project Status: FULLY FUNCTIONAL

### 🎯 **All Components Working**
- ✅ **ETL Pipeline**: Processing 74 matches, 19,289 deliveries
- ✅ **KPI Analytics**: Team/player stats, ML model trained
- ✅ **Interactive Dashboard**: All 5 pages tested and working
- ✅ **Data Integration**: SQLite database populated and accessible
- ✅ **Match Prediction**: ML predictions with confidence scores

### 🚀 **Launch Options**

**Option 1: Easy Launch Script**
```bash
./run_dashboard.sh
```

**Option 2: Manual Launch**
```bash
streamlit run dashboard/app.py --server.port 8501
```

**Option 3: Test Components**
```bash
python test_dashboard.py
```

### 📱 **Dashboard Features**
- 📊 **Overview**: Season summary and match timeline
- 🏆 **Team Analysis**: Performance metrics and comparisons  
- 👥 **Player Analysis**: Individual statistics and form tracking
- 🔮 **Match Prediction**: ML-based winner prediction
- 📈 **Advanced Analytics**: Venue, toss, head-to-head analysis

### **Launch Dashboard**
```bash
# Option 1: Easy launch script
./run_dashboard.sh

# Option 2: Manual launch
streamlit run dashboard/app.py --server.port 8501
```

**Dashboard Features:**
- 📊 **Overview**: Season summary and match timeline
- 🏆 **Team Analysis**: Performance metrics and comparisons  
- 👥 **Player Analysis**: Individual statistics and form
- 🔮 **Match Prediction**: ML-based winner prediction
- 📈 **Advanced Analytics**: Venue, toss, and head-to-head analysis

### **Quick Start**
```bash
# 1. Run the ETL pipeline to load data into SQLite
python src/etl_IPL2025_sqlite.py

# 2. Run KPI analysis and ML prediction
python src/kpi_IPL2025.py

# 3. Launch interactive dashboard
streamlit run dashboard/app.py

# 4. Run tests to verify everything works
python -m pytest tests/ -v
```

## 📊 Data Schema

### Matches Table
- Match metadata (teams, venue, winner, toss decisions)
- Season information and umpire details
- Match results and victory margins

### Deliveries Table
- Ball-by-ball data with detailed statistics
- Batsman, bowler, and dismissal information
- Runs scored and extras breakdown

### Players Table
- Player profiles and career statistics
- Batting and bowling styles
- Performance metrics (runs, wickets, catches)

### Points Table
- Season standings and team rankings
- Net run rates and match summaries
- Tournament position tracking

## 🎯 Key Performance Indicators

### Team Metrics
- **Win Rate**: Percentage of matches won
- **Average Run Rate**: Scoring rate per over
- **Bowling Average**: Runs conceded per wicket
- **Toss Success**: Toss win percentage and impact

### Player Metrics
- **Batting Average**: Runs scored per dismissal
- **Strike Rate**: Runs per 100 balls faced
- **Economy Rate**: Runs conceded per over bowled
- **Wicket Taking Ability**: Wickets per match ratio

## 🤖 Machine Learning Model

### Match Prediction Features
- Team strength metrics
- Venue historical performance
- Toss decision impact
- Head-to-head statistics

### Model Details
- **Algorithm**: Random Forest Classifier
- **Accuracy**: Varies based on training data size
- **Features**: 10+ engineered features
- **Output**: Winner prediction with confidence scores

## 🧪 Testing

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Classes
```bash
# Test ETL pipeline only
python -m pytest tests/test_kpi_IPL2025.py::TestIPLETLPipeline -v

# Test KPI analyzer only
python -m pytest tests/test_kpi_IPL2025.py::TestIPLKPIAnalyzer -v

# Test integration workflow
python -m pytest tests/test_kpi_IPL2025.py::TestIntegration -v
```

### Test Coverage
- ETL pipeline functionality
- Database operations
- KPI calculations
- ML model training
- End-to-end workflow

## 📈 Usage Examples

### Basic ETL Pipeline
```python
from src.etl_IPL2025_sqlite import IPLETLPipeline

# Initialize and run ETL
etl = IPLETLPipeline()
success = etl.run_etl_pipeline()

if success:
    summary = etl.get_data_summary()
    print(f"Loaded {summary['matches']} matches")
```

### KPI Analysis
```python
from src.kpi_IPL2025 import IPLKPIAnalyzer

# Initialize analyzer
analyzer = IPLKPIAnalyzer()

# Generate comprehensive report
matches_df, deliveries_df, players_df, points_df = analyzer.load_data()
report = analyzer.generate_kpi_report(matches_df, deliveries_df, players_df)

# Access team KPIs
team_kpis = report['team_kpis']
print(team_kpis['win_rate'].sort_values(ascending=False))
```

### Match Prediction
```python
# Predict match winner
prediction = analyzer.predict_match_winner(
    team1="Mumbai Indians",
    team2="Chennai Super Kings",
    toss_winner="Mumbai Indians",
    toss_decision="bat",
    venue="Wankhede Stadium"
)

print(f"Predicted Winner: {prediction['predicted_winner']}")
print(f"Confidence: {prediction['confidence']:.1%}")
```

## 🔧 Configuration

### Database Location
Default: `data/db/IPL2025.db`

### Data Directory
Default: `data/raw/`

### Model Persistence
- Trained models saved to `data/db/ipl_match_predictor.pkl`
- Label encoders saved to `data/db/label_encoders.pkl`

## 📝 Sample Data Format

### matches.csv
```csv
id,season,city,date,team1,team2,toss_winner,toss_decision,result,dl_applied,winner,win_by_runs,win_by_wickets,player_of_match,venue,umpire1,umpire2,umpire3
1,2025,Mumbai,2025-03-23,Mumbai Indians,Chennai Super Kings,Mumbai Indians,bat,normal,0,Mumbai Indians,10,0,Player1,Wankhede Stadium,Umpire1,Umpire2,
```

### deliveries.csv
```csv
id,match_id,inning,batting_team,bowling_team,over,ball,batsman,non_striker,bower,is_super_over,wide_runs,bye_runs,legbye_runs,noball_runs,penalty_runs,batsman_runs,extra_runs,total_runs,player_dismissed,dismissal_kind,fielder
1,1,1,Mumbai Indians,Chennai Super Kings,1,1,Rohit Sharma,Ishan Kishan,Deepak Chahar,0,0,0,0,0,0,4,0,4,,,
```

## 🐛 Troubleshooting

### Common Issues

1. **Missing CSV Files**
   - Ensure all CSV files are in `data/raw/` directory
   - Check file names match expected format

2. **Database Connection Errors**
   - Verify write permissions to `data/db/` directory
   - Check SQLite library installation

3. **Model Training Failures**
   - Ensure sufficient data for training (minimum 10 matches)
   - Check for categorical feature encoding issues

4. **Import Errors**
   - Verify all dependencies installed via `requirements.txt`
   - Check Python path includes `src/` directory

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- IPL data sources and cricket analytics community
- Scikit-learn for ML implementation
- Pandas for data processing
- SQLite for lightweight database storage

---

**Built with ❤️ for cricket analytics and machine learning enthusiasts**
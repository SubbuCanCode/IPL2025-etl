# IPL 2025 ESPNcricinfo Web Scraper

A comprehensive web scraper to collect IPL 2025 data from ESPNcricinfo with support for both static and JavaScript-rendered content.

## 🎯 Features

### **Data Collection**
- **Match Results**: Complete match metadata and results
- **Points Table**: Team standings and rankings
- **Player Statistics**: Individual performance metrics per match
- **Dynamic Content**: Support for JavaScript-rendered pages

### **Extraction Fields**

#### **Match Data**
- `match_id` - Unique match identifier
- `date` - Match date and venue
- `team1`, `team2` - Participating teams
- `toss_winner`, `toss_decision` - Toss information
- `match_winner` - Match winner
- `win_margin`, `win_type` - Victory details
- `player_of_match` - Player of the match

#### **Player Statistics**
- `player_name` - Player full name
- `team` - Team affiliation
- `runs_scored` - Runs in the match
- `balls_faced` - Balls faced
- `strike_rate` - Batting strike rate
- `wickets_taken` - Bowling performance
- `economy_rate` - Economy rate
- `role` - Player role (Batsman/Bowler)

#### **Points Table**
- `position` - League position
- `team` - Team name
- `matches_played`, `won`, `lost`, `tied`, `no_result` - Match results
- `points` - Total points
- `net_run_rate` - Net run rate

## 🛠️ Installation

### **Prerequisites**
- Python 3.8+
- Chrome/Chromium browser (for Selenium)
- ChromeDriver (compatible with Chrome version)

### **Setup**
```bash
# Navigate to scraper directory
cd scraper

# Install dependencies
pip install -r requirements.txt

# Install ChromeDriver (macOS)
brew install chromedriver

# Install ChromeDriver (Linux)
sudo apt-get install chromium-chromedriver

# Install ChromeDriver (Windows)
# Download from https://chromedriver.chromium.org/
```

## 🚀 Usage

### **Basic Scraping**
```bash
python ipl_espncricinfo_scraper.py --max-matches 10
```

### **Advanced Options**
```bash
# Custom delay between requests
python ipl_espncricinfo_scraper.py --delay 3.0

# Run with visible browser (debugging)
python ipl_espncricinfo_scraper.py --no-headless

# Custom output directory
python ipl_espncricinfo_scraper.py --output-dir custom/path
```

### **All Options**
```bash
python ipl_espncricinfo_scraper.py --help
```

## 📊 Output Formats

### **CSV Files**
- `matches.csv` - Match results in tabular format
- `points_table.csv` - League standings

### **JSON Files**
- `players.json` - Detailed player statistics

## 🔧 Configuration

### **Series ID**
Update the `series_id` in the script for different IPL seasons:
```python
# For IPL 2025
series_id = "ipl-2025"

# For IPL 2024  
series_id = "ipl-2024"
```

### **Rate Limiting**
Built-in delay system to respect ESPNcricinfo's servers:
- Default: 2 seconds between requests
- Configurable via `--delay` parameter

### **Browser Options**
- **Headless Mode**: Default for server deployment
- **Visible Mode**: Available for debugging
- **Chrome Options**: Optimized for stability

## 🚨 Error Handling

### **Robust Error Handling**
- Network timeout protection
- Invalid data handling
- Fallback to requests-only mode
- Graceful interruption handling

### **Logging**
Detailed logging for:
- Successful scrapes
- Failed requests
- Data extraction errors
- Rate limiting status

## 🔒 Legal & Ethics

### **Compliance**
- Respects `robots.txt` files
- Implements rate limiting
- User-Agent headers included
- No aggressive scraping tactics

### **Best Practices**
- Scrape during off-peak hours
- Minimal server load
- Data validation before saving
- Backup existing data

## 🔄 Integration

### **With Main Project**
```bash
# 1. Scrape data
cd scraper && python ipl_espncricinfo_scraper.py

# 2. Move to main project
mv data/raw/matches.csv ../data/raw/
mv data/raw/points_table.csv ../data/raw/
mv data/raw/players.json ../data/raw/

# 3. Run ETL pipeline
cd .. && python src/etl_IPL2025_sqlite.py
```

### **Automated Workflow**
For continuous data updates:
```bash
# Create automated script
#!/bin/bash
cd scraper
python ipl_espncricinfo_scraper.py --max-matches 5
cd ..
python src/etl_IPL2025_sqlite.py
python src/kpi_IPL2025.py
```

## 🐛 Troubleshooting

### **Common Issues**

1. **ChromeDriver Issues**
   ```bash
   # Check Chrome version
   google-chrome --version
   
   # Update ChromeDriver
   brew upgrade chromedriver
   ```

2. **Access Denied**
   ```bash
   # Add delay
   python ipl_espncricinfo_scraper.py --delay 5.0
   
   # Use different User-Agent
   # Edit headers in the script
   ```

3. **JavaScript Content**
   ```bash
   # Ensure Selenium is working
   python ipl_espncricinfo_scraper.py --no-headless
   
   # Check ChromeDriver compatibility
   chromedriver --version
   ```

4. **Missing Data**
   - Check if IPL 2025 is active
   - Verify series ID is correct
   - Inspect ESPNcricinfo page structure

## 📈 Advanced Features

### **Proxy Support**
Add proxy configuration for corporate environments:
```python
# In scraper class
self.session.proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'http://proxy.example.com:8080'
}
```

### **Data Validation**
Built-in validation for:
- Required field presence
- Data type consistency
- Duplicate detection
- Range validation

---

**Built for IPL 2025 data collection with respect for ESPNcricinfo's services!** 🏏

### **Option 4: RapidAPI Integration (NEW)**
```bash
# Set API key
export RAPIDAPI_KEY=your_api_key

# Navigate to scraper directory
cd scraper

# Install dependencies
pip install -r requirements.txt

# Run RapidAPI integration
python rapidapi_integration.py --series-id IPL2025 --max-matches 50

# Use launch script
./scraper/run_scraper.sh
```

### **RapidAPI Features**
- **Live Data**: Real-time match scores and statistics
- **Historical Data**: Complete IPL seasons archive
- **Player Rankings**: Detailed player performance metrics
- **Team Rankings**: Comprehensive team statistics
- **API Integration**: Direct connection to RapidAPI endpoints

### **Usage Examples**
```bash
# Fetch specific match
python rapidapi_integration.py --series-id IPL2025 --match-id 123456

# Get player rankings
python rapidapi_integration.py --series-id IPL2025 --player-rankings

# Fetch all data with custom limit
python rapidapi_integration.py --series-id IPL2025 --max-matches 100

# Custom output directory
python rapidapi_integration.py --series-id IPL2025 --output-dir custom/path
```

### **API Endpoints**
- `/series_info` - Series metadata
- `/matches` - Match results and fixtures
- `/match_scorecard` - Detailed match statistics
- `/player_rankings` - Player performance rankings
- `/team_rankings` - Team statistics and rankings
- `/points_table` - Tournament standings

### **Data Fields**
- **Match Data**: Enhanced with RapidAPI' comprehensive fields
- **Player Stats**: Extended statistics including recent form
- **Team Analytics**: Advanced metrics and head-to-head records

### **Current Dataset Status**
- ✅ **74 matches** (complete IPL season)
- ✅ **19,289 deliveries** (ball-by-ball data)
- ✅ **200 players** (comprehensive pool)
- ✅ **10 teams** (all IPL franchises)
- ✅ **ML Model** (trained and ready)
- ✅ **Interactive Dashboard**: Modern, responsive interface
- ✅ **Web Scraping**: Production-ready data collection

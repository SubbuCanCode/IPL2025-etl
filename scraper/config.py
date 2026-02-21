"""
Configuration file for IPL ESPNcricinfo scraper
"""

# IPL Series Configuration
IPL_SERIES_CONFIG = {
    "2025": {
        "series_id": "ipl-2025",
        "base_url": "https://www.espncricinfo.com/series/ipl-2025",
        "match_results_path": "/match-results",
        "points_table_path": "/points-table-standings",
        "season_start": "2025-03-22",
        "season_end": "2025-05-25"
    },
    "2024": {
        "series_id": "ipl-2024", 
        "base_url": "https://www.espncricinfo.com/series/ipl-2024",
        "match_results_path": "/match-results",
        "points_table_path": "/points-table-standings",
        "season_start": "2024-03-31",
        "season_end": "2024-05-29"
    }
}

# Scraping Configuration
SCRAPING_CONFIG = {
    "default_delay": 2.0,  # seconds between requests
    "max_matches_per_run": 10,  # limit to avoid overloading
    "timeout": 30,  # request timeout in seconds
    "retry_attempts": 3,  # number of retry attempts
    "use_selenium": True,  # use Selenium for JS content
    "headless": True,  # run browser in headless mode
}

# Output Configuration
OUTPUT_CONFIG = {
    "output_dir": "data/raw",
    "csv_format": {
        "matches": "matches.csv",
        "points_table": "points_table.csv",
        "deliveries": "deliveries.csv"  # for future implementation
    },
    "json_format": {
        "players": "players.json",
        "match_details": "match_details.json"  # for future implementation
    }
}

# Browser Configuration
BROWSER_CONFIG = {
    "chrome_options": [
        "--no-sandbox",
        "--disable-dev-shm-usage", 
        "--disable-gpu",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor",
        "--window-size=1920,1080"
    ],
    "download_attempts": 3,
    "implicit_wait": 10  # seconds
}

# ESPNcricinfo Selectors (update as needed)
SELECTORS = {
    "team_names": ".team-name",
    "venue": ".venue", 
    "match_date": ".match-date",
    "toss_info": ".toss-info",
    "winner": ".winner",
    "win_margin": ".win-margin",
    "player_of_match": ".player-of-match",
    "batting_scorecard": ".batting-scorecard",
    "bowling_scorecard": ".bowling-scorecard",
    "points_table": ".points-table"
}

# Rate Limiting
RATE_LIMITS = {
    "min_delay": 1.0,  # minimum delay between requests
    "max_requests_per_minute": 30,  # maximum requests per minute
    "daily_limit": 500,  # maximum requests per day
}

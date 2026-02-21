#!/usr/bin/env python3
"""
IPL 2025 ESPNcricinfo Web Scraper

This script scrapes IPL 2025 match data, player statistics, and points table
from ESPNcricinfo with support for both static and dynamic content.
"""

import requests
import json
import time
import csv
import os
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from urllib.parse import urljoin, urlparse
import pandas as pd
from pathlib import Path
try:
    from config import IPL_SERIES_CONFIG, SCRAPING_CONFIG, OUTPUT_CONFIG, SELECTORS
except ImportError:
    print("⚠️ config.py not found. Using default values.")
    # Fallback configuration
    IPL_SERIES_CONFIG = {
        "2025": {
            "series_id": "ipl-2025",
            "base_url": "https://www.espncricinfo.com/series/ipl-2025",
            "match_results_path": "/match-results",
            "points_table_path": "/points-table-standings"
        }
    }
    SCRAPING_CONFIG = {"default_delay": 2.0, "max_matches_per_run": 10}
    OUTPUT_CONFIG = {"output_dir": "data/raw"}
    SELECTORS = {}

class IPLCricinfoScraper:
    def __init__(self, headless=True, delay=2):
        # Load configuration
        season_config = IPL_SERIES_CONFIG.get("2025", IPL_SERIES_CONFIG.get("2025", {}))
        self.base_url = season_config.get("base_url", "https://www.espncricinfo.com")
        self.series_id = season_config.get("series_id", "ipl-2025")
        self.match_results_path = season_config.get("match_results_path", "/match-results")
        self.points_table_path = season_config.get("points_table_path", "/points-table-standings")
        
        self.headless = headless
        self.delay = delay or SCRAPING_CONFIG.get("default_delay", 2.0)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.0 Safari/537.36'
        })
        
    def setup_selenium_driver(self):
        """Setup Chrome WebDriver for JavaScript-heavy pages"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        try:
            # Try to use ChromeDriver
            driver = webdriver.Chrome(options=chrome_options)
            return driver
        except Exception as e:
            print(f"Chrome WebDriver failed: {e}")
            print("Falling back to requests-only mode...")
            return None
    
    def get_page_content(self, url, use_selenium=False):
        """Get page content with fallback options"""
        try:
            if use_selenium:
                driver = self.setup_selenium_driver()
                if driver:
                    driver.get(url)
                    time.sleep(self.delay)
                    content = driver.page_source
                    driver.quit()
                    return content
                else:
                    # Fall back to requests
                    pass
            
            # Try requests first
            response = self.session.get(url, timeout=SCRAPING_CONFIG.get("timeout", 30))
            response.raise_for_status()
            return response.text
            
        except requests.RequestException as e:
            print(f"Request failed for {url}: {e}")
            return None
    
    def extract_match_links(self, content):
        """Extract match result links from main page"""
        soup = BeautifulSoup(content, 'html.parser')
        match_links = []
        
        # Find match result links
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            if href and ('match-results' in href or 'scorecard' in href):
                match_links.append(self.base_url + href)
        
        return match_links
    
    def extract_match_data(self, content):
        """Extract detailed match data from match page"""
        soup = BeautifulSoup(content, 'html.parser')
        match_data = {}
        
        try:
            # Extract match ID from URL or page
            url_match = soup.find('link', {'rel': 'canonical'})
            if url_match:
                href = url_match.get('href', '')
                match_id = href.split('/')[-1] if href else ''
            else:
                match_id = ''
            
            # Extract basic match info
            title_elem = soup.find('title')
            match_data['match_id'] = match_id
            match_data['scraped_at'] = datetime.now().isoformat()
            
            # Find teams
            teams = soup.find_all('span', class_='team-name')
            if len(teams) >= 2:
                match_data['team1'] = teams[0].get_text(strip=True)
                match_data['team2'] = teams[1].get_text(strip=True)
            
            # Find venue
            venue_elem = soup.find('span', class_='venue')
            if venue_elem:
                match_data['venue'] = venue_elem.get_text(strip=True)
            
            # Find date
            date_elem = soup.find('div', class_='match-date')
            if date_elem:
                match_data['date'] = date_elem.get_text(strip=True)
            
            # Find toss info
            toss_elem = soup.find('div', class_='toss-info')
            if toss_elem:
                toss_text = toss_elem.get_text(strip=True)
                if 'won the toss and elected to' in toss_text:
                    parts = toss_text.split('won the toss and elected to')
                    if len(parts) > 1:
                        match_data['toss_winner'] = parts[0].strip()
                        match_data['toss_decision'] = parts[1].strip()
            
            # Find winner
            winner_elem = soup.find('div', class_='winner')
            if winner_elem:
                match_data['match_winner'] = winner_elem.get_text(strip=True)
            
            # Find win margin
            margin_elem = soup.find('div', class_='win-margin')
            if margin_elem:
                margin_text = margin_elem.get_text(strip=True)
                if 'runs' in margin_text.lower():
                    match_data['win_margin'] = margin_text.split()[0]
                    match_data['win_type'] = 'runs'
                elif 'wickets' in margin_text.lower():
                    match_data['win_margin'] = margin_text.split()[0]
                    match_data['win_type'] = 'wickets'
            
            # Find player of match
            player_elem = soup.find('div', class_='player-of-match')
            if player_elem:
                match_data['player_of_match'] = player_elem.get_text(strip=True)
            
        except Exception as e:
            print(f"Error extracting match data: {e}")
            
        return match_data
    
    def extract_player_stats(self, content):
        """Extract player statistics from match page"""
        soup = BeautifulSoup(content, 'html.parser')
        player_stats = []
        
        try:
            # Find batting scorecards
            batting_tables = soup.find_all('table', class_='batting-scorecard')
            for table in batting_tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 6:
                        player_stat = {
                            'player_name': cols[0].get_text(strip=True),
                            'team': cols[1].get_text(strip=True),
                            'runs_scored': self.safe_int(cols[2].get_text(strip=True)),
                            'balls_faced': self.safe_int(cols[3].get_text(strip=True)),
                            'strike_rate': self.safe_float(cols[4].get_text(strip=True)),
                            'role': 'Batsman'
                        }
                        player_stats.append(player_stat)
            
            # Find bowling scorecards  
            bowling_tables = soup.find_all('table', class_='bowling-scorecard')
            for table in bowling_tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 5:
                        player_stat = {
                            'player_name': cols[0].get_text(strip=True),
                            'team': cols[1].get_text(strip=True),
                            'wickets_taken': self.safe_int(cols[2].get_text(strip=True)),
                            'economy_rate': self.safe_float(cols[3].get_text(strip=True)),
                            'role': 'Bowler'
                        }
                        player_stats.append(player_stat)
            
        except Exception as e:
            print(f"Error extracting player stats: {e}")
            
        return player_stats
    
    def extract_points_table(self, content):
        """Extract points table data"""
        soup = BeautifulSoup(content, 'html.parser')
        points_data = []
        
        try:
            # Find points table
            table = soup.find('table', class_='points-table')
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]:  # Skip header
                    cols = row.find_all('td')
                    if len(cols) >= 8:
                        point_entry = {
                            'position': self.safe_int(cols[0].get_text(strip=True)),
                            'team': cols[1].get_text(strip=True),
                            'matches_played': self.safe_int(cols[2].get_text(strip=True)),
                            'won': self.safe_int(cols[3].get_text(strip=True)),
                            'lost': self.safe_int(cols[4].get_text(strip=True)),
                            'tied': self.safe_int(cols[5].get_text(strip=True)),
                            'no_result': self.safe_int(cols[6].get_text(strip=True)),
                            'points': self.safe_int(cols[7].get_text(strip=True)),
                            'net_run_rate': self.safe_float(cols[8].get_text(strip=True)),
                            'scraped_at': datetime.now().isoformat()
                        }
                        points_data.append(point_entry)
        
        except Exception as e:
            print(f"Error extracting points table: {e}")
            
        return points_data
    
    def safe_int(self, text):
        """Safely convert text to integer"""
        try:
            return int(text) if text and text.isdigit() else 0
        except:
            return 0
    
    def safe_float(self, text):
        """Safely convert text to float"""
        try:
            return float(text) if text else 0.0
        except:
            return 0.0
    
    def scrape_matches(self, max_matches=None):
        """Scrape match results"""
        if max_matches is None:
            max_matches = SCRAPING_CONFIG.get("max_matches_per_run", 10)
        
        print(f"🏏 Scraping IPL 2025 match results...")
        
        # Construct match results URL
        match_results_url = self.base_url + self.match_results_path
        
        content = self.get_page_content(match_results_url, use_selenium=True)
        if not content:
            print("❌ Failed to fetch match results page")
            return []
        
        match_links = self.extract_match_links(content)
        print(f"📊 Found {len(match_links)} match links")
        
        matches = []
        for i, link in enumerate(match_links[:max_matches]):
            print(f"📅 Scraping match {i+1}/{min(max_matches, len(match_links))}")
            
            match_content = self.get_page_content(link, use_selenium=True)
            if match_content:
                match_data = self.extract_match_data(match_content)
                if match_data:
                    matches.append(match_data)
            
            time.sleep(self.delay)  # Rate limiting
        
        return matches
    
    def scrape_points_table(self):
        """Scrape points table standings"""
        print("📊 Scraping IPL 2025 points table...")
        
        # Construct points table URL
        points_url = self.base_url + self.points_table_path
        
        content = self.get_page_content(points_url, use_selenium=True)
        if not content:
            print("❌ Failed to fetch points table page")
            return []
        
        points_data = self.extract_points_table(content)
        print(f"📊 Extracted {len(points_data)} point entries")
        
        return points_data
    
    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        output_path = Path(OUTPUT_CONFIG.get("output_dir", "data/raw"))
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        
        if not data:
            print(f"⚠️ No data to save to {filename}")
            return
        
        # Convert to DataFrame and save
        if filename == OUTPUT_CONFIG.get("csv_format", {}).get("matches", "matches.csv"):
            df = pd.DataFrame(data)
            df = df[['match_id', 'date', 'venue', 'team1', 'team2', 'toss_winner', 
                      'toss_decision', 'match_winner', 'win_margin', 'win_type', 'player_of_match']]
        elif filename == OUTPUT_CONFIG.get("csv_format", {}).get("points_table", "points_table.csv"):
            df = pd.DataFrame(data)
            df = df[['position', 'team', 'matches_played', 'won', 'lost', 'tied', 
                      'no_result', 'points', 'net_run_rate', 'scraped_at']]
        else:  # players data
            df = pd.DataFrame(data)
        
        df.to_csv(file_path, index=False)
        print(f"✅ Saved {len(data)} records to {file_path}")
    
    def save_to_json(self, data, filename):
        """Save data to JSON file"""
        output_path = Path(OUTPUT_CONFIG.get("output_dir", "data/raw"))
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(data)} records to {file_path}")
    
    def run_full_scrape(self, max_matches=10):
        """Run complete scraping process"""
        print("🚀 Starting IPL 2025 data scraping from ESPNcricinfo...")
        print(f"📅 Series ID: {self.series_id}")
        print(f"🌐 Base URL: {self.base_url}")
        
        # Scrape matches
        matches = self.scrape_matches(max_matches)
        
        # Scrape points table
        points_table = self.scrape_points_table()
        
        # Save data
        matches_file = OUTPUT_CONFIG.get("csv_format", {}).get("matches", "matches.csv")
        points_file = OUTPUT_CONFIG.get("csv_format", {}).get("points_table", "points_table.csv")
        players_file = OUTPUT_CONFIG.get("json_format", {}).get("players", "players.json")
        
        self.save_to_csv(matches, matches_file)
        self.save_to_csv(points_table, points_file)
        
        # Save player stats (extracted during match scraping)
        all_players = []
        for match in matches:
            if 'player_stats' in match:
                all_players.extend(match['player_stats'])
        
        if all_players:
            self.save_to_json(all_players, players_file)
        
        print("\n🎉 Scraping completed!")
        print(f"� Files created in {OUTPUT_CONFIG.get('output_dir', 'data/raw')}:")
        print(f"📅 {matches_file}: {len(matches)} matches")
        print(f"📊 {points_file}: {len(points_table)} teams")
        print(f"👥 {players_file}: {len(all_players)} player entries")
        
        return {
            'matches': matches,
            'points_table': points_table,
            'players': all_players
        }

def main():
    """Main function to run the scraper"""
    import argparse
    
    parser = argparse.ArgumentParser(description='IPL 2025 ESPNcricinfo Scraper')
    parser.add_argument('--max-matches', type=int, default=10, 
                       help='Maximum number of matches to scrape (default: 10)')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode')
    parser.add_argument('--delay', type=float, default=2.0,
                       help='Delay between requests in seconds (default: 2.0)')
    parser.add_argument('--output-dir', default=OUTPUT_CONFIG.get("output_dir", "data/raw"),
                       help=f'Output directory for scraped data (default: {OUTPUT_CONFIG.get("output_dir", "data/raw")}')
    
    args = parser.parse_args()
    
    # Initialize scraper
    scraper = IPLCricinfoScraper(headless=args.headless, delay=args.delay, output_dir=args.output_dir)
    
    try:
        # Run scraping
        results = scraper.run_full_scrape(max_matches=args.max_matches)
        
        if results['matches'] or results['points_table']:
            print("\n✅ Scraping successful!")
            print("📁 Files created:")
            matches_file = OUTPUT_CONFIG.get("csv_format", {}).get("matches", "matches.csv")
            points_file = OUTPUT_CONFIG.get("csv_format", {}).get("points_table", "points_table.csv")
            players_file = OUTPUT_CONFIG.get("json_format", {}).get("players", "players.json")
            print(f"  - {matches_file}: {len(results['matches'])} matches")
            print(f"  - {points_file}: {len(results['points_table'])} teams")
            if results.get('players'):
                print(f"  - {players_file}: {len(results['players'])} player entries")
        else:
            print("\n⚠️ No data scraped. Check if IPL 2025 is active.")
    
    except KeyboardInterrupt:
        print("\n🛑 Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Scraping failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

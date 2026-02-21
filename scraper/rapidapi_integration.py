#!/usr/bin/env python3
"""
RapidAPI Integration for IPL 2025 Project

This module provides integration with RapidAPI for fetching live and historical IPL data,
including match results, player statistics, and team rankings.
"""

import requests
import json
import time
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
import sys

class RapidAPIIntegration:
    def __init__(self, api_key=None, base_url="https://cricapi.com/api/v1"):
        self.api_key = api_key or os.getenv('RAPIDAPI_KEY')
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'IPL2025-ETL-Project/1.0',
            'Content-Type': 'application/json'
        })
        
    def get_series_info(self, series_id="IPL2025"):
        """Get series information for IPL 2025"""
        url = f"{self.base_url}/series_info"
        params = {'apikey': self.api_key, 'id': series_id}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching series info: {e}")
            return None
    
    def get_matches(self, series_id="IPL2025", limit=50):
        """Get match results for IPL 2025"""
        url = f"{self.base_url}/matches"
        params = {
            'apikey': self.api_key,
            'id': series_id,
            'limit': limit,
            'orderby': 'start_desc'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching matches: {e}")
            return None
    
    def get_match_scorecard(self, match_id):
        """Get detailed scorecard for a specific match"""
        url = f"{self.base_url}/match_scorecard"
        params = {
            'apikey': self.api_key,
            'id': match_id
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching match scorecard: {e}")
            return None
    
    def get_player_rankings(self, series_id="IPL2025"):
        """Get player rankings for IPL 2025"""
        url = f"{self.base_url}/player_rankings"
        params = {
            'apikey': self.api_key,
            'id': series_id,
            'format': 'json'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching player rankings: {e}")
            return None
    
    def get_team_rankings(self, series_id="IPL2025"):
        """Get team rankings for IPL 2025"""
        url = f"{self.base_url}/team_rankings"
        params = {
            'apikey': self.api_key,
            'id': series_id,
            'format': 'json'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching team rankings: {e}")
            return None
    
    def get_points_table(self, series_id="IPL2025"):
        """Get points table for IPL 2025"""
        url = f"{self.base_url}/points_table"
        params = {
            'apikey': self.api_key,
            'id': series_id,
            'format': 'json'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching points table: {e}")
            return None
    
    def save_to_csv(self, data, filename, output_dir="data/raw"):
        """Save data to CSV file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        
        if not data:
            print(f"⚠️ No data to save to {filename}")
            return False
        
        # Convert to DataFrame and save
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"✅ Saved {len(data)} records to {file_path}")
        return True
    
    def save_to_json(self, data, filename, output_dir="data/raw"):
        """Save data to JSON file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {len(data)} records to {file_path}")
        return True
    
    def convert_rapidapi_to_etl_format(self, api_data, data_type):
        """Convert RapidAPI data to ETL-compatible format"""
        if data_type == 'matches':
            converted_data = []
            for match in api_data.get('data', []):
                converted_match = {
                    'id': match.get('id'),
                    'season': match.get('season', {}).get('name', 'IPL2025'),
                    'date': match.get('starting_at', '').split('T')[0],
                    'city': match.get('venue', {}).get('city', ''),
                    'venue': match.get('venue', {}).get('name', ''),
                    'team1': match.get('teams', [{}])[0].get('name', ''),
                    'team2': match.get('teams', [{}])[1].get('name', ''),
                    'toss_winner': match.get('toss_winner', {}).get('name', ''),
                    'toss_decision': match.get('toss_decision', ''),
                    'result': match.get('status', ''),
                    'dl_applied': 0,
                    'winner': match.get('winner', {}).get('name', ''),
                    'win_by_runs': match.get('win_by_runs', 0),
                    'win_by_wickets': match.get('win_by_wickets', 0),
                    'player_of_match': match.get('player_of_match', {}).get('name', ''),
                    'venue': match.get('venue', {}).get('name', ''),
                    'umpire1': match.get('umpires', [{}])[0].get('name', ''),
                    'umpire2': match.get('umpires', [{}])[1].get('name', ''),
                    'umpire3': ''
                }
                converted_data.append(converted_match)
        
        elif data_type == 'players':
            converted_data = []
            for player in api_data.get('data', []):
                converted_player = {
                    'id': player.get('id'),
                    'player_name': player.get('name'),
                    'team': player.get('team', {}).get('name', ''),
                    'role': player.get('role', ''),
                    'batting_style': player.get('batting_style', ''),
                    'bowling_style': player.get('bowling_style', ''),
                    'country': player.get('country', ''),
                    'born_date': player.get('date_of_birth', ''),
                    'matches_played': player.get('matches_played', 0),
                    'runs_scored': player.get('runs', 0),
                    'wickets_taken': player.get('wickets', 0),
                    'catches': player.get('catches', 0),
                    'stumpings': player.get('stumpings', 0)
                }
                converted_data.append(converted_player)
        
        return converted_data
    
    def fetch_all_data(self, series_id="IPL2025", max_matches=100):
        """Fetch all data from RapidAPI"""
        print(f"🚀 Fetching IPL 2025 data from RapidAPI...")
        
        # Get series info
        series_info = self.get_series_info(series_id)
        if not series_info:
            return False
        
        print(f"📊 Series: {series_info.get('title')}")
        print(f"📅 Season: {series_info.get('season', {}).get('name', 'Unknown')}")
        
        # Get matches
        matches_data = self.get_matches(series_id, max_matches)
        if not matches_data:
            return False
        
        matches = matches_data.get('data', [])
        print(f"📅 Fetched {len(matches)} matches")
        
        # Get player rankings
        player_rankings = self.get_player_rankings(series_id)
        if not player_rankings:
            return False
        
        players = player_rankings.get('data', [])
        print(f"👥 Fetched {len(players)} player rankings")
        
        # Get team rankings
        team_rankings = self.get_team_rankings(series_id)
        if not team_rankings:
            return False
        
        teams = team_rankings.get('data', [])
        print(f"🏆 Fetched {len(teams)} team rankings")
        
        # Get points table
        points_table = self.get_points_table(series_id)
        if not points_table:
            return False
        
        points = points_table.get('data', [])
        print(f"📊 Fetched {len(points)} points table entries")
        
        # Convert to ETL format
        converted_matches = self.convert_rapidapi_to_etl_format(matches_data, 'matches')
        converted_players = self.convert_rapidapi_to_etl_format(players_data, 'players')
        converted_points = self.convert_rapidapi_to_etl_format(points_data, 'points')
        
        # Save to files
        self.save_to_csv(converted_matches, 'matches.csv')
        self.save_to_csv(converted_points, 'points_table.csv')
        self.save_to_json(converted_players, 'players.json')
        
        print("\n🎉 RapidAPI data collection completed!")
        print("📁 Files created:")
        print("  - data/raw/matches.csv")
        print("  - data/raw/points_table.csv")
        print("  - data/raw/players.json")
        
        return {
            'matches': len(converted_matches),
            'players': len(converted_players),
            'points': len(converted_points)
        }

def main():
    """Main function to run RapidAPI integration"""
    import argparse
    
    parser = argparse.ArgumentParser(description='IPL 2025 RapidAPI Integration')
    parser.add_argument('--api-key', type=str, 
                       help='RapidAPI key (or set RAPIDAPI_KEY environment variable)')
    parser.add_argument('--series-id', type=str, default='IPL2025',
                       help='Series ID for IPL 2025')
    parser.add_argument('--max-matches', type=int, default=50,
                       help='Maximum number of matches to fetch (default: 50)')
    parser.add_argument('--output-dir', type=str, default='data/raw',
                       help='Output directory for fetched data')
    
    args = parser.parse_args()
    
    # Initialize RapidAPI client
    client = RapidAPIIntegration(api_key=args.api_key)
    
    try:
        # Fetch all data
        results = client.fetch_all_data(args.series_id, args.max_matches)
        
        if results:
            print("\n✅ RapidAPI integration successful!")
            print(f"📊 Results: {results}")
        else:
            print("\n❌ RapidAPI integration failed!")
    
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
import json

class IPLDataGenerator:
    def __init__(self):
        self.teams = [
            "Mumbai Indians", "Chennai Super Kings", "Kolkata Knight Riders",
            "Royal Challengers Bangalore", "Delhi Capitals", "Sunrisers Hyderabad",
            "Rajasthan Royals", "Punjab Kings", "Gujarat Titans", "Lucknow Super Giants"
        ]
        
        self.venues = [
            "Wankhede Stadium", "Eden Gardens", "Chepauk Stadium", "M Chinnaswamy Stadium",
            "Arun Jaitley Stadium", "Rajiv Gandhi Stadium", "Sawai Mansingh Stadium",
            "Punjab Cricket Association Stadium", "Narendra Modi Stadium", "BRSABV Ekana Stadium"
        ]
        
        self.player_pool = self.generate_player_pool()
        
    def generate_player_pool(self):
        """Generate realistic player pool with IPL-style names and stats"""
        first_names = ["Rohit", "Virat", "MS", "Jasprit", "Ravindra", "Hardik", "KL", "Shikhar", 
                     "Rishabh", "Sanju", "Jos", "David", "Faf", "Kane", "Trent", "Rashid", "Yuzvendra"]
        last_names = ["Sharma", "Kohli", "Dhoni", "Bumrah", "Jadeja", "Pandya", "Rahul", "Dhawan",
                     "Pant", "Samson", "Buttler", "Warner", "du Plessis", "Williamson", "Boult", "Khan", "Chahal"]
        
        roles = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
        batting_styles = ["Right-handed", "Left-handed"]
        bowling_styles = ["Right-arm fast", "Left-arm fast", "Right-arm off-break", "Left-arm orthodox", ""]
        countries = ["India", "Australia", "England", "South Africa", "New Zealand", "West Indies", "Afghanistan"]
        
        players = []
        for i in range(200):  # Generate 200 players
            player = {
                'id': i + 1,
                'player_name': f"{random.choice(first_names)} {random.choice(last_names)}",
                'team': random.choice(self.teams),
                'role': random.choice(roles),
                'batting_style': random.choice(batting_styles),
                'bowling_style': random.choice(bowling_styles) if random.random() > 0.3 else "",
                'country': random.choice(countries),
                'born_date': f"{random.randint(1985, 2002)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                'matches_played': random.randint(10, 250),
                'runs_scored': random.randint(0, 8000),
                'wickets_taken': random.randint(0, 300),
                'catches': random.randint(0, 200),
                'stumpings': random.randint(0, 50) if random.random() > 0.8 else 0
            }
            players.append(player)
        
        return players
    
    def generate_matches(self, num_matches=74):
        """Generate realistic IPL match data"""
        matches = []
        match_id = 1
        
        # Generate round-robin schedule
        for _ in range(num_matches):
            team1, team2 = random.sample(self.teams, 2)
            venue = random.choice(self.venues)
            
            # Generate realistic match date (March-May 2025)
            start_date = datetime(2025, 3, 22)
            end_date = datetime(2025, 5, 25)
            match_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
            
            # Determine winner based on team strength
            winner = team1 if random.random() > 0.5 else team2
            toss_winner = team1 if random.random() > 0.5 else team2
            toss_decision = random.choice(["bat", "field"])
            
            # Generate realistic scores
            if toss_decision == "bat" and toss_winner == winner:
                win_by_wickets = random.randint(1, 10)
                win_by_runs = 0
            elif toss_decision == "field" and toss_winner == winner:
                win_by_runs = random.randint(1, 50)
                win_by_wickets = 0
            else:
                win_by_runs = random.randint(1, 50) if random.random() > 0.3 else 0
                win_by_wickets = random.randint(1, 10) if win_by_runs == 0 else 0
            
            match = {
                'id': match_id,
                'season': 2025,
                'city': venue.split()[0],  # Extract city name
                'date': match_date.strftime('%Y-%m-%d'),
                'team1': team1,
                'team2': team2,
                'toss_winner': toss_winner,
                'toss_decision': toss_decision,
                'result': 'normal',
                'dl_applied': 0,
                'winner': winner,
                'win_by_runs': win_by_runs,
                'win_by_wickets': win_by_wickets,
                'player_of_match': random.choice([p['player_name'] for p in self.player_pool[:50]]),
                'venue': venue,
                'umpire1': f"Umpire{match_id}",
                'umpire2': f"Umpire{match_id+1}",
                'umpire3': ""
            }
            matches.append(match)
            match_id += 1
        
        return matches
    
    def generate_deliveries(self, matches):
        """Generate realistic ball-by-ball data"""
        deliveries = []
        delivery_id = 1
        
        for match in matches:
            # Generate 20 overs per innings (2 innings per match)
            for inning in [1, 2]:
                batting_team = match['team1'] if inning == 1 else match['team2']
                bowling_team = match['team2'] if inning == 1 else match['team1']
                
                # Get players for this match
                team_players = [p for p in self.player_pool if p['team'] in [batting_team, bowling_team]]
                batsmen = [p for p in team_players if p['team'] == batting_team][:6]
                bowlers = [p for p in team_players if p['team'] == bowling_team][:4]
                
                over = 0
                while over < 20:
                    ball = 1
                    while ball <= 6:
                        # Random batsman and bowler
                        batsman = random.choice(batsmen)['player_name']
                        non_striker = random.choice([b for b in batsmen if b['player_name'] != batsman])['player_name']
                        bowler = random.choice(bowlers)['player_name']
                        
                        # Generate realistic ball outcome
                        runs_distribution = [0.35, 0.25, 0.15, 0.10, 0.08, 0.04, 0.02, 0.01]  # 0-6 runs
                        runs_options = [0, 1, 2, 3, 4, 5, 6, 7]  # 7 represents 6+ runs
                        batsman_runs = np.random.choice(runs_options, p=runs_distribution)
                        if batsman_runs == 7:
                            batsman_runs = random.randint(6, 8)  # Convert 7 to 6-8 runs
                        
                        # Extras
                        wide_runs = 1 if random.random() < 0.05 else 0
                        bye_runs = 1 if random.random() < 0.02 else 0
                        legbye_runs = 1 if random.random() < 0.03 else 0
                        noball_runs = 1 if random.random() < 0.03 else 0
                        
                        extra_runs = wide_runs + bye_runs + legbye_runs + noball_runs
                        total_runs = batsman_runs + extra_runs
                        
                        # Wickets
                        is_wicket = random.random() < 0.05  # 5% chance of wicket
                        player_dismissed = ""
                        dismissal_kind = ""
                        fielder = ""
                        
                        if is_wicket and batsman_runs == 0:
                            player_dismissed = batsman
                            dismissal_kinds = ["caught", "bowled", "lbw", "run out", "stumped"]
                            dismissal_kind = random.choice(dismissal_kinds)
                            if dismissal_kind in ["caught", "stumped"]:
                                fielder = random.choice([p['player_name'] for p in team_players[:10]])
                        
                        delivery = {
                            'id': delivery_id,
                            'match_id': match['id'],
                            'inning': inning,
                            'batting_team': batting_team,
                            'bowling_team': bowling_team,
                            'over': over + 1,
                            'ball': ball,
                            'batsman': batsman,
                            'non_striker': non_striker,
                            'bowler': bowler,
                            'is_super_over': 0,
                            'wide_runs': wide_runs,
                            'bye_runs': bye_runs,
                            'legbye_runs': legbye_runs,
                            'noball_runs': noball_runs,
                            'penalty_runs': 0,
                            'batsman_runs': batsman_runs,
                            'extra_runs': extra_runs,
                            'total_runs': total_runs,
                            'player_dismissed': player_dismissed,
                            'dismissal_kind': dismissal_kind,
                            'fielder': fielder
                        }
                        deliveries.append(delivery)
                        delivery_id += 1
                        
                        # Handle extra balls
                        if wide_runs > 0 or noball_runs > 0:
                            continue  # Replay the ball
                        ball += 1
                    over += 1
        
        return deliveries
    
    def generate_venues(self):
        """Generate realistic venue data"""
        venues = []
        
        for i, venue_name in enumerate(self.venues):
            venue = {
                'id': i + 1,
                'name': venue_name,
                'city': venue_name.split()[0],  # Extract city name
                'capacity': random.randint(30000, 100000),  # Realistic stadium capacities
                'timezone': 'Asia/Kolkata' if 'Kolkata' in venue_name else 
                          'Asia/Mumbai' if 'Mumbai' in venue_name else
                          'Asia/Chennai' if 'Chennai' in venue_name else
                          'Asia/Delhi' if 'Delhi' in venue_name else
                          'Asia/Bengaluru' if 'Bengaluru' in venue_name else
                          'Asia/Hyderabad' if 'Hyderabad' in venue_name else
                          'Asia/Jaipur' if 'Jaipur' in venue_name else
                          'Asia/Ahmedabad' if 'Ahmedabad' in venue_name else
                          'Asia/Lucknow' if 'Lucknow' in venue_name else
                          'UTC+5:30'  # Default timezone
            }
            venues.append(venue)
        
        return venues
    
    def generate_points_table(self):
        points_data = []
        
        for team in self.teams:
            matches_played = 14  # Each team plays 14 matches in IPL
            won = random.randint(2, 12)
            lost = matches_played - won - random.randint(0, 2)
            tied = random.randint(0, 2)
            no_result = matches_played - won - lost - tied
            
            points = won * 2 + tied * 1
            net_run_rate = round(random.uniform(-2.0, 2.5), 3)
            
            points_entry = {
                'id': self.teams.index(team) + 1,
                'season': 2025,
                'team': team,
                'matches_played': matches_played,
                'won': won,
                'lost': lost,
                'tied': tied,
                'no_result': no_result,
                'points': points,
                'net_run_rate': net_run_rate,
                'for_overs': round(random.uniform(2400, 3200), 1),
                'against_overs': round(random.uniform(2400, 3200), 1),
                'position': 0  # Will be calculated later
            }
            points_data.append(points_entry)
        
        # Sort by points and assign positions
        points_data.sort(key=lambda x: (-x['points'], x['net_run_rate']))
        for i, entry in enumerate(points_data):
            entry['position'] = i + 1
        
        return points_data
    
    def save_datasets(self, output_dir="data/raw"):
        """Generate and save all datasets"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print("🏏 Generating realistic IPL 2025 datasets...")
        
        # Generate venues
        venues = self.generate_venues()
        venues_df = pd.DataFrame(venues)
        venues_df.to_csv(output_path / "ipl_2025_venues.csv", index=False)
        print(f"✅ Generated {len(venues)} venues")
        
        # Generate matches
        matches = self.generate_matches(74)
        matches_df = pd.DataFrame(matches)
        matches_df.to_csv(output_path / "ipl_2025_matches.csv", index=False)
        print(f"✅ Generated {len(matches)} matches")
        
        # Generate deliveries
        deliveries = self.generate_deliveries(matches)
        deliveries_df = pd.DataFrame(deliveries)
        deliveries_df.to_csv(output_path / "ipl_2025_ball_by_ball.csv", index=False)
        print(f"✅ Generated {len(deliveries)} deliveries")
        
        # Generate players
        players_df = pd.DataFrame(self.player_pool)
        players_df.to_csv(output_path / "ipl_2025_players.csv", index=False)
        print(f"✅ Generated {len(self.player_pool)} players")
        
        # Generate points table
        points = self.generate_points_table()
        points_df = pd.DataFrame(points)
        points_df.to_csv(output_path / "ipl_2025_teams.csv", index=False)
        print(f"✅ Generated points table for {len(points)} teams")
        
        # Generate venues
        venues = self.generate_venues()
        venues_df = pd.DataFrame(venues)
        venues_df.to_csv(output_path / "ipl_2025_venues.csv", index=False)
        print(f"✅ Generated {len(venues)} venues")
        
        print(f"\n📊 All datasets saved to {output_path}")
        print("\n📈 Dataset Summary:")
        print(f"  Matches: {len(matches)}")
        print(f"  Deliveries: {len(deliveries)}")
        print(f"  Players: {len(self.player_pool)}")
        print(f"  Teams: {len(points)}")
        print(f"  Venues: {len(venues)}")
        
        return matches_df, deliveries_df, players_df, points_df, venues_df

def main():
    """Main function to generate IPL datasets"""
    generator = IPLDataGenerator()
    matches_df, deliveries_df, players_df, points_df, venues_df = generator.save_datasets()
    
    print("\n🎯 Sample Data Preview:")
    print("\nMatches Sample:")
    print(matches_df[['team1', 'team2', 'winner', 'venue']].head())
    
    print("\nTop 5 Teams by Points:")
    print(points_df[['team', 'points', 'net_run_rate', 'position']].head())
    
    print("\nPlayer Sample:")
    print(players_df[['player_name', 'team', 'role', 'matches_played']].head())

if __name__ == "__main__":
    main()

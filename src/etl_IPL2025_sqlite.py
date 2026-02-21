import pandas as pd
import sqlite3
import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IPLETLPipeline:
    def __init__(self, data_dir="data", db_name="IPL2025.db"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.db_dir = self.data_dir / "db"
        self.db_path = self.db_dir / db_name
        
        # Ensure directories exist
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.db_dir.mkdir(parents=True, exist_ok=True)
        
        self.conn = None
    
    def connect_to_db(self):
        """Establish connection to SQLite database"""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            logger.info(f"Connected to database: {self.db_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def create_tables(self):
        """Create all necessary tables in SQLite database"""
        if not self.conn:
            logger.error("No database connection")
            return False
        
        try:
            cursor = self.conn.cursor()
            
            # Matches table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matches (
                    id INTEGER PRIMARY KEY,
                    season INTEGER,
                    city TEXT,
                    date TEXT,
                    team1 TEXT,
                    team2 TEXT,
                    toss_winner TEXT,
                    toss_decision TEXT,
                    result TEXT,
                    dl_applied INTEGER,
                    winner TEXT,
                    win_by_runs INTEGER,
                    win_by_wickets INTEGER,
                    player_of_match TEXT,
                    venue TEXT,
                    umpire1 TEXT,
                    umpire2 TEXT,
                    umpire3 TEXT
                )
            ''')
            
            # Deliveries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS deliveries (
                    id INTEGER PRIMARY KEY,
                    match_id INTEGER,
                    inning INTEGER,
                    batting_team TEXT,
                    bowling_team TEXT,
                    over INTEGER,
                    ball INTEGER,
                    batsman TEXT,
                    non_striker TEXT,
                    bowler TEXT,
                    is_super_over INTEGER,
                    wide_runs INTEGER,
                    bye_runs INTEGER,
                    legbye_runs INTEGER,
                    noball_runs INTEGER,
                    penalty_runs INTEGER,
                    batsman_runs INTEGER,
                    extra_runs INTEGER,
                    total_runs INTEGER,
                    player_dismissed TEXT,
                    dismissal_kind TEXT,
                    fielder TEXT,
                    FOREIGN KEY (match_id) REFERENCES matches (id)
                )
            ''')
            
            # Players table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    player_name TEXT,
                    team TEXT,
                    role TEXT,
                    batting_style TEXT,
                    bowling_style TEXT,
                    country TEXT,
                    born_date TEXT,
                    matches_played INTEGER,
                    runs_scored INTEGER,
                    wickets_taken INTEGER,
                    catches INTEGER,
                    stumpings INTEGER
                )
            ''')
            
            # Points table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS points_table (
                    id INTEGER PRIMARY KEY,
                    season INTEGER,
                    team TEXT,
                    matches_played INTEGER,
                    won INTEGER,
                    lost INTEGER,
                    tied INTEGER,
                    no_result INTEGER,
                    points INTEGER,
                    net_run_rate REAL,
                    for_overs REAL,
                    against_overs REAL,
                    position INTEGER
                )
            ''')
            
            self.conn.commit()
            logger.info("All tables created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create tables: {e}")
            return False
    
    def load_csv_data(self, filename):
        """Load CSV data from raw directory"""
        file_path = self.raw_dir / filename
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows from {filename}")
            return df
        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
            return None
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return None
    
    def insert_matches_data(self, df):
        """Insert matches data into database"""
        if df is None or df.empty:
            logger.warning("No matches data to insert")
            return False
        
        try:
            df.to_sql('matches', self.conn, if_exists='replace', index=False)
            logger.info(f"Inserted {len(df)} matches records")
            return True
        except Exception as e:
            logger.error(f"Error inserting matches data: {e}")
            return False
    
    def insert_deliveries_data(self, df):
        """Insert deliveries data into database"""
        if df is None or df.empty:
            logger.warning("No deliveries data to insert")
            return False
        
        try:
            df.to_sql('deliveries', self.conn, if_exists='replace', index=False)
            logger.info(f"Inserted {len(df)} deliveries records")
            return True
        except Exception as e:
            logger.error(f"Error inserting deliveries data: {e}")
            return False
    
    def insert_players_data(self, df):
        """Insert players data into database"""
        if df is None or df.empty:
            logger.warning("No players data to insert")
            return False
        
        try:
            df.to_sql('players', self.conn, if_exists='replace', index=False)
            logger.info(f"Inserted {len(df)} players records")
            return True
        except Exception as e:
            logger.error(f"Error inserting players data: {e}")
            return False
    
    def insert_points_table_data(self, df):
        """Insert points table data into database"""
        if df is None or df.empty:
            logger.warning("No points table data to insert")
            return False
        
        try:
            df.to_sql('points_table', self.conn, if_exists='replace', index=False)
            logger.info(f"Inserted {len(df)} points table records")
            return True
        except Exception as e:
            logger.error(f"Error inserting points table data: {e}")
            return False
    
    def run_etl_pipeline(self):
        """Run the complete ETL pipeline"""
        logger.info("Starting IPL2025 ETL Pipeline")
        
        # Connect to database
        if not self.connect_to_db():
            return False
        
        # Create tables
        if not self.create_tables():
            return False
        
        # Load and insert data
        files_to_process = [
            ('matches.csv', self.insert_matches_data),
            ('deliveries.csv', self.insert_deliveries_data),
            ('players.csv', self.insert_players_data),
            ('points_table.csv', self.insert_points_table_data)
        ]
        
        success_count = 0
        for filename, insert_function in files_to_process:
            df = self.load_csv_data(filename)
            if df is not None and insert_function(df):
                success_count += 1
        
        logger.info(f"ETL Pipeline completed. {success_count}/{len(files_to_process)} files processed successfully")
        
        # Close connection
        if self.conn:
            self.conn.close()
        
        return success_count == len(files_to_process)
    
    def get_data_summary(self):
        """Get summary of data in database"""
        if not self.connect_to_db():
            return None
        
        try:
            summary = {}
            tables = ['matches', 'deliveries', 'players', 'points_table']
            
            for table in tables:
                cursor = self.conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                summary[table] = count
            
            self.conn.close()
            return summary
            
        except Exception as e:
            logger.error(f"Error getting data summary: {e}")
            return None

def main():
    """Main function to run the ETL pipeline"""
    etl = IPLETLPipeline()
    
    # Run the pipeline
    success = etl.run_etl_pipeline()
    
    if success:
        print("✅ ETL Pipeline completed successfully!")
        
        # Show data summary
        summary = etl.get_data_summary()
        if summary:
            print("\n📊 Data Summary:")
            for table, count in summary.items():
                print(f"  {table}: {count:,} records")
    else:
        print("❌ ETL Pipeline failed. Check logs for details.")

if __name__ == "__main__":
    main()

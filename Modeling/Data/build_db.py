import sqlite3
import sys

def create_australia_historical_games_table():
    # create db if it doesn't exist called db.sqlite3
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    
    # create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS historical_games
                (
                id INTEGER PRIMARY KEY, 
                season INTEGER, 
                week INTEGER, 
                home_team TEXT, 
                away_team TEXT,
                home_score INTEGER,
                away_score INTEGER,
                home_line_close REAL,
                home_spread_diff REAL,
                over_under_close REAL,
                total_points REAL,
                over_under_diff REAL
                over_under_result TEXT,
                home_cover_result TEXT
                )''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_australia_historical_games_table()

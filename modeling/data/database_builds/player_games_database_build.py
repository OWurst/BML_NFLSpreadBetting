import sqlite3
import pandas as pd

def create_players_table(conn):
    conn.execute('''
        CREATE TABLE players (
            player_id INTEGER PRIMARY KEY,
            player_name TEXT,
            player_position TEXT,
            player_current_team TEXT
        )
    ''')